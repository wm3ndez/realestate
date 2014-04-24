from realestate.home.models import News, Links
from django import template
from realestate.property.models import OnSale

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
    deals = OnSale.objects.filter(status='activa')[:2]
    return {'deals': deals}
