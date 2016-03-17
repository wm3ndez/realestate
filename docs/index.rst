Welcome to django-realestate's documentation!
=============================================

Installing
----------
Install **django-realestate** with ``pip install -e git+https://github.com/wm3ndez/realestate.git#egg=realestate``.

Usage
-----

Add dependencies to INSTALLED_APPS::


        INSTALLED_APPS =(
            # other apps

            'realestate',
            'realestate.listing',
            'realestate.home',

            #django-constance
            'constance',
            # see django-constance documentation
            'constance.backends.database',
            'widget_tweaks',
            'haystack',

        )

Add the url patterns::

        url('^', include('realestate.urls'))

Configure Constance::

        CONSTANCE_CONFIG = {
            'PROPERTIES_PER_PAGE': (16, 'Properties per page'),
            'RECENTLY_ADDED': (6, 'Recently Added'),
            'CONTACT_DEFAULT_EMAIL': ('contact@example.com', 'Contact form email')

        }


Assuming that you are storing Constance values in the Database::

        CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


Though, the default and recommended backend is Redis. You can read more
here: https://github.com/comoga/django-constance#redis-default



Haystack
--------

We're using Haystack to handle the search.  Here is an example using
Elasticsearch::

        HAYSTACK_CONNECTIONS = {
                'default': {
                        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
                        'URL': 'http://127.0.0.1:9200/',
                        'INDEX_NAME': 'realestate',
                },
        }


You might use a simpler configuration for development::

        HAYSTACK_CONNECTIONS = {
            'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        }


For more info you can look at Haystack documentation:
http://django-haystack.readthedocs.org/en/latest/tutorial.html#modify-your-settings-py


RESTful API
-----------

**djangorestframework**
