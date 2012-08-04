from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'holguinmatos.home.views.index', name='index'),
    url(r'^propiedades/$', 'holguinmatos.property.views.propiedades', name='all_properties'),
    url(r'^venta/$', 'holguinmatos.property.views.venta', name='properties_for_sale'),
    url(r'^venta/(?P<tipo>\w+)/$', 'holguinmatos.property.views.venta', name='properties_for_sale'),
    url(r'^renta/$', 'holguinmatos.property.views.renta', name='properties_for_rent'),
    url(r'^renta/(?P<tipo>\w+)/$', 'holguinmatos.property.views.renta', name='properties_for_rent'),
    url(r'^busqueda/', 'holguinmatos.property.views.search', name='search'),
    url(r'^propiedad/(?P<slug>[\w-]+)/', 'holguinmatos.property.views.details', name='property_details'),
    url(r'^nosotros/$', 'holguinmatos.home.views.nosotros', name='home_aboutus'),
    url(r'^contacto/$', 'holguinmatos.home.views.contacto', name='home_contact'),
    url(r'^servicios/$', 'holguinmatos.home.views.servicios', name='home_services'),
    url(r'^escribenos/$', 'holguinmatos.home.views.escribenos', name='home_escribenos'),
    (r'^admin/', include(admin.site.urls)), # Enabling Admin
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
