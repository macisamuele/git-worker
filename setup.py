# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='Git Worker',
    version='0.0.1-dev',
    description='Configurable Git Update manager',
    license='Apache License, Version 2.0',

    author='Samuele Maci',
    author_email='macisamuele@gmail.com',

    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    keywords='git',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    install_requires=[
        'argparse',
        'jsonschema >= 2.5.1',
        'simplejson >= 3.8.2',
    ],
)
