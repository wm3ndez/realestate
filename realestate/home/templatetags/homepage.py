from django.template import Library
from realestate.listing.models import Listing

register = Library()

#TODO: Move this templatetag to 'listing' app
@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    properties = Listing.objects.featured()[:limit]
    return {'listings': properties}