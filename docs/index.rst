Welcome to django-realestate's documentation!
=============================================

Installing
----------
Install **django-realestate** with ``pip install -e git+https://github.com/wm3ndez/realestate.git#egg=realestate``.

Usage
-----

Add the need apps to INSTALLED_APPS::


        INSTALLED_APPS =(
            ...

            'realestate',
            'realestate.listing',
            'realestate.home',

            #django-constance
            'constance',
            'constance.backends.database', # see django-constance documentation

        )

Add the url patterns::

        url('^', include('realestate.urls'))

Configure Constance::

        CONSTANCE_CONFIG = {
            'PROPERTIES_PER_PAGE': (16, _('Properties per page')),
            'RECENTLY_ADDED': (6, _('Recently Added')),

        }


Assuming that you are storing Constance values in the Database::

        CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


