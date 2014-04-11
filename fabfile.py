from fabric.api import local


def test_app(cli_args=''):
    local('venv/bin/coverage -x testproject/manage.py test %s' % cli_args)


def runserver(cli_args=''):
    local('venv/bin/python testproject/manage.py runserver_plus 0.0.0.0:8000 %s' % cli_args)


def local_deploy():
    local('mv testproject/realestate.db testproject/realestate_bak.db')
    local('venv/bin/python testproject/manage.py syncdb;', False)
    local('venv/bin/python testproject/manage.py migrate')
    local('venv/bin/python testproject/manage.py loaddata realestate/propiedad/fixtures/atributos.json')
