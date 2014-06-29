import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = (
    ('Williams Mendez', 'wmendez27@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/realestate.db' % PROJECT_ROOT,
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Santo_Domingo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
_ = lambda s: s
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('es', _('Spanish')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lkvn#jzxj1jz8hk#y+74*)u8d#!0s@alaz(ytc6q=3@lgt$h-k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'testproject.urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'constance',
    'constance.backends.database',

    'django_extensions',
    'south',
    'sorl.thumbnail',
    'realestate',
    'realestate.listing',
    'realestate.home',
    'realestate.api',
    'testproject',
    'testproject.localsite',
    'rest_framework',
    'discoverage'

)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'PROPERTIES_PER_PAGE': (16, _('Properties per page')),
    'RECENTLY_ADDED': (6, _('Recently Added')),
    'CONTACT_DEFAULT_EMAIL': (ADMINS[0][0], _('Contact form email'))
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    # 'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'realestate.api.authentication.ApiKeyAuthentication',  # this should be the last one cause it never returns none
    )
}

CURRENCIES = ('USD', 'EUR', 'CNY', 'DOP',)

# Test Settings
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'discoverage.DiscoverageRunner'

import sys

if 'test' in sys.argv:
    # Speed up Tests by changing the default Password Hasher
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

try:
    from settings_local import *
except ImportError:
    pass