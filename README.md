# BP Homecharge integration for Home Assistant

This is an early attempt at a simple Home Assistant integration for BP Chargemaster Homecharge units using the ChargeVision platform.

It is based on earlier work towards an unofficial API client by James Muscat.

## Installation

### HACS

Add the repository:
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=chris-y&repository=homecharge&category=integration)

### Manual
Copy `custom_components/homecharge` into your custom_components directory in your Home Assistant config dir.

### Configuration
Add the following to configuration.yaml:

```
homecharge:
    username: "email"
    password: "password"

```

If you restart Home Assistant it should log in and retrieve details, which for the moment appear under the generic sensors areas prefixed with Homecharge.

## Features

* View the car charging status directly in Home Assistant
* Toggle schedule override

You could set one short schedule to get the charger into "smart" mode and use the override toggle to control charging the car directly from HA - eg. start charging when electricity is cheapest or greenest. 
