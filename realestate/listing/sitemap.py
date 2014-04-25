from django.contrib.sitemaps import Sitemap
from realestate.listing.models import Listing


class ListingSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Listing.objects.active()

    def lastmod(self, obj):
        return obj.last_modified