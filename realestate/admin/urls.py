from django.conf.urls import patterns, url
from realestate.admin.views import Dashboard

urlpatterns = patterns(
    'realestate.admin.views',
    url('^$', Dashboard.as_view(), name='dashboard'),

)