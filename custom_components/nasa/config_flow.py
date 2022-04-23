"""Config flow for Nasa."""
from __future__ import annotations

from typing import Any

from aionasa import APOD
from aionasa.errors import APIException
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import (
    API_CATEGORY,
    CONF_API_CATEGORY,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    LOGGER,
)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Optional(CONF_API_KEY): str})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nasa."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def _validate_input(self, data) -> None:
        """Validate the user input allows us to connect."""

        api_key = data.get(CONF_API_KEY)
        session = async_get_clientsession(self.hass)

        try:
            if api_key is not None:
                api = APOD(api_key=api_key, session=session)
                return await api.get(as_json=True)

        except APIException as error:
            raise InputValidationError("invalid_api_key") from error
        except OSError as error:
            raise InputValidationError("invalid_api_key") from error

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            try:
                await self._validate_input(user_input)
            except InputValidationError as error:
                errors["base"] = error.base
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            if not errors:
                return self.async_create_entry(title=DOMAIN.title(), data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Nasa."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.options = config_entry.options
        self.data = config_entry.data

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle options flow."""
        if not user_input:
            configured_api_category: list[str] = self.options.get(CONF_API_CATEGORY, [])

            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_API_CATEGORY,
                            default=configured_api_category,
                        ): cv.multi_select({k: k for k in API_CATEGORY}),
                        vol.Optional(
                            CONF_SCAN_INTERVAL,
                            default=self.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                        ): cv.positive_int,
                    }
                ),
            )
        LOGGER.debug("User input CONFIG OPTION: %s", user_input)
        return self.async_create_entry(title="", data=user_input)


class InputValidationError(exceptions.HomeAssistantError):
    """Error to indicate we cannot proceed due to invalid input."""

    def __init__(self, base: str) -> None:
        """Initialize with error base."""
        super().__init__()
        self.base = base
