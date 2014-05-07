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

        )

Add the url patterns::

        url('^', include('realestate.urls'))

