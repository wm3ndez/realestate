from django.contrib.sitemaps import Sitemap
from realestate.property.models import Propiedad

class PropiedadSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Propiedad.objects.all()

    def lastmod(self, obj):
        return obj.creacion