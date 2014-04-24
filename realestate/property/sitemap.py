from django.contrib.sitemaps import Sitemap
from realestate.property.models import Property


class PropiedadSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Property.objects.all()

    def lastmod(self, obj):
        return obj.creacion