from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import datetime

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
    add_entities([AdviceHeaderSensor(hass),
        AdviceMessageSensor(hass),
        AdviceScheduleSensor(hass),
        AdviceChargeLevelSensor(hass),
        AdviceMaxkWh(hass),
        ChargeIDSensor(hass),
        StartedSensor(hass),
        EnergySensor(hass),
        PowerSensor(hass),
        PowerReasonSensor(hass),
        TotalChargesSensor(hass),
        CurrentEnergySensor(hass)])

class AdviceHeaderSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge status"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_status"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_header']

class AdviceMessageSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge message"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_message"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_message']

class AdviceScheduleSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge schedule"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_schedule"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_schedule']

class AdviceChargeLevelSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charge level"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_chargelevel"

    @property
    def device_class(self):
        return SensorDeviceClass.POWER_FACTOR
    
    @property
    def native_value(self):
        return (self.hass.data[DOMAIN]['advice_chargelevel'] * 100) / 3
        
    @property
    def native_unit_of_measurement(self):
        return "%"

class AdviceMaxkWh(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge max kWh"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_maxkwh"

    @property
    def device_class(self):
        return SensorDeviceClass.ENERGY_STORAGE
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['advice_maxkwh']
        
    @property
    def native_unit_of_measurement(self):
        return "kWh"

class ChargeIDSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charge ID"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_chargeid"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['charge_id']

class PowerSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge power"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_power"

    @property
    def device_class(self):
        return SensorDeviceClass.CURRENT
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['power']
        
    @property
    def native_unit_of_measurement(self):
        return "A"

class StartedSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charge started at"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_start"

    @property
    def device_class(self):
        return SensorDeviceClass.TIMESTAMP
    
    @property
    def native_value(self):
        if self.hass.data[DOMAIN]['started_ts'] is not None:
            return datetime.datetime.fromtimestamp(self.hass.data[DOMAIN]['started_ts']).astimezone()
        else:
            return None

class EnergySensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge energy"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_energy"

    @property
    def device_class(self):
        return SensorDeviceClass.ENERGY
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['energy']
        
    @property
    def native_unit_of_measurement(self):
        return "kWh"

class PowerReasonSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge power reason"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_reason"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['power_reason']


class TotalChargesSensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge total charges"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_totalcharges"
    
    @property
    def state_class(self):
        return "total"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['c_total']

class CurrentEnergySensor(SensorEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charge energy"
        
    def __init__(self, hass: HomeAssistant):
        serial = hass.data[DOMAIN]['unique_id']
        self._attr_unique_id = f"{DOMAIN}_{serial}_chargeenergy"

    @property
    def device_class(self):
        return SensorDeviceClass.ENERGY
    
    @property
    def native_value(self):
        return self.hass.data[DOMAIN]['c_energy']
        
    @property
    def native_unit_of_measurement(self):
        return "kWh"
    
    @property
    def state_class(self):
        return "total_increasing"
    
    def update(self):
        hc = homecharge.Client()
        if hc:
            self.hass.data[DOMAIN]['hc'] = hc
            try:
                apikey = hc.login(self.hass.data[DOMAIN]['user'], self.hass.data[DOMAIN]['pass'])
            except:
                return
            
            hc_charges = hc.get_charges()
            self.hass.data[DOMAIN]['c_total'] = hc_charges['total']
            hc_cur_charge = hc_charges['recharges'][0]

            if self.hass.data[DOMAIN]['charge_id'] is not None:                
                if hc_cur_charge['charge_id'] == self.hass.data[DOMAIN]['charge_id']:
                    self.hass.data[DOMAIN]['c_energy'] = hc_cur_charge['energy']
                else:
                    self.hass.data[DOMAIN]['c_energy'] = 0
            else: # get energy from most recent charge so we have an accurate total
                self.hass.data[DOMAIN]['c_energy'] = hc_cur_charge['energy']
