"""Support for Twente Milieu sensors."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER
from .entity import OdenseRenoEntity


@dataclass
class OdenseRenoSensorDescription(SensorEntityDescription):
    """Odense Reno sensor description"""

    key: str
    name: str
    icon: str = "mdi:delete-empty"
    device_class = SensorDeviceClass.DATE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = []
    for sensor in coordinator.data:
        sensors.append(
            OdenseRenoSensorDescription(
                key=sensor, name=f"{DOMAIN}_{entry.data[CONF_ADDRESS]}_{sensor}"
            )
        )

    async_add_entities(
        OdenseRenoSensor(coordinator, description, entry) for description in sensors
    )


class OdenseRenoSensor(OdenseRenoEntity, SensorEntity):
    """Representation of Odense Reno sensor."""

    entity_description: OdenseRenoSensorDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: OdenseRenoSensorDescription,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, entry)

        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{entry.data[CONF_ADDRESS]}_{description.key}"

    @property
    def native_value(self) -> date | None:
        return datetime.fromisoformat(
            self.coordinator.data[self.entity_description.key][0]
        ).date()

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["next_pickup"] = self.coordinator.data[self.entity_description.key][1:-1]
        return attrs
