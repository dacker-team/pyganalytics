# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyspreadsheet',
    version='0.0.4',
    description='Easily send data to Google Sheets',
    long_description=readme,
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyspreadsheet',
    license=license,
    keywords='send data google spreadsheet sheets easy',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',

)
