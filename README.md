# BP Homecharge integration for Home Assistant

This is an early attempt at a simple Home Assistant integration for BP Chargemaster Homecharge units using the ChargeVision platform.

It is based on earlier work towards an unofficial API client by James Muscat.

**Pretty much immediately after I got this working but not fully tested, my Homecharge unit decided to stop sending updates to Chargevision.  Hopefully this is a coincidence and it will come back.  For now, I have not been able to test monitoring of charging sessions and have suspended any work on this until it decides to communicate again (yes I have tried rebooting).**

## Installation

This should be available through HACS in future which will make installation easier.  For now, copy `custom_components/homecharge` into your custom_components directory in your Home Assistant config dir.

Then, add the following to configuration.yaml:

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
