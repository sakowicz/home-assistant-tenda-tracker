## Tenda AC23 Router Device Tracker

Adds device tracking support for [Tenda AC23](https://www.tendacn.com/product/AC23.html) to [Home Assistant](https://www.home-assistant.io/).

## Setup Process

1. Install using [HACS](https://github.com/hacs/integration) or manually copy the files
2. Add tenda_tracker to your configuration.yaml
3. Restart Home Assistant

## Step 1: Installation

### Installation with Home Assistant Community Store (HACS)

For easy updates whenever a new version is released, use the [Home Assistant Community Store (HACS)](https://github.com/hacs/integration) and add the following Integration in the Settings tab:

```
sakowicz/home-assistant-tenda-tracker
```

## Step 2: Add Tracker to Home Assistant's Configuration

Now that that installation and authentication are done, all that is left is to add the [device_tracker](https://www.home-assistant.io/integrations/device_tracker/) to your `configuration.yaml`.

The minimum required configuration:

```yaml
device_tracker:
  - platform: eero_tracker
    host: 192.168.1.1
    password: <password to admin panel>
```

## Step 3: Restart and Test

You should see new devices in your entities. Their names will appear as you configured them before in Tenda admin panel or as their hostname or mac address. You can manipulate them in `known_devices.yaml`.



### Disclamer

I am not a python developer so code can be not as clean as I would want to. Feel free to contribute and do refactor!
