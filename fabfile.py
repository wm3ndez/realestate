from fabric.api import local, run, env


def test_app(cli_args=''):
    local('venv/bin/coverage -x testproject/manage.py test %s' % cli_args)


def run_server(cli_args=''):
    local('venv/bin/python testproject/manage.py runserver 0.0.0.0:8000 %s'
          % cli_args)


