#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

from skeleton.meta import *

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license='BSD',
    packages=['skeleton',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points = {},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        ],
)
