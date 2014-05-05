from django.conf.urls import patterns, url
from realestate.admin.views import Dashboard, CreateListing, UpdateListing, Listings, CreateAgent, Agents, Contacts, CreateContact, \
    UpdateAgent, UpdateContact, Cities, CreateCity, UpdateCity, Sectors, CreateSector, UpdateSector

urlpatterns = patterns(
    'realestate.admin.views',
    url('^$', Dashboard.as_view(), name='dashboard'),

    url('^listing/', Listings.as_view(), name='admin-list-listing'),
    url('^new-listing/', CreateListing.as_view(), name='add-listing'),
    url('^update-listing/(?P<pk>\d+)$', UpdateListing.as_view(), name='update-listing'),
    url('^agents/', Agents.as_view(), name='admin-list-agents'),
    url('^new-agent/', CreateAgent.as_view(), name='add-agent'),
    url('^update-agent/(?P<pk>\d+)$', UpdateAgent.as_view(), name='update-agent'),
    url('^contacts/', Contacts.as_view(), name='admin-list-contacts'),
    url('^new-contact/', CreateContact.as_view(), name='add-contact'),
    url('^update-contact/(?P<pk>\d+)$', UpdateContact.as_view(), name='update-contact'),
    url('^cities/', Cities.as_view(), name='admin-list-cities'),
    url('^new-city/', CreateCity.as_view(), name='add-city'),
    url('^update-city/(?P<pk>\d+)$', UpdateCity.as_view(), name='update-city'),
    url('^sectors/', Sectors.as_view(), name='admin-list-sectors'),
    url('^new-sector/', CreateSector.as_view(), name='add-sector'),
    url('^update-sector/(?P<pk>\d+)$', UpdateSector.as_view(), name='update-sector'),

)