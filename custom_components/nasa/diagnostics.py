"""Provides diagnostics for dpc."""
from __future__ import annotations

from typing import Any

from aionasa import APOD
from aionasa.errors import APIException
from attr import asdict
import requests

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_API_CATEGORY, DOMAIN
from .coordinator import NasaDataUpdateCoordinator

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    def _rate_limit(api_key):
        headers = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}").headers
        return int(headers["X-RateLimit-Remaining"])

    data = {"options": {**config_entry.options}}
    api_key = config_entry.data.get(CONF_API_KEY, "DEMO_KEY")
    client = APOD(
        session=async_get_clientsession(hass),
        api_key=api_key,
    )
    try:
        response = await client.get()
    except APIException as err:
        data["rate_limit"] = {"error": str(err)}
    else:
        data["read_chunk"] = await response.read_chunk(1000000)
        data["rate_limit"] = await hass.async_add_executor_job(_rate_limit, api_key)

    sourceapis: dict[str, NasaDataUpdateCoordinator] = hass.data[DOMAIN]
    data[CONF_API_CATEGORY] = {}

    for sourceapi, coordinator in sourceapis.items():
        data[CONF_API_CATEGORY][sourceapi] = coordinator.data

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    devices = []

    registry_devices = dr.async_entries_for_config_entry(device_registry, config_entry.entry_id)

    for device in registry_devices:
        entities = []

        registry_entities = er.async_entries_for_device(
            entity_registry,
            device_id=device.id,
            include_disabled_entities=True,
        )

        for entity in registry_entities:
            state_dict = None
            if state := hass.states.get(entity.entity_id):
                state_dict = dict(state.as_dict())
                state_dict.pop("context", None)

            entities.append({"entry": asdict(entity), "state": state_dict})

        devices.append({"device": asdict(device), "entities": entities})
    data["devices"] = devices

    return async_redact_data(data, TO_REDACT)
