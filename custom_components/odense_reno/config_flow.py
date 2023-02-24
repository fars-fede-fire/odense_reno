"""Config flow to configure the Odense Renovation integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol


from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_API_KEY, CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_validation import slugify

from .odense_reno import OdenseReno

from .const import DOMAIN


class OdenseRenoFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Odense Renovation config flow."""

    VERSION = 1

    async def _show_setup_form(
        self, errors: dict[str, str] | None = None
    ) -> FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors or {},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        session = async_get_clientsession(self.hass)

        odensereno = OdenseReno(
            address_no=user_input[CONF_API_KEY],
            session=session,
        )

        address = await odensereno.get_adress()

        await self.async_set_unique_id(str(slugify(address)))
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=str(address),
            data={
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_ADDRESS: str(slugify(address)),
            },
        )
