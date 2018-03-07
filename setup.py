# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import environ, path
import re


def find_version(filename):
    """ Find the embedded version string in the package source. """
    _version_re = re.compile(r"__VERSION__ = '(.*)'")
    for line in open(filename):
        version_match = _version_re.match(line)
        if version_match:
            return version_match.group(1)


def get_packages():
    """ Return a list of packages that represent the distributed source. """
    packages = find_packages(exclude=['data', 'docs', 'test', 'examples'])
    if environ.get('READTHEDOCS', None):
        # if building docs for RTD, include examples to get docstrings
        packages.append('examples')
    return packages


def get_long_description(filename):
    """ Read the long description from a file, usually a README.*. """
    with open(filename) as f:
        return f.read()


def get_requirements(filename):
    requirements = []
    with open(filename) as f:
        requirements.append(f.read().splitlines())
    return requirements


NAME = 'rdftools'
HERE = path.abspath(path.dirname(__file__))
VERSION = find_version(path.join(HERE, ('%s/__init__.py' % NAME)))
PACKAGES = get_packages()
LONG_DESCRIPTION = get_long_description(path.join(HERE, 'README.md'))

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name=NAME,
    version=VERSION,
    description='Command-line tools for RDF',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/johnstonskj/%s' % NAME,
    author='Simon Johnston',
    author_email='johnstonskj@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='development, RDF',
    packages=PACKAGES,
    python_requires='>=3.3',
    install_requires=['rdflib>=4.2', 'python-i18n>=0.3', 'pyyaml>=3.10'],
    tests_require=['pytest>=3.0', 'pytest-cov>2.5', 'coverage>3.7',
                   'coveralls>1.1'],
    entry_points={  # Optional
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
