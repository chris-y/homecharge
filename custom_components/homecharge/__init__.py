from __future__ import annotations

from . import homecharge

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType


import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = "homecharge"

CONF_USER = "username"
CONF_PASS = "password"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USER): cv.string,
        vol.Required(CONF_PASS): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    hc = homecharge.Client()
    if hc:
        email = config[DOMAIN].get(CONF_USER)
        pw = config[DOMAIN].get(CONF_PASS)

        try:
            apikey = hc.login(email, pw)
        except:
            return False

        if apikey:
            hcstatus = hc.get_status()
            hass.states.set("homecharge.serial", hcstatus['serial'])
            
            hc_cur_status = hcstatus['status']
            
            hass.data[DOMAIN] = {
                'hc': hc,
                'user': email,
                'pass': pw,
                'override': hc_cur_status['override'],
                'advice_charging': hc_cur_status['advice_charging'],
                'advice_header': hc_cur_status['advice_header']
            }

            hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
            hass.helpers.discovery.load_platform('binary_sensor', DOMAIN, {}, config)
            hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
            
            return True

        return False


