"""Base entity for the Odense Renovation integration."""
from __future__ import annotations

from datetime import date


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


class OdenseRenoEntity(CoordinatorEntity[DataUpdateCoordinator], Entity):
    """Defines a Odense Renovation entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Odense Renovation entity."""
        super().__init__(coordinator=coordinator)
        self._attr_device_info = DeviceInfo(
            configuration_url="https://mit.odenserenovation.dk/hentkalender",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, str(entry.data[CONF_API_KEY]))},
            manufacturer="Odense Renovation",
            name="Odense Renovation",

        )
