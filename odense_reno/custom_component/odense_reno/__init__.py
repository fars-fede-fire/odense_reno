"""
Custom integration to integrate odense_reno with Home Assistant.

For more details about this integration, please refer to
https://github.com/fars-fede-fire/odense_reno
"""
from __future__ import annotations

from datetime import date, timedelta


import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .odense_reno import OdenseReno

from .const import DOMAIN, LOGGER

SCAN_INTERVAL = timedelta(hours=3)

SERVICE_UPDATE = "update"

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Odense Renovation from a config entry."""
    session = async_get_clientsession(hass)
    odensereno = OdenseReno(
        address_no=entry.data[CONF_API_KEY],
        session=session,
    )

    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=DOMAIN,
        update_interval=SCAN_INTERVAL,
        update_method=odensereno.get_pickup_dates,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "odense_reno": odense_reno,
    }
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Odense Renovation config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN][entry.entry_id]
    return unload_ok
