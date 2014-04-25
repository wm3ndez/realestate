from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
from realestate.listing import sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'realestate.home.views.index', name='index'),
    url(r'^properties/$', 'realestate.listing.views.properties', name='all_properties'),
    url(r'^sale/$', 'realestate.listing.views.sale', name='properties_for_sale'),
    url(r'^sale/(?P<type>\w+)/$', 'realestate.listing.views.sale', name='properties_for_sale'),
    url(r'^rent/$', 'realestate.listing.views.rent', name='properties_for_rent'),
    url(r'^rent/(?P<type>\w+)/$', 'realestate.listing.views.rent', name='properties_for_rent'),
    url(r'^search/', 'realestate.listing.views.search', name='search'),
    url(r'^listing/(?P<slug>[\w-]+)/', 'realestate.listing.views.details', name='property_details'),
    url(r'^about-us/$', 'realestate.home.views.about_us', name='home_aboutus'),
    url(r'^contact/$', 'realestate.home.views.contact', name='home_contact'),
    url(r'^services/$', 'realestate.home.views.services', name='home_services'),
    url(r'^write-us/$', 'realestate.home.views.write_us', name='home_write_us'),


    url(r'^listado_propiedades/$', 'realestate.listing.views.get_map', name='mapa-propiedades'),  # Ajax
    (r'^admin/', include(admin.site.urls)),  # Enabling Admin
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'blog': sitemap.ListingSitemap}}),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
