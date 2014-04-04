from django.conf.urls import *
from django.conf import settings
from hitcount.views import update_hit_count_ajax
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

    (r'^admin/', include(admin.site.urls)),  # Enabling Admin

    (r'^tinymce/', include('tinymce.urls')),  #TinyMCE
    (r'^newsletter/', include('newsletter.urls')),  #django-newsletter

    #Ajax
    url(r'^mapa-propiedades/$', 'realestate.propiedad.views.get_mapa_propiedades', name='mapa-propiedades'),

    url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': {'propiedades': sitemap.PropiedadSitemap}}),

)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views', url(r'^static/(?P<path>.*)$', 'serve'), )