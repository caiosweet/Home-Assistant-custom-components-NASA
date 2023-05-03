"""Definition and setup of the Nasa Sensors for Home Assistant."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    # SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import NasaDataUpdateCoordinator
from .entity import NasaEntity


@dataclass
class BaseEntityDescriptionMixin:
    """Mixin for required Nasa base description keys."""

    value_fn: Callable[[dict[str, Any]], StateType]


@dataclass
class BaseEntityDescription(SensorEntityDescription):
    """Describes Nasa sensor entity default overrides."""

    icon: str = "mdi:rocket"
    attr_fn: Callable[[dict[str, Any]], Mapping[str, Any] | None] = lambda data: None
    avabl_fn: Callable[[dict[str, Any]], bool] = lambda data: True


@dataclass
class NasaSensorEntityDescription(BaseEntityDescription, BaseEntityDescriptionMixin):
    """Describes Nasa issue sensor entity."""


SENSOR_DESCRIPTIONS: tuple[NasaSensorEntityDescription, ...] = (
    NasaSensorEntityDescription(
        key="apod",
        name="APOD",
        icon="mdi:image",
        # native_unit_of_measurement="Apod",
        entity_category=EntityCategory.DIAGNOSTIC,
        # state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["title"],
        attr_fn=lambda data: data,
    ),
    NasaSensorEntityDescription(
        key="epic",
        name="EPIC",
        icon="mdi:earth",
        # state_class=SensorStateClass.MEASUREMENT,
        # avabl_fn=lambda data: data["date"],
        value_fn=lambda data: data["last_date"],
        attr_fn=lambda data: data,
    ),
    NasaSensorEntityDescription(
        entity_registry_enabled_default=False,
        key="insight",
        name="InSight",
        icon="mdi:sun-compass",
        # state_class=SensorStateClass.MEASUREMENT,
        avabl_fn=lambda data: data["sol_keys"],
        value_fn=lambda data: data["sol_keys"][-1],
        attr_fn=lambda data: data[data["sol_keys"][-1]],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nasa sensors."""
    sourceapis: dict[str, NasaDataUpdateCoordinator] = hass.data[DOMAIN]

    async_add_entities(
        (
            NasaSensorEntity(coordinator, description)
            for description in SENSOR_DESCRIPTIONS
            for coordinator in sourceapis.values()
            if coordinator.name in description.name
        ),
    )


class NasaSensorEntity(NasaEntity, SensorEntity):
    """Nasa sensor entity class."""

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self.entity_description.avabl_fn(self.coordinator.data)
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the extra state attributes."""
        return self.entity_description.attr_fn(self.coordinator.data)
