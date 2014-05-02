from django.conf.urls import patterns, url
from realestate.admin.views import Dashboard, CreateListing, Listings, CreateAgent, Agents, Contacts, CreateContact

urlpatterns = patterns(
    'realestate.admin.views',
    url('^$', Dashboard.as_view(), name='dashboard'),

    url('^listing/', Listings.as_view(), name='admin-list-listing'),
    url('^new-listing/', CreateListing.as_view(), name='add-listing'),
    url('^agents/', Agents.as_view(), name='admin-list-agents'),
    url('^new-agent/', CreateAgent.as_view(), name='add-agent'),

    url('^contacts/', Contacts.as_view(), name='admin-list-contacts'),
    url('^new-contact/', CreateContact.as_view(), name='add-contact'),

)