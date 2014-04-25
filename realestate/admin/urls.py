from django.conf.urls import patterns, url
from realestate.admin.views import Dashboard, CreateListing, Listings

urlpatterns = patterns(
    'realestate.admin.views',
    url('^$', Dashboard.as_view(), name='dashboard'),

    url('^new-listing/', CreateListing.as_view(), name='add-listing'),
    url('^listing/', Listings.as_view(), name='admin-list-listing'),

)