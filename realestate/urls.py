from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
from realestate.propiedad import sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'realestate.home.views.index', name='index'),
    url(r'^propiedades/$', 'realestate.propiedad.views.propiedades', name='all_properties'),
    url(r'^venta/$', 'realestate.propiedad.views.venta', name='properties_for_sale'),
    url(r'^venta/(?P<tipo>\w+)/$', 'realestate.propiedad.views.venta', name='properties_for_sale'),
    url(r'^alquiler/$', 'realestate.propiedad.views.alquiler', name='properties_for_rent'),
    url(r'^alquiler/(?P<tipo>\w+)/$', 'realestate.propiedad.views.alquiler', name='properties_for_rent'),
    url(r'^busqueda/', 'realestate.propiedad.views.search', name='search'),
    url(r'^propiedad/(?P<slug>[\w-]+)/', 'realestate.propiedad.views.details', name='propiedad_details'),
    url(r'^nosotros/$', 'realestate.home.views.nosotros', name='home_aboutus'),
    url(r'^contacto/$', 'realestate.home.views.contacto', name='home_contact'),
    url(r'^servicios/$', 'realestate.home.views.servicios', name='home_services'),
    url(r'^escribenos/$', 'realestate.home.views.escribenos', name='home_escribenos'),


    url(r'^listado_propiedades/$', 'realestate.propiedad.views.get_mapa_propiedades', name='mapa-propiedades'),  # Ajax
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
