from django.template import Library
from realestate.propiedad.models import Propiedad

register = Library()


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimas_casas(limit=4):
    propiedades = Propiedad.objects.casas()[:limit]
    return {'propiedades': propiedades}


@register.inclusion_tag('home/homepage_listing.html')
def get_ultimos_apartamentos(limit=4):
    propiedades = Propiedad.objects.apartamentos()[:limit]
    return {'propiedades': propiedades}


@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    propiedades = Propiedad.objects.featured()[:limit]
    return {'propiedades': propiedades}