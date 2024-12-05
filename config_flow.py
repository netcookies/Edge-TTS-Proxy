import logging
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.components.tts import ATTR_VOICE
from .const import (
    NAME,
    DOMAIN,
    CONF_API_URL,
    CONF_API_TOKEN,
    ENDPOINT,
    DEFAULT_LANG,
    DEFAULT_VOICE,
    DEFAULT_FORMAT,
    SUPPORTED_VOICES,
    SUPPORTED_LANGUAGES,
    SUPPORTED_FORMATS,
    PITCH_VALUES,
    RATE_VALUES,
    VOLUME_VALUES,
)

_LOGGER = logging.getLogger(__name__)

class EdgeTTSProxyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EdgeTTSProxyEntity."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        if user_input is not None:
            # Validate the user input and create config entry
            return self.async_create_entry(
                title=NAME,
                data=user_input
            )

        # Show the configuration form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
            errors={}
        )

    def _get_data_schema(self):
        """Return the schema for user input."""
        return vol.Schema({
            vol.Required(CONF_API_URL): str,
            vol.Optional(CONF_API_TOKEN, default=""): str,
            vol.Optional(ATTR_VOICE, default=DEFAULT_VOICE):
                vol.In(list(SUPPORTED_VOICES.keys())),
            vol.Optional("format", default=DEFAULT_FORMAT): 
                vol.In(list(SUPPORTED_FORMATS.keys())),
            vol.Optional("pitch", default="medium"): 
                vol.In(list(PITCH_VALUES.keys())),
            vol.Optional("rate", default="medium"):
                vol.In(list(RATE_VALUES.keys())),
            vol.Optional("volume", default="x-loud"):
                vol.In(list(VOLUME_VALUES.keys())),
        }) 
