from django.template import Library
from realestate.listing.models import Listing

register = Library()


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimas_casas(limit=4):
    properties = Listing.objects.casas()[:limit]
    return {'properties': properties}


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimos_apartamentos(limit=4):
    properties = Listing.objects.apartamentos()[:limit]
    return {'properties': properties}


@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    properties = Listing.objects.featured()[:limit]
    return {'listings': properties}