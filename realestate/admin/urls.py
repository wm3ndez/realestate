from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from realestate.admin import views as admin_views

urlpatterns = patterns(
    'realestate.admin.views',
    url('^$', admin_views.Dashboard.as_view(), name='dashboard'),

    url('^listing/', admin_views.Listings.as_view(), name='admin-list-listing'),
    url('^new-listing/(?P<step>.+)$', admin_views.CreateListingWizard.as_view(url_name="add-listing-wizard"),
        name='add-listing-wizard'),
    # url('^update-listing/(?P<pk>\d+)$', admin_views.UpdateListing.as_view(), name='update-listing'),
    url('^agents/', admin_views.Agents.as_view(), name='admin-list-agents'),
    url('^new-agent/', admin_views.CreateAgent.as_view(), name='add-agent'),
    url('^update-agent/(?P<pk>\d+)$', admin_views.UpdateAgent.as_view(), name='update-agent'),
    url('^contacts/', admin_views.Contacts.as_view(), name='admin-list-contacts'),
    url('^new-contact/', admin_views.CreateContact.as_view(), name='add-contact'),
    url('^update-contact/(?P<pk>\d+)$', admin_views.UpdateContact.as_view(), name='update-contact'),
    url('^locations/', admin_views.Locations.as_view(), name='admin-list-sectors'),
    url('^new-location/', admin_views.CreateLocation.as_view(), name='add-sector'),
    url('^update-location/(?P<pk>\d+)$', admin_views.UpdateLocation.as_view(), name='update-sector'),
    url('^users/', admin_views.Users.as_view(), name='admin-list-users'),
    url('^new-user/', admin_views.CreateUser.as_view(), name='add-user'),
    url('^update-user/(?P<pk>\d+)$', admin_views.UpdateUser.as_view(), name='update-user'),
    url('^set-user-password/(?P<user_id>\d+)$', admin_views.SetUserPassword.as_view(), name='set-user-password'),
    (r'password_change/$', password_change,
     {'template_name': 'dashboard/password_reset.html', 'post_change_redirect': 'admin-list-users'}),
    url('^deals/', admin_views.Deals.as_view(), name='admin-list-deals'),
    url('^new-deal/', admin_views.CreateDeal.as_view(), name='add-deal'),
    url('^update-deal/(?P<pk>\d+)$', admin_views.UpdateDeal.as_view(), name='update-deal'),
    url('^api-keys/', admin_views.ApiKeys.as_view(), name='admin-api-keys'),
    url('^new-api-key/', admin_views.CreateApiKey.as_view(), name='add-apikey'),
    url('^delete-api-key/(?P<pk>[\w-]+)$', admin_views.DeleteApiKey.as_view(), name='delete-apikey'),

    url('^config/$', admin_views.Settings.as_view(), name='dashboard-settings'),
)