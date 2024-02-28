from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass
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
    add_entities([AdviceHeaderSensor()])

class AdviceHeaderSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge header"
        
    def __init__(self):
        '''init''' #self._is_on = self.hass.data[DOMAIN]['override']

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_header']

