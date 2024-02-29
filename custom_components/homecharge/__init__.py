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
            
            c_duration = None
            c_energy = 0
            
            hc_cur_status = hcstatus['status']
            
            if hc_cur_status['charge_id'] is not None:
                advice_charging = hc_cur_status['advice_charging']
                power = hc_cur_status['power']
                power_reason = hc_cur_status['power_reason']
                override = hc_cur_status['override']
                started_ts = hc_cur_status['started_ts']
                energy = hc_cur_status['energy']
                
                hc_charges = get_charges()
                hc_cur_charge = hc_charges['recharges'][0]
                
                if hc_cur_charge['charge_id'] == hc_cur_status['charge_id']:
                    c_duration = hc_cur_charge['duration']
                    c_energy = hc_cur_charge['energy']

            else:
                advice_charging = False
                power = 0
                power_reason = ''
                override = False
                started_ts = None
                energy = 0

            
            hass.data[DOMAIN] = {
                'hc': hc,
                'user': email,
                'pass': pw,
                'override': override,
                'advice_charging': advice_charging,
                'advice_header': hc_cur_status['advice_header'],
                'advice_message': hc_cur_status['advice_message'],
                'advice_schedule': hc_cur_status['advice_schedule'],
                'advice_chargelevel': hc_cur_status['advice_chargelevel'],
                'advice_maxkwh': hc_cur_status['advice_maxkwh'],
                'charge_id': hc_cur_status['charge_id'],
                'power' : power,
                'power_reason': power_reason,
                'started_ts': started_ts,
                'energy': 0,
                'c_duration': c_duration,
                'c_energy': c_energy
            }

            hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
            hass.helpers.discovery.load_platform('binary_sensor', DOMAIN, {}, config)
            hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
            
            return True

        return False


