# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyganalytics',
    version='0.0.4',
    description='Easily get data from Google Analytics',
    long_description=readme,
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyganalytics',
    license=license,
    keywords='get data google analytics easy',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',

)
