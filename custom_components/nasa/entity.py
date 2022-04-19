"""Common entity class for Nasa integration."""

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, VERSION
from .coordinator import NasaDataUpdateCoordinator


class NasaEntity(CoordinatorEntity[NasaDataUpdateCoordinator]):
    """Common entity class for Nasa integration."""

    _attr_attribution = "Data provided by Nasa"

    def __init__(
        self,
        coordinator: NasaDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize Nasa entities."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.name}_{entity_description.key}"
        self._attr_name = f"{DOMAIN.title()} {entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.name)},
            name=coordinator.name,
            manufacturer="NASA",
            model="Nasa APIs",
            suggested_area="Space",
            sw_version=VERSION,
            entry_type=DeviceEntryType.SERVICE,
        )
