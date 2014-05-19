from django import template
from realestate.listing.forms import SearchForm

register = template.Library()


@register.inclusion_tag('forms/search.html', takes_context=True)
def get_search_form(context):
    form = SearchForm(context['request'].GET)
    return {'form': form}