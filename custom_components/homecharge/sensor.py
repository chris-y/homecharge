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
    add_entities([AdviceHeaderSensor(),
        AdviceMessageSensor(),
        PowerSensor(),
        PowerReasonSensor()])

class AdviceHeaderSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge header"
        
    def __init__(self):
        '''init'''

    #@property
    #def device_class(self):
    #    return BinarySensorDeviceClass.BATTERY_CHARGING
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_header']

class AdviceMessageSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge message"
        
    def __init__(self):
        '''init'''

    #@property
    #def device_class(self):
    #    return BinarySensorDeviceClass.BATTERY_CHARGING
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_message']

class PowerSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge power"
        
    def __init__(self):
        '''init'''

    @property
    def device_class(self):
        return SensorDeviceClass.CURRENT
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['power']
        
    @property
    def native_unit_of_measurement(self):
        return "A"

class PowerReasonSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge power reason"
        
    def __init__(self):
        '''init'''

    #@property
    #def device_class(self):
    #    return BinarySensorDeviceClass.BATTERY_CHARGING
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['power_reason']

