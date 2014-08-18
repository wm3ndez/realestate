from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
from django.views.generic import TemplateView
from realestate.listing import views  as listing_views
from rest_framework import routers
from home.views import ContactView, IndexView
from realestate.api import PropiedadViewSet
from realestate.listing import sitemap

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'propiedades', PropiedadViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^properties/$', listing_views.ListingList.as_view(), name='all_properties'),
    url(r'^sale/$', listing_views.ListingForSaleList.as_view(), name='properties_for_sale'),
    url(r'^sale/(?P<order_by>[\w-]+)/$', listing_views.ListingForSaleList.as_view(), name='properties_for_sale'),
    url(r'^rent/$', listing_views.ListingForRentList.as_view(), name='properties_for_rent'),
    url(r'^rent/(?P<order_by>[\w-]+)/$', listing_views.ListingForRentList.as_view(), name='properties_for_rent'),
    url(r'^search/', listing_views.SearchView.as_view(), name='search'),
    url(r'^listing/(?P<slug>[\w-]+)/', listing_views.ListingView.as_view(), name='property_details'),
    url(r'^agents/$', listing_views.AgentList.as_view(), name='agents'),
    url(r'^agents/listing/(?P<agent>[\d]+)/$', listing_views.AgentListing.as_view(), name='agent-listings'),
    url(r'^get_map/$', listing_views.MapView.as_view(), name='mapa-propiedades'),
    url(r'^contact/$', ContactView.as_view(), name='home_contact'),

    # Static Pages
    url(r'^about-us/$', TemplateView.as_view(template_name='home/about-us.html'), name='home_aboutus'),
    url(r'^services/$', TemplateView.as_view(template_name='home/services.html'), name='home_services'),
    url(r'^thank-you/$', TemplateView.as_view(template_name='home/thank-you.html'), name='thank-you'),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^api/', include(router.urls)),

    # Sitemaps
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'blog': sitemap.ListingSitemap}}),

    # Django apps
    (r'^dashboard/', include('realestate.admin.urls')),  # Custom Admin Site

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    (r'^admin/', include(admin.site.urls)),  # Enabling Admin
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
