from fabric.api import local


def test_app(cli_args=''):
    local('venv/bin/coverage -x testproject/manage.py test %s' % cli_args)


def runserver(cli_args=''):
    local('venv/bin/python testproject/manage.py runserver_plus 0.0.0.0:8000 %s' % cli_args)
