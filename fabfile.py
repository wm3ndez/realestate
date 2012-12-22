from fabric.api import local, run, env

env.hosts = ['wmendez@108.59.4.79:22']

def test_app(cli_args=''):
    local('venv/bin/coverage -x holguinmatos/manage.py test %s' % cli_args)


def run_server(cli_args=''):
    local('venv/bin/python holguinmatos/manage.py runserver 0.0.0.0:8000 %s' % cli_args)


def pushpull():
    local('git push') # runs the command on the local environment
    run('cd webapps/holguinmatos/; git pull; ./apache2/bin/restart') # runs the command on the remote environment

def deploy():
    run('cd webapps/holguinmatos/; git pull; ./apache2/bin/restart') # runs the command on the remote environment