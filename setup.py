#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from __future__ import absolute_import, division, unicode_literals
import os

from setuptools import setup, find_packages

from spruce import __version__

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()
CHANGELOG = open(os.path.join(ROOT, 'CHANGELOG.txt')).read()

install_requires = []
tests_require = [
    'nose==1.2.1',
]

setup(
    name='spruce',
    version=__version__,
    # author='',
    # author_email='',
    url='http://github.com/Pewpewarrows/spruce',
    description='Spruce up your automated deployment!',
    long_description=README + '\n\n' + CHANGELOG,
    packages=find_packages(exclude=('tests',)),
    # package_data={'': ''},
    # package_dir={'': ''},
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    # test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    license='MIT',
    keywords='',
)
