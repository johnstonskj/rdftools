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

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name='rdftools',
    version='0.1.0',
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
    install_dependencies=['rdflib'],
       extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
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
