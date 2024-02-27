from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities([OverrideButton()])

class OverrideButton(ButtonEntity):
    _attr_has_entity_name = True

    @property
    def name(self):
        return "Homecharge charge now"

    def press(self) -> None:
        hc = self.hass.data[DOMAIN]['hc']
        hc.override()
