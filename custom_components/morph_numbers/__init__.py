from homeassistant.helpers.template import _ENVIRONMENT, TemplateEnvironment
from jinja2.filters import do_format

from . import utils


def morph_format(value, *args, **kwargs):
    if 'morph' in kwargs:
        as_text = kwargs.get('as_text', True)
        return utils.numword(value, kwargs['morph'], as_text)
    else:
        return do_format(value, *args, **kwargs)


# noinspection PyUnusedLocal
async def async_setup(hass, hass_config):
    if _ENVIRONMENT not in hass.data:
        hass.data[_ENVIRONMENT] = TemplateEnvironment(hass)

    # используем уже существующий фильтр, чтоб не нарваться на ошибку
    # инициализации
    hass.data[_ENVIRONMENT].filters['format'] = morph_format

    return True
