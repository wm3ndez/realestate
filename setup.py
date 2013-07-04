#!/usr/bin/env python
from distutils.core import setup
from distutils.util import convert_path
from realestate import __version__, __maintainer__, __email__
from fnmatch import fnmatchcase
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

standard_exclude = ['*.py', '*.pyc', '*~', '.*', '*.bak']
standard_exclude_directories = [
    '.*', 'CVS', '_darcs', './build',
    './dist', 'EGG-INFO', '*.egg-info', 'testproject'
]


def find_package_data(where='.', package='', exclude=standard_exclude,
                      exclude_directories=standard_exclude_directories,
                      only_in_packages=True, show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                'Directory %s ignored by pattern %s'
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py'))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append(
                        (fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                'File %s ignored by pattern %s'
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


excluded_directories = standard_exclude_directories + ['./requirements',
                                                       './scripts']
package_data = find_package_data(exclude_directories=excluded_directories)
license_text = open('LICENSE.txt').read()
long_description = open('README.rest').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    #    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    #    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django'
]

DESCRIPTION = """Real Estate Built on Django FW by Williams Mendez"""

setup(
    name='realestate',
    version=__version__,
    url='https://bitbucket.org/wm3ndez/realestate',
    author=__maintainer__,
    author_email=__email__,
    license=license_text,
    packages=find_packages(),
    package_data=package_data,
    #    data_files=[('', ['LICENSE.txt',
    #                      'README.rest'])],
    description=DESCRIPTION,
    long_description=long_description,
    classifiers=CLASSIFIERS,
    #    tests_require=[
    #        'django',
    #    ],
    #    test_suite='django_facebook.runtests.runtests',
    install_requires=[
        'Django==1.5.1',
        'Fabric==1.6.1',
        'MarkupSafe==0.18',
        'MySQL-python==1.2.4',
        'PIL==1.1.7',
        'Pygments==1.6',
        'South==0.8.1',
        'Sphinx==1.2b1',
        'Werkzeug==0.9.1',
        'argparse==1.2.1',
        'coverage==3.6',
        'decorator==3.4.0',
        'django-admin-tools==0.5.1',
        'django-coverage==1.2.4',
        'django-debug-toolbar==0.9.4',
        'django-extensions==1.1.1',
        '-e git+https://github.com/tschellenbach/Django-facebook.git#egg=django_facebook-dev',
        '-e git+ssh://git@bitbucket.org/wm3ndez/django-hitcounter.git#egg=django_hitcount-dev',
        'django-localeurl==1.5',
        'django-newsletter==0.4.1',
        'django-seo==0.3.5',
        'django-tinymce==1.5.1',
        'docutils==0.10',
        'feedparser==5.1.3',
        'httplib2==0.8',
        'ipdb==0.7',
        'ipdbplugin==1.2',
        'ipython==0.13.2',
        'nose==1.3.0',
        'oauth2==1.5.211',
        'paramiko==1.10.1',
        'pycrypto==2.6',
        'python-twitter==1.0',
        'simplejson==3.3.0',
        'six==1.3.0',
        'sorl-thumbnail==11.12',
        'surlex==0.1.2',
        'wsgiref==0.1.2',
    ],
)
