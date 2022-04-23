"""Constants for the Nasa integration."""
from __future__ import annotations

from logging import Logger, getLogger
from typing import Final

from homeassistant.const import Platform

from .version import __version__

DOMAIN: Final = "nasa"
LOGGER: Final[Logger] = getLogger(__package__)
PLATFORMS: Final[list[Platform]] = [Platform.SENSOR]

NAME: Final = "NASA APIs"
VERSION: Final = __version__
ISSUE_URL: Final = "https://github.com/caiosweet/Home-Assistant-custom-components-NASA/issues"

API_CATEGORY: Final[list] = ["APOD", "InSight", "EPIC", "NeoWs", "Exoplanet"]
CONF_API_CATEGORY: Final = "api_category"

DEFAULT_SCAN_INTERVAL: Final[int] = 120

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
