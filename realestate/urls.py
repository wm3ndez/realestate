from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'realestate.home.views.index', name='index'),
    url(r'^propiedades/$', 'realestate.property.views.propiedades', name='all_properties'),
    url(r'^venta/$', 'realestate.property.views.venta', name='properties_for_sale'),
    url(r'^venta/(?P<tipo>\w+)/$', 'realestate.property.views.venta', name='properties_for_sale'),
    url(r'^alquiler/$', 'realestate.property.views.alquiler', name='properties_for_rent'),
    url(r'^alquiler/(?P<tipo>\w+)/$', 'realestate.property.views.alquiler', name='properties_for_rent'),
    url(r'^busqueda/', 'realestate.property.views.search', name='search'),
    url(r'^propiedad/(?P<slug>[\w-]+)/', 'realestate.property.views.details', name='property_details'),
    url(r'^nosotros/$', 'realestate.home.views.nosotros', name='home_aboutus'),
    url(r'^contacto/$', 'realestate.home.views.contacto', name='home_contact'),
    url(r'^servicios/$', 'realestate.home.views.servicios', name='home_services'),
    url(r'^escribenos/$', 'realestate.home.views.escribenos', name='home_escribenos'),
    (r'^admin/', include(admin.site.urls)), # Enabling Admin
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
