# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import environ, path
import re


def find_version(filename):
    """ Find the embedded version string in the package source. """
    _version_re = re.compile(r"__VERSION__ *= *'(.*)'", re.IGNORECASE)
    for line in open(filename):
        version_match = _version_re.match(line)
        if version_match:
            return version_match.group(1)


def get_packages():
    """ Return a list of packages that represent the distributed source. """
    packages = find_packages(exclude=['data', 'docs', 'test', 'examples', 'venv'])
    if environ.get('READTHEDOCS', None):
        # if building docs for RTD, include examples to get docstrings
        packages.append('examples')
    return packages


def get_long_description(filename):
    """ Read the long description from a file, usually a README.*. """
    with open(filename) as f:
        return f.read()


NAME = 'rdftools'
HERE = path.abspath(path.dirname(__file__))
VERSION = find_version(path.join(HERE, ('%s/__init__.py' % NAME)))
PACKAGES = get_packages()
LONG_DESCRIPTION = get_long_description(path.join(HERE, 'README.md'))
LICENSE = "MIT"

setup(
    name=NAME,
    version=VERSION,
    description='Command-line tools for RDF: conversion, validation, simple and SPARQL querries',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/elevont/%s' % NAME,
    author='Simon Johnston',
    author_email='johnstonskj@gmail.com',
    license=LICENSE,
    classifiers=[ # Optional
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: %s License" % LICENSE,
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='development, RDF',
    packages=PACKAGES,
    python_requires='>=3.3',
    # NOTE While this is the same info as in 'requirements.txt',
    #      we should still maintain them separately,
    #      see <https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py>.
    #      While we should maintain the minimum requried versions here,
    #      we might want to promote more recent versions in 'requirements.txt'.
    install_requires=[
        'rdflib>=4.2',
        'python-i18n>=0.3',
        'pyyaml>=3.10',
        'termcolor>=1.1.0'
        ],
    tests_require=[
        'pytest>=3.0',
        'pytest-cov>2.5',
        'coverage>3.7',
        'coveralls>1.1'
        ],
    package_data={
        '': ['*.yml']
    },
    entry_points={ # Optional
        'console_scripts': [
            'rdf=rdftools.scripts.rdf:main',
            'rdf-convert=rdftools.scripts.convert:main',
            'rdf-query=rdftools.scripts.query:main',
            'rdf-select=rdftools.scripts.select:main',
            'rdf-shell=rdftools.scripts.shell:main',
            'rdf-validate=rdftools.scripts.validate:main',
        ],
    }
)
