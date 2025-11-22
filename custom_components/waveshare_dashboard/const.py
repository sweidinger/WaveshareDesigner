"""
Constants for the Waveshare E-Paper Dashboard Designer integration.
"""

DOMAIN = "waveshare_dashboard"

# Storage
STORAGE_KEY = DOMAIN
STORAGE_VERSION = 1

# Display models and their dimensions
DISPLAY_MODELS = {
    "2.90in": {"width": 296, "height": 128, "model": "2.90in"},
    "4.20in": {"width": 400, "height": 300, "model": "4.20in"},
    "7.50in": {"width": 640, "height": 384, "model": "7.50in"},
    "7.50inV2": {"width": 800, "height": 480, "model": "7.50inV2"},
    "7.50in-bV3-bwr": {"width": 800, "height": 480, "model": "7.50in-bV3-bwr", "colors": ["black", "white", "red"]},
}

# Default display (7.5" V2 - most common)
DEFAULT_DISPLAY_MODEL = "7.50inV2"
IMAGE_WIDTH = 800  # Default, will be overridden by selected model
IMAGE_HEIGHT = 480  # Default, will be overridden by selected model

# Config keys
CONF_DEVICE_ID = "device_id"
CONF_DEVICE_NAME = "device_name"
CONF_API_TOKEN = "api_token"
CONF_PAGES = "pages"
CONF_DISPLAY_MODEL = "display_model"

# Service names
SERVICE_SET_PAGE = "set_page"
SERVICE_NEXT_PAGE = "next_page"
SERVICE_PREV_PAGE = "prev_page"

# HTTP API paths (joined with /api/)
API_BASE_PATH = f"/api/{DOMAIN}"
API_IMAGE_PATH = f"{API_BASE_PATH}" + "/{device_id}/page/{page_index}/image.png"
API_LAYOUT_PATH = f"{API_BASE_PATH}" + "/{device_id}/layout"
API_LAYOUT_PAGE_PATH = f"{API_BASE_PATH}" + "/{device_id}/page/{page_index}"

# Defaults
DEFAULT_PAGES = 3
MIN_PAGES = 1
MAX_PAGES = 8

# Security / tokens
# Per-device token length; tokens are generated and stored by the integration, not user-provided.
API_TOKEN_BYTES = 16