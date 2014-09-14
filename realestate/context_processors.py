# -*- coding: utf-8 -*-
# taken from https://github.com/noirbizarre/django-absolute

from django.contrib.sites.models import Site
from django.conf import settings


def get_site_url(request, slash=False):
    domain = Site.objects.get_current().domain
    protocol = 'https' if request.is_secure() else 'http'
    root = "%s://%s" % (protocol, domain)
    if slash:
        root += '/'
    return root


def absolute(request):
    urls = {
        'ABSOLUTE_ROOT': request.build_absolute_uri('/')[:-1].strip("/"),
        'ABSOLUTE_ROOT_URL': request.build_absolute_uri('/').strip("/"),
    }

    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        urls['SITE_ROOT'] = get_site_url(request)
        urls['SITE_ROOT_URL'] = get_site_url(request, True)

    return urls


def site_name(request):
    return {'site_name': Site.objects.get_current().name}
