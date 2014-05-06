from django import template
from realestate.listing.models import OnSale

register = template.Library()


@register.inclusion_tag('widgets/deals.html')
def deals_widget():
    deals = OnSale.objects.filter(status='activa')[:2]
    return {'deals': deals}
