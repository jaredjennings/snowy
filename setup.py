#!/usr/bin/env python

from setuptools import setup

setup(
    name='snowy',
    version='0.7.1',
    description='Sync server for Tomboy/Tomdroid/Conboy notes',
    author='Jared Jennings',
    author_email='jjennings@fastmail.fm',
    url='https://github.com/jaredjennings/snowy',
    install_requires=['Django<=1.4', 'lxml', 'pytz', 'dateutil', 'openid', 'South', 'psycopg2'],
)
