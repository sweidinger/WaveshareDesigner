"""
Config flow for the Waveshare E-Paper Dashboard Designer integration.

Goals:
- Simple setup: each config entry represents enabling the dashboard designer.
- Devices (Waveshare displays) are managed via storage and the editor, not via YAML.
- For each new device, we generate:
  - device_id
  - api_token
  - display_model
  and store it in DashboardStorage.

This flow:
- Creates a single config entry (no per-device duplicates needed initially).
- Provides the base URL hint for ESPHome (using the HA external/internal URL the user configures).
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
import os
import secrets
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback, HomeAssistant

from .const import (
    DOMAIN,
    API_BASE_PATH,
    API_TOKEN_BYTES,
    DISPLAY_MODELS,
    DEFAULT_DISPLAY_MODEL,
    CONF_DISPLAY_MODEL,
)
from .storage import DashboardStorage

_LOGGER = logging.getLogger(__name__)


@dataclass
class FlowContext:
    """Hold temporary flow context."""
    entry_title: str = "Waveshare E-Paper Dashboard Designer"
    display_model: str = DEFAULT_DISPLAY_MODEL


async def _get_storage(hass: HomeAssistant) -> DashboardStorage:
    """Helper to obtain storage initialized in __init__."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    storage: DashboardStorage | None = domain_data.get("storage")
    if storage is None:
        from .storage import DashboardStorage as DS

        storage = DS(hass=hass)
        await storage.async_load()
        domain_data["storage"] = storage
    return storage


class WaveshareDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waveshare E-Paper Dashboard Designer."""

    VERSION = 1

    def __init__(self) -> None:
        self.flow_ctx = FlowContext()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return WaveshareDashboardOptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Initial step: create the integration entry."""
        errors: dict[str, str] = {}

        # Prevent multiple entries; one global integration is sufficient.
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            name = user_input.get(CONF_NAME) or self.flow_ctx.entry_title
            display_model = user_input.get(CONF_DISPLAY_MODEL) or DEFAULT_DISPLAY_MODEL
            self.flow_ctx.entry_title = name
            self.flow_ctx.display_model = display_model
            _LOGGER.debug("%s: Creating config entry with title=%s, model=%s", DOMAIN, name, display_model)
            return self.async_create_entry(
                title=name, 
                data={CONF_DISPLAY_MODEL: display_model}
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=self.flow_ctx.entry_title): str,
                vol.Required(CONF_DISPLAY_MODEL, default=DEFAULT_DISPLAY_MODEL): vol.In(list(DISPLAY_MODELS.keys())),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )


class WaveshareDashboardOptionsFlow(config_entries.OptionsFlow):
    """Options flow: provide device URL hints and simple UX info."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        super().__init__()
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Show read-only info useful for configuring ESPHome and devices."""
        # Options are currently informational; no changes stored here.
        # The editor and HTTP API manage actual layouts/devices.

        hass = self.hass  # type: ignore[attr-defined]
        storage = await _get_storage(hass)

        # Try to detect a base URL hint for the user.
        # Fallback to host header usage; actual deployments might set `external_url`.
        base_url = (
            (getattr(hass.config, "external_url", None) or "")
            or (getattr(hass.config, "internal_url", None) or "")
        )
        if not base_url:
            # Fallback that user can adapt.
            base_url = "http://homeassistant.local:8123"

        api_base = f"{base_url}{API_BASE_PATH}"
        dashboard_url = f"{base_url}/waveshare-dashboard"

        # Get display model from config entry
        display_model = self._config_entry.data.get(CONF_DISPLAY_MODEL, DEFAULT_DISPLAY_MODEL)
        
        # Provide a textual summary; options dict not used to drive logic yet.
        info_text = (
            f"🎨 Dashboard Editor: {dashboard_url}\n\n"
            f"Waveshare E-Paper Dashboard Designer is configured.\n\n"
            f"Display Model: {display_model}\n\n"
            "Use the following pattern in your ESPHome firmware:\n"
            f"  online_image URL: {api_base}" + "/{device_id}/page/{page}/image.png?token={api_token}\n\n"
            "Devices and layouts are managed via the dashboard editor and HTTP API."
        )

        if user_input is not None:
            # Nothing to store yet; just close.
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional("info", default=info_text): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={
                "dashboard_url": dashboard_url,
            },
        )