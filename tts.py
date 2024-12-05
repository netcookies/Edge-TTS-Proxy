import logging
import aiohttp
import voluptuous as vol
from homeassistant.components.tts import TextToSpeechEntity, CONF_LANG, ATTR_VOICE, Provider
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry
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
)

_LOGGER = logging.getLogger(__name__)


async def async_get_engine(hass, entry: ConfigEntry):
    """Set up the TTS provider from config entry."""
    return EdgeTTSProxyEntity(hass, entry)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up the TTS platform from a config entry."""
    # 初始化 TTS 提供器实例
    provider = await async_get_engine(hass, entry)
    if provider is None:
        _LOGGER.error("Failed to initialize the TTS provider")
        return

    # 只注册为 TTS 服务，而不是实体
    async_add_entities([provider])
    #hass.data[DOMAIN][entry.entry_id] = provider

    return True

class EdgeTTSProxyEntity(TextToSpeechEntity):
    """The Entity."""

    def __init__(self, hass, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._config = entry.data
        self._attr_name = f"{NAME} Entity"
        self._attr_unique_id = entry.entry_id
        self._prosody_options = ['pitch', 'rate', 'volume']
        _LOGGER.debug("Initializing Edge TTS provider with config: %s", self._config)

    @property
    def default_language(self):
        return self._config.get(CONF_LANG, DEFAULT_LANG)

    @property
    def supported_languages(self):
        return list([*SUPPORTED_LANGUAGES.keys(), *SUPPORTED_VOICES.keys()])

    @property
    def supported_options(self):
        return [CONF_LANG, ATTR_VOICE] + self._prosody_options

    def supported_formats(self):
        return list(SUPPORTED_FORMATS.keys())

    async def async_get_tts_audio(self, message, language, options=None):
        opt = dict(self._config)
        if language in SUPPORTED_VOICES:
            opt[CONF_LANG] = SUPPORTED_VOICES[language]
            opt[ATTR_VOICE] = language

        if options:
            opt.update(options)

        params = {
            'text': message,
            'voiceName': opt.get(ATTR_VOICE) or SUPPORTED_LANGUAGES.get(opt[CONF_LANG]) or DEFAULT_VOICE,
            'format': opt.get('format', DEFAULT_FORMAT),
        }

        if opt.get(CONF_API_TOKEN):
            params['token'] = opt[CONF_API_TOKEN]

        for key in self._prosody_options:
            if key in opt:
                params[key] = opt[key]

        api_url = opt.get(CONF_API_URL)
        if not api_url:
            _LOGGER.error("Missing api_url configuration")
            return None, None

        if not api_url.endswith('/'):
            api_url += '/'

        # 使用 ENDPOINT 替换硬编码的 URL 部分
        full_url = f"{api_url}{ENDPOINT}"

        _LOGGER.debug("Making request to URL: %s with params: %s", full_url, params)
        filtered_params = {k: v for k, v in params.items() if v is not None}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(full_url, params=filtered_params) as response:
                    if response.status != 200:
                        _LOGGER.error("API request failed with status %s", response.status)
                        return None, None
                    return SUPPORTED_FORMATS.get(opt.get('format', DEFAULT_FORMAT), 'mp3'), await response.read()
        except Exception as err:
            _LOGGER.error("Failed to fetch TTS audio: %s", err)
            return None, None


class EdgeTTSProxyProvider(Provider):
    """The provider."""

    def __init__(self, hass, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._config = entry.data
        self.name = NAME
        self._prosody_options = ['pitch', 'rate', 'volume']
        _LOGGER.debug("Initializing Edge TTS provider with config: %s", self._config)

    @property
    def default_language(self):
        return self._config.get(CONF_LANG, DEFAULT_LANG)

    @property
    def supported_languages(self):
        return list([*SUPPORTED_LANGUAGES.keys(), *SUPPORTED_VOICES.keys()])

    @property
    def supported_options(self):
        return [CONF_LANG, ATTR_VOICE] + self._prosody_options

    def supported_formats(self):
        return list(SUPPORTED_FORMATS.keys())

    async def async_get_tts_audio(self, message, language, options=None):
        opt = dict(self._config)
        if language in SUPPORTED_VOICES:
            opt[CONF_LANG] = SUPPORTED_VOICES[language]
            opt[ATTR_VOICE] = language

        if options:
            opt.update(options)

        params = {
            'text': message,
            'voiceName': opt.get(ATTR_VOICE) or SUPPORTED_LANGUAGES.get(opt[CONF_LANG]) or DEFAULT_VOICE,
            'format': opt.get('format', DEFAULT_FORMAT),
        }

        if opt.get(CONF_API_TOKEN):
            params['token'] = opt[CONF_API_TOKEN]

        for key in self._prosody_options:
            if key in opt:
                params[key] = opt[key]

        api_url = opt.get(CONF_API_URL)
        if not api_url:
            _LOGGER.error("Missing api_url configuration")
            return None, None

        if not api_url.endswith('/'):
            api_url += '/'

        # 使用 ENDPOINT 替换硬编码的 URL 部分
        full_url = f"{api_url}{ENDPOINT}"

        _LOGGER.debug("Making request to URL: %s with params: %s", full_url, params)
        filtered_params = {k: v for k, v in params.items() if v is not None}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(full_url, params=filtered_params) as response:
                    if response.status != 200:
                        _LOGGER.error("API request failed with status %s", response.status)
                        return None, None
                    return SUPPORTED_FORMATS.get(opt.get('format', DEFAULT_FORMAT), 'mp3'), await response.read()
        except Exception as err:
            _LOGGER.error("Failed to fetch TTS audio: %s", err)
            return None, None

