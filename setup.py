#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask-Bulbs
-------------

Flask extension for [Bulbs](http://bulbflow.com/) supporting the factory pattern with the init_app method.
"""
from setuptools import setup


setup(
    name='Flask-Bulbs',
    version='0.1',
    url='http://github.com/peterhil/flask-bulbs/',
    license='MIT',
    author='Peter Hillerström',
    author_email='peter.hillerstrom@gmail.com',
    description='Flask extension for [Bulbs](http://bulbflow.com/) supporting the factory pattern with the init_app method.',
    long_description=__doc__,
    py_modules=['flask_bulbs'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_bulbs'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'bulbs',
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
