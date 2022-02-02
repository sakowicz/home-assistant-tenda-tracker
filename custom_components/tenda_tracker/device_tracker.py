import hashlib
import json
import logging
from time import time
import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.device_tracker import (
    DOMAIN,
    PLATFORM_SCHEMA,
    DeviceScanner,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

HTTP_HEADER_NO_CACHE = "no-cache"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


def get_scanner(hass, config):
    scanner = TendaDeviceScanner(config[DOMAIN])
    if scanner.is_initialized:
        return scanner
    return None


class TendaDeviceScanner(DeviceScanner):
    def __init__(self, config):
        host = config[CONF_HOST]
        password = config[CONF_PASSWORD]
        self.is_initialized = False
        self.last_results = {}

        try:
            self.tenda_client = TendaClient(host, password)
            self._update_info()
            self.is_initialized = True
        except requests.exceptions.ConnectionError:
            _LOGGER.error("Cannot connect to tenda device")

    def scan_devices(self):
        _LOGGER.debug("Scanning devices...")
        self._update_info()
        return self.last_results

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        _LOGGER.debug("Loading wireless clients...")
        self.last_results = self.tenda_client.get_connected_devices()


class TendaClient:
    def __init__(self, host: str, password: str) -> None:
        self.host = host
        self.password = password
        self.cookies = None
        self.is_authorized = None

    def auth(self):
        _LOGGER.debug("Trying to authorize")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        data = (
                "username=admin&password=" + hashlib.md5(self.password.encode()).hexdigest()
        )
        response = requests.post(
            "http://" + self.host + "/login/Auth",
            headers=headers,
            data=data,
            verify=False,
            allow_redirects=False,
        )
        self.cookies = response.cookies

    def get_connected_devices(self):
        if self.cookies is None:
            _LOGGER.debug("Cookies not found")
            self.auth()

        response = requests.get(
            "http://" + self.host + "/goform/getOnlineList?" + str(time()),
            verify=False,
            cookies=self.cookies,
            allow_redirects=False,
        )

        try:
            json_response = json.loads(response.content)
        except json.JSONDecodeError:
            self.cookies = None
            return self.get_connected_devices()

        devices = {}

        for device in json_response:
            mac = None
            name = None

            if "deviceId" in device:
                mac = device.get("deviceId")
            elif "localhostName" in device:
                mac = device.get("localhostMac")

            if "devName" in device:
                name = device.get("devName")
            elif "localhostName" in device:
                name = device.get("localhostName")

            if mac is not None and name is not None:
                devices[mac] = name

        return devices
