from django import template
from realestate.listing.models import Listing


register = template.Library()


@register.simple_tag
def feature_list(listing):
    try:
        features = listing.get_features()
    except:
        return ''
    html = '<div class="span2"><ul>'
    for index in range(0, len(features)):
        if index % 3 == 0 and index:
            html += '</ul></div><div class="span2"><ul>'
        html += '<li>%s</li>' % features[index]

    html += '</ul></div>'
    return html


@register.inclusion_tag('home/carousel.html')
def frontpage_carousel():
    listings = Listing.objects.active().order_by('-id')[:4]
    return {
        'listings': listings
    }
