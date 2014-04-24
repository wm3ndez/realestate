from django import template
from realestate.property.models import TYPES, PROVINCIAS, OFERTAS
from django.template.loader import get_template
from django.template import Context, TemplateDoesNotExist

from realestate.home.forms import SearchForm

register = template.Library()


def _render_drop_down(field_id, field_name, options):
    try:
        template = get_template('forms/drop_down.html')
    except TemplateDoesNotExist:
        return
    c = Context({
        'options': options,
        'field_id': field_id,
        'field_name': field_name,
    })
    return template.render(c)


@register.simple_tag
def render_property_type_select():
    options = [{'name': name, 'value': value} for value, name in TYPES]
    field_id = field_name = 'type'
    return _render_drop_down(field_id, field_name, options)


@register.simple_tag
def render_bath_qty_select():
    options = [{'name': i, 'value': i} for i in range(1, 6)]
    return _render_drop_down('busqueda_banos', 'busqueda_banos', options)


@register.simple_tag
def render_location_select():
    options = [{'name': name, 'value': value} for value, name in PROVINCIAS]
    return _render_drop_down('provincia', 'provincia', options)


@register.simple_tag
def render_offer_select():
    options = [{'name': name, 'value': value} for value, name in OFERTAS]
    return _render_drop_down('offer', 'offer', options)


@register.inclusion_tag('forms/search.html', takes_context=True)
def get_search_form(context):
    form = SearchForm(context['request'].GET)
    return {'form': form}


@register.inclusion_tag('forms/secondary_search.html', takes_context=True)
def get_secondary_search_form(context):
    form = SearchForm(context['request'].GET)
    return {'form': form}