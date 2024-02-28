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

            self.hass.data[DOMAIN]['advice_charging'] = hc_cur_status['advice_charging']
            
            # update everything else too
            self.hass.data[DOMAIN]['advice_header'] = hc_cur_status['advice_header']
            self.hass.data[DOMAIN]['override'] = hc_cur_status['override']

            return
