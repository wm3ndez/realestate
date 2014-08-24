from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from realestate.listing.models import Listing

register = template.Library()


@register.filter
def currency(dollars):
    try:
        dollars = float(dollars)
    except (ValueError, TypeError):
        return '$0'
    return "$%s" % intcomma(int(dollars), False)


@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    properties = Listing.objects.featured()[:limit]
    return {'listings': properties}