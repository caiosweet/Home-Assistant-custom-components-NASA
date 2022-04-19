"""Data update coordinator for Nasa entities."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from aionasa.errors import APIException

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER


class NasaDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Data update coordinator for Nasa integration."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api: object,
        name: str,
        update_interval: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=name,
            update_interval=timedelta(minutes=update_interval),
        )

        self.api = api
        self.data = {}

    async def _async_update_data(self) -> None:
        """Update Nasa data."""
        response = {}
        try:
            if "APOD" in self.name:
                response = await self.api.get(as_json=True)

            elif "InSight" in self.name:
                response = await self.api.get()

            elif "EPIC" in self.name:
                images = await self.api.natural_images()
                for i, image in enumerate(images):
                    response[f"date_{i}"] = image.date
                    response[f"url_{i}"] = image.png_url
                response[f"last_date"] = images[-1].date
                # response = images.json

        except APIException as exception:
            raise UpdateFailed(exception) from exception
        except ValueError as exception:
            LOGGER.exception(exception)
            raise UpdateFailed(exception) from exception
        else:
            return response
