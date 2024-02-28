from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
    add_entities([OverrideSwitch()])

class OverrideSwitch(SwitchEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge schedule override"
        
    def __init__(self):
        '''init''' #self._is_on = self.hass.data[DOMAIN]['override']
        
    @property
    def is_on(self):
        return self.hass.data[DOMAIN]['override']

    def _toggle(self):
        hc = self.hass.data[DOMAIN]['hc']
        if hc:
            hc.override()
            hcstatus = hc.get_status()
            hc_cur_status = hcstatus['status']
            self.hass.data[DOMAIN]['override'] = hc_cur_status['override']
            
            
    def turn_on(self, **kwargs):
        return self._toggle()
        
    def turn_off(self, **kwargs):
        return self._toggle()

    def update(self):
        hc = self.hass.data[DOMAIN]['hc']
        if hc:
            hcstatus = hc.get_status()
            hc_cur_status = hcstatus['status']
                
            self.hass.data[DOMAIN]['override'] = hc_cur_status['override']
            return

