#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
from distutils.core import setup
from setuptools import find_packages

from difoss_pybase import __version__

setup (
    name        = 'difoss_pybase',
    version     =  __version__,
    description = 'Python base library in python 2.7',
    author      = 'Difoss Chan',
    author_email= 'difoss@163.com',
    license     = 'Apache License 2.0',
    install_requires = ['mysql-connector-python', 'colorama'],
    platforms = 'any',
    classifiers = [
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    packages = find_packages()
)
