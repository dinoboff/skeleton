#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup


PROJECT = 'skeleton'
VERSION = '0.1'
URL = 'http://github.com/dinoboff/skeleton'
AUTHOR = 'Damien Lebrun'
AUTHOR_EMAIL = 'dinoboff@gmail.com'
DESC = "Basic Template system for project skeleton."

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=['skeleton',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points = {},
    classifiers=[],
)
