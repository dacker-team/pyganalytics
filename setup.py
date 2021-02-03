from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='pyganalytics',
    version='0.1.23',
    description='Easily get data from Google Analytics',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyganalytics',
    keywords='get data google analytics easy',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ["requirements.txt"]},
    python_requires='>=3',
    install_requires=[
        "dbstream>=0.0.12",
        "PyYAML>=5.1",
        "isoweek>=1.3.3",
        "googleauthentication>=0.0.15"
    ],
)
