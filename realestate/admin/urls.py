from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from realestate.admin.views import Dashboard, CreateListing, UpdateListing, Listings, CreateAgent, Agents, Contacts, \
    CreateContact, \
    UpdateAgent, UpdateContact, Cities, CreateCity, UpdateCity, Sectors, CreateSector, UpdateSector, Settings, Users, \
    CreateUser, UpdateUser, SetUserPassword, Deals, CreateDeal, UpdateDeal

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
    url('^users/', Users.as_view(), name='admin-list-users'),
    url('^new-user/', CreateUser.as_view(), name='add-user'),
    url('^update-user/(?P<pk>\d+)$', UpdateUser.as_view(), name='update-user'),
    url('^set-user-password/(?P<user_id>\d+)$', SetUserPassword.as_view(), name='set-user-password'),
    (r'password_change/$', password_change,
     {'template_name': 'dashboard/password_reset.html', 'post_change_redirect': 'admin-list-users'}),
    url('^deals/', Deals.as_view(), name='admin-list-deals'),
    url('^new-deal/', CreateDeal.as_view(), name='add-deal'),
    url('^update-deal/(?P<pk>\d+)$', UpdateDeal.as_view(), name='update-deal'),


    url('^config/$', Settings.as_view(), name='dashboard-settings'),
)