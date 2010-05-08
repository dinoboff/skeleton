#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

PROJECT = 'skeleton'
VERSION = '0.4'
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
    license='BSD',
    packages=['skeleton', 'skeleton.tests', 'skeleton.examples'],
    test_suite='skeleton.tests',
    use_2to3=True,
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        'virtualenv-templates':  [
            'virtualenvwrapper>=2.1.1',
            'virtualenvwrapper.project>=1.0'
            ],
    },
    entry_points={
        'virtualenvwrapper.project.template': [
            'package = skeleton.examples.basicpackage:virtualenv_warpper_hook',
            ],
        },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        ],
)
