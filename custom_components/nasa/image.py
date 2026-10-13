"""Definition and setup of the Nasa Images for Home Assistant."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from homeassistant.components.image import ImageEntity, ImageEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NasaDataUpdateCoordinator
from .entity import NasaEntity

from datetime import datetime
from homeassistant.util import dt as dt_util

@dataclass(frozen=True, kw_only=True)
class NasaImageEntityDescription(ImageEntityDescription):
    """Describes Nasa image entity."""
    attr_fn: Callable[[dict[str, Any]], Mapping[str, Any] | None] = lambda data: None
    avabl_fn: Callable[[dict[str, Any]], bool] = lambda data: True

IMAGE_DESCRIPTIONS: tuple[NasaImageEntityDescription, ...] = (
    NasaImageEntityDescription(
        key="apod_image",
        name="APOD Image",
        icon="mdi:image",
        attr_fn=lambda data: data,
        avabl_fn=lambda data: data.get("media_type") == "image" and "hdurl" in data,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nasa images."""
    sourceapis: dict[str, NasaDataUpdateCoordinator] = hass.data[DOMAIN]

    async_add_entities(
        (
            NasaImageEntity(hass, coordinator, description)
            for description in IMAGE_DESCRIPTIONS
            for coordinator in sourceapis.values()
            if "APOD" in coordinator.name
        ),
    )

class NasaImageEntity(NasaEntity, ImageEntity):
    """Nasa image entity class."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: NasaDataUpdateCoordinator,
        entity_description: NasaImageEntityDescription,
    ) -> None:
        """Initialize Nasa image entity."""
        super().__init__(coordinator, entity_description)
        ImageEntity.__init__(self, hass)
        self.entity_description = entity_description

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self.entity_description.avabl_fn(self.coordinator.data)
        )

    @property
    def image_url(self) -> str | None:
        """Return URL of image."""
        if self.coordinator.data:
            return self.coordinator.data.get("hdurl")
        return None

    @property
    def image_last_updated(self) -> datetime | None:
        """The time when the image was last updated."""
        if self.coordinator.data:
            date_str = self.coordinator.data.get("date")
            if date_str:
                try:
                    return dt_util.parse_datetime(date_str) or datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt_util.UTC)
                except ValueError:
                    return None
        return None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the extra state attributes."""
        return self.entity_description.attr_fn(self.coordinator.data)
