from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from . import homecharge

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities([ChargingSensor()])

class ChargingSensor(BinarySensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charging"
        
    def __init__(self):
        '''init''' #self._is_on = self.hass.data[DOMAIN]['override']

    @property
    def device_class(self):
        return BinarySensorDeviceClass.BATTERY_CHARGING
    
    @property
    def is_on(self):
        return self.hass.data[DOMAIN]['advice_charging']

    def update(self):
        hc = self.hass.data[DOMAIN]['hc']
        if hc:
            hcstatus = hc.get_status()
            hc_cur_status = hcstatus['status']
            
            # update everything
            self.hass.data[DOMAIN]['advice_header'] = hc_cur_status['advice_header']
            self.hass.data[DOMAIN]['advice_message'] = hc_cur_status['advice_message']
            self.hass.data[DOMAIN]['advice_schedule'] = hc_cur_status['advice_schedule']
            self.hass.data[DOMAIN]['advice_chargelevel'] = hc_cur_status['advice_chargelevel']
            self.hass.data[DOMAIN]['advice_maxkwh'] = hc_cur_status['advice_maxkwh']
            self.hass.data[DOMAIN]['charge_id'] = hc_cur_status['charge_id']
            
            if hc_cur_status['charge_id'] is not None:
                self.hass.data[DOMAIN]['advice_charging'] = hc_cur_status['advice_charging']
                self.hass.data[DOMAIN]['power'] = hc_cur_status['power']
                self.hass.data[DOMAIN]['power_reason'] = hc_cur_status['power_reason']
                self.hass.data[DOMAIN]['override'] = hc_cur_status['override']
                self.hass.data[DOMAIN]['started_ts'] = hc_cur_status['started_ts']
                self.hass.data[DOMAIN]['energy'] = hc_cur_status['energy']
                
                hc_charges = get_charges()
                hc_cur_charge = hc_charges['recharges'][0]
                
                if hc_cur_charge['charge_id'] == hc_cur_status['charge_id']:
                    self.hass.data[DOMAIN]['c_duration'] = hc_cur_charge['duration']
                    self.hass.data[DOMAIN]['c_energy'] = hc_cur_charge['energy']
            
            else:
                self.hass.data[DOMAIN]['advice_charging'] = False
                self.hass.data[DOMAIN]['power'] = 0
                self.hass.data[DOMAIN]['power_reason'] = ''
                self.hass.data[DOMAIN]['override'] = False
                self.hass.data[DOMAIN]['started_ts'] = None
                self.hass.data[DOMAIN]['energy'] = 0
                self.hass.data[DOMAIN]['c_duration'] = None
                self.hass.data[DOMAIN]['c_energy'] = 0

            return
