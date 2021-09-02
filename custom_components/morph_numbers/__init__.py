from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.helpers.template import _ENVIRONMENT, TemplateEnvironment
from jinja2.filters import do_format

from .utils import MorphNumber

DOMAIN = 'morph_numbers'

MORPH = MorphNumber()


# noinspection PyUnusedLocal
async def async_setup(hass, hass_config):
    if DOMAIN in hass_config and not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}
        ))
    return True


async def async_setup_entry(hass, entry):
    if _ENVIRONMENT not in hass.data:
        hass.data[_ENVIRONMENT] = TemplateEnvironment(hass)

    # use an existing filter so as not to get an initialization error
    hass.data[_ENVIRONMENT].filters['format'] = morph_format

    return True


async def async_unload_entry(hass, entry):
    hass.data[_ENVIRONMENT].filters['format'] = do_format
    return True


def morph_format(value, *args, **kwargs):
    if 'morph' in kwargs:
        if kwargs.get('as_ordinal'):
            return MORPH.ordinal_number(value, kwargs['morph'])

        as_text = kwargs.get('as_text', True)

        if isinstance(kwargs['morph'], list):
            return MORPH.custom_numword(value, kwargs['morph'], as_text)

        return MORPH.numword(value, kwargs['morph'], as_text)

    else:
        return do_format(value, *args, **kwargs)
