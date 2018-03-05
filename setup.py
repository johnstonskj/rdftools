"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
# Get version from module
import rdftools

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name=rdftools.__name__,
    version=rdftools.__VERSION__,
    description='Command-line tools for RDF',
    long_description=long_description,
    url='https://github.com/johnstonskj/rdftools',
    author='Simon Johnston',
    author_email='johnstonskj@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='development, RDF',
    packages=find_packages(exclude=['data', 'docs', 'tests']),
    python_requires='>=3.3',
    install_requires=['rdflib>=4.2'],
    tests_require=['pytest>=3.0', 'pytest-cov>2.5', 'coverage>3.7', 'coveralls>1.1'],
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
