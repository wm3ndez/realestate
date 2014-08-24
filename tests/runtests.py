# !/usr/bin/env python
import os
import sys

import django
from django.conf import settings


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',

        'realestate',
        'realestate.home',
        'realestate.listing',

        # Deps
        'constance',
        'sorl.thumbnail',
        'widget_tweaks',
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test.db"
        }
    },
    MEDIA_ROOT=os.path.join(os.path.dirname(__file__), 'media'),
    MEDIA_URL='/media/',
    STATIC_URL='/static/',

    CONSTANCE_CONFIG={
        'PROPERTIES_PER_PAGE': (16, 'Properties per page'),
        'RECENTLY_ADDED': (6, 'Recently Added'),
        'CONTACT_DEFAULT_EMAIL': ('email@example.com', 'Contact form email')
    },
    CONSTANCE_CONNECTION_CLASS='tests.redis_mockup.Connection',
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    ROOT_URLCONF='realestate.urls',
    TEMPLATE_DIRS=(os.path.abspath(os.path.join(os.path.dirname(__file__), '../realestate/templates')), ),
)


def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner

        runner_class = DiscoverRunner
        test_args = ['realestate']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner

        runner_class = DjangoTestSuiteRunner
        test_args = ['tests']

    failures = runner_class(verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()