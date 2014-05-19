# !/usr/bin/env python
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


excluded_directories = standard_exclude_directories + ['./requirements', './scripts']
package_data = find_package_data(exclude_directories=excluded_directories)
license_text = open('LICENSE.txt').read()
long_description = open('README.rst').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Office/Business',
    'Framework :: Django'
]

DESCRIPTION = """Real Estate app built on Django"""

setup(
    name='django-realestate',
    version=__version__,
    url='https://github.com/wm3ndez/realestate',
    author=__maintainer__,
    author_email=__email__,
    license=license_text,
    packages=find_packages(),
    package_data=package_data,
    description=DESCRIPTION,
    long_description=long_description,
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.5.1',
        'MySQL-python',
        'Pillow',
        'South',
        'Werkzeug',
        'decorator==3.4.0',
        'django-extensions',
        'django-localeurl',
        'six',
        'sorl-thumbnail',
        'djangorestframework',
        'django-filter',
        'django-braces==1.4.0',
        'django-money==0.4.1',
        'django-discover-runner==1.0',
        'django-discoverage==1.0.0',
        'django-constance',
        'django-picklefield',
    ],
    test_suite='tests.runtests.main',
)
