from django.core.urlresolvers import reverse
from realestate.home.models import News, Links
from django import template
from realestate.property.models import Especial, TIPO_PROPIEDADES

register = template.Library()

@register.inclusion_tag('widgets/news.html')
def news_widget():
    news = News.objects.filter(active=True)[:5]
    return {'news': news}


@register.inclusion_tag('widgets/links.html')
def links_widget():
    links = Links.objects.filter(active=True)[:5]
    return {'links': links}


@register.inclusion_tag('widgets/deals.html')
def deals_widget():
    deals = Especial.objects.filter(estado='activa')[:2]
    return {'deals': deals}
