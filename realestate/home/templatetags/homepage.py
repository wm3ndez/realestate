from django.template import Library
from realestate.property.models import Property

register = Library()


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimas_casas(limit=4):
    properties = Property.objects.casas()[:limit]
    return {'properties': properties}


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimos_apartamentos(limit=4):
    properties = Property.objects.apartamentos()[:limit]
    return {'properties': properties}


@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    properties = Property.objects.featured()[:limit]
    return {'properties': properties}