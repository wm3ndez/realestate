import os

root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
activate_this = os.path.join(root_path, "venv/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'
application = WSGIHandler()
