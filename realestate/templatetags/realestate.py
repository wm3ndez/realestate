from django import template
from property.models import Propiedad
from newsletter.models import Newsletter


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
#    import ipdb; ipdb.set_trace()
    return {
        'propiedades': propiedades
    }

@register.inclusion_tag('forms/newsletter_header_form.html')
def get_newsletter_form():
    """
     Newsletter Form
    """
    try:
        newsletter = Newsletter.objects.get(slug='ultimas-noticias')
        subscribe_url = newsletter.subscribe_url()
    except Newsletter.DoesNotExist:
        subscribe_url = '/'

    return {
        'subscribe_url':subscribe_url,

    }

