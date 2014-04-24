from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
from realestate.property import sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'realestate.home.views.index', name='index'),
    url(r'^propiedades/$', 'realestate.property.views.propiedades', name='all_properties'),
    url(r'^venta/$', 'realestate.property.views.venta', name='properties_for_sale'),
    url(r'^venta/(?P<type>\w+)/$', 'realestate.property.views.venta', name='properties_for_sale'),
    url(r'^alquiler/$', 'realestate.property.views.alquiler', name='properties_for_rent'),
    url(r'^alquiler/(?P<type>\w+)/$', 'realestate.property.views.alquiler', name='properties_for_rent'),
    url(r'^busqueda/', 'realestate.property.views.search', name='search'),
    url(r'^property/(?P<slug>[\w-]+)/', 'realestate.property.views.details', name='property_details'),
    url(r'^nosotros/$', 'realestate.home.views.nosotros', name='home_aboutus'),
    url(r'^contacto/$', 'realestate.home.views.contacto', name='home_contact'),
    url(r'^servicios/$', 'realestate.home.views.servicios', name='home_services'),
    url(r'^escribenos/$', 'realestate.home.views.escribenos', name='home_escribenos'),


    url(r'^listado_propiedades/$', 'realestate.property.views.get_mapa_propiedades', name='mapa-propiedades'),  # Ajax
    (r'^admin/', include(admin.site.urls)),  # Enabling Admin
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'blog': sitemap.PropiedadSitemap}}),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
