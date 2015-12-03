from datetime import datetime

from fabric.api import local
from fabric.colors import _wrap_with
from fabric.context_managers import settings

green_bg = _wrap_with('42')
red_bg = _wrap_with('41')


def test_app(cli_args=''):
    if len(cli_args.strip()) == 0:
        source = 'realestate'
    else:
        source = cli_args.replace('.', '/')

    command = "coverage run --source='%s' tests/runtests.py test %s;" % (source, cli_args)
    command += "coverage report --omit=*tests*,*test_*,*migrations*," \
               "*wsgi.py* --show-missing"

    local('clear')
    print("Test started at:")
    print('\033[93m' + datetime.now().strftime("%I:%M:%S"))
    print('\033[0m')

    with settings(warn_only=True):
        result = local(command)

    if result.failed:
        print(red_bg("Some tests failed"))
    else:
        print()
        print(green_bg("All tests passed - have a banana!"))


def runserver(cli_args=''):
    local('venv/bin/python testproject/manage.py runserver_plus 0.0.0.0:8000 %s' % cli_args)


def shell():
    local('venv/bin/python testproject/manage.py shell_plus')


def local_deploy():
    local('mv testproject/realestate.db testproject/realestate_bak.db')
    local('venv/bin/python testproject/manage.py syncdb;', False)
    local('venv/bin/python testproject/manage.py migrate')
    local('venv/bin/python testproject/manage.py loaddata attributes.json')
