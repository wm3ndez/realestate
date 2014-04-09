from django import template
from realestate.propiedad.models import Propiedad


register = template.Library()

@register.simple_tag
def listado_features(propiedad):
    features = propiedad.get_features()
    html = '<div class="span2"><ul>'
    for index in range(0, len(features)):
        if index % 3 == 0 and index:
            html += '</ul></div><div class="span2"><ul>'
        html += '<li>%s</li>' % features[index]

    html += '</ul></div>'
    return  html


@register.inclusion_tag('home/carousel.html')
def frontpage_carousel():
    propiedades = Propiedad.objects.activas().order_by('-id')[:4]
    return {
        'propiedades': propiedades
    }
