from django.conf.urls import *
from django.conf import settings
from rest_framework import routers
from realestate.api import PropiedadViewSet
from realestate.urls import urlpatterns as realestate_patterns


router = routers.DefaultRouter()
router.register(r'api/propiedades', PropiedadViewSet)

urlpatterns = patterns(
    '',
    url('^', include(router.urls)),
) + realestate_patterns

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )