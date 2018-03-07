# RDF Tools

This package consists of a set of command-line tools that do interesting things with RDF and SPARQL.

The functionality is provided by RDFLib, and while that provides a set of commands those provided here are somewhat more extensive and also based upon a common command framework that can be extended easily for more cases.

[![Travis Status](https://travis-ci.org/johnstonskj/rdftools.svg?branch=master)](https://travis-ci.org/johnstonskj/rdftools)
[![Coverage Status](https://coveralls.io/repos/github/johnstonskj/rdftools/badge.svg?branch=master)](https://coveralls.io/github/johnstonskj/rdftools?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/713dc63ecf8f8efa44d7/maintainability)](https://codeclimate.com/github/johnstonskj/rdftools/maintainability)
[![Requirements](https://requires.io/github/johnstonskj/rdftools/requirements.svg?branch=master)](https://requires.io/github/johnstonskj/rdftools/requirements/?branch=master)
<!--
[![Doc Status](https://readthedocs.org/projects/rdftools/badge/?style=flat)](https://readthedocs.org/projects/rdftools)
-->
[![GitHub stars](https://img.shields.io/github/stars/johnstonskj/rdftools.svg)](https://github.com/johnstonskj/rdftools/stargazers)
[![Current Version](https://img.shields.io/pypi/v/rdftools.svg)](https://pypi.python.org/pypi/rdftools)
[![Python Versions](https://img.shields.io/pypi/pyversions/rdftools.svg)](https://pypi.python.org/pypi/rdftools)
[![Python Implementations](https://img.shields.io/pypi/implementation/rdftools.svg)](https://pypi.python.org/pypi/tdftools)

## Usage

The tooling uses a common starting command, `rdf`, that then executes sub-commands. As expected, the command has a help function and lists the supported sub-commands as _positional arguments_. These sub-commands also have their own help.

```
$ rdf -h
usage: rdf [-h] [-v] {validate,convert,select,query} ...

RDF tool

positional arguments:
  {validate,convert,select,shell,query}
  subargs

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
```

The currently supported sub-commands are as follows.

* `convert` - convert files between different RDF representations (NTriples, Notation3, XML, ...).
* `query` - execute SPARQL queries over RDF files.
* `select` - simple projections from RDF files.
* `shell` - run an interactive shell session.
* `validate` - validate an RDF file.

An example, running a SPARQL query over a downloaded file is shown below.

```
$ rdf query -i ~/social.n3 -r n3 -q "SELECT DISTINCT ?person ?topic WHERE { ?person <http://example.org/social/relationship/1.0/likes> ?topic. }"
person                                         topic
============================================== =============================================
http://amazon.com/cprm/customers/1.0/Alice     http://amazon.com/cprm/entities/1.0/Diving
http://amazon.com/cprm/customers/1.0/Bob       http://amazon.com/cprm/entities/1.0/Diving
http://amazon.com/cprm/customers/1.0/Alice     http://amazon.com/cprm/entities/1.0/Shoes
3 rows returned in 1.629622 seconds.
```

## Debugging

The `-v` parameter to either `rdf` or one of the sub-commands controls the standard Python logging level. It can be stated multiple times to increase the logging; `-v` for warnings, `-vv` for informational, `-vvv` for debug.

## Interactive Shell

For a more interactive exploration of RDF data you can run `rdf shell` which gives you access to a lot of the same functions in the separate tools. The shell has a single common graph into which you can load data from external files (and stores in the future), and run SPARQL queries. The shell also has a default initialization file, so commonly used prefixes, common data, etc. can be loaded before you start your session.

```
$ rdf shell
RDF Shell, v0.1.0.
reading commands from file /Users/simonjo/.rdfshrc
Graph updated with 40 statements.
>
```

As you might expect, the shell supports a `help` function and command completion as well as a persistent history.

### Initialization File

The default location for this is `~/.rdfshrc`, all commands are read as if you typed them into the shell.

### History File

The default location for this is `~/.rdfsh_hist`, it will be read at startup and updated on closing the shell.

## Extending

New commands are added as modules in the `rdftools/scripts` folder and have the following structure.

```python
import rdftools

def main():
    (LOG, cmd) = rdftools.startup('Tool description.', add_args=None)

    ...
```

The `add_args` parameter is used to add additional command-line arguments to the common `argparse` structure. The function, if required, takes in a parser object and returns it. The common command line arguments include verbosity, help, and reading files.

```python
def add_args(parser):
    return parser

```

The results from `startup` are a standard logger and an (`ArgumentParser`) `Namespace` object. The tool can then use the functions `read`, `read_into`, `read_all`, `write`, and `query` to perform common operations on RDF files.

Extending the shell is also pretty simple, you add a function of the following form, it always takes a context object first, and the doc string will be used by default as the displayed help for your command. Arguments may be parsed for more structure, and `print()` is used extensively for user feedback. Note that you must always return the context, whether you updated it or not. The `add_command` function will install it into the shell, enabling help and command completion.

```python
def echo(context, args):
    """ echo text
        Echo back the following text."""
    print(args)
    return context
add_command(echo)
```

## References

* [RDF Working Group](https://www.w3.org/2011/rdf-wg/wiki/Main_Page)
* [SPARQL Overview](https://www.w3.org/TR/sparql11-overview/)
* [RDFLib](https://github.com/RDFLib/rdflib)
* [Travis Project](https://travis-ci.org/johnstonskj/rdftools)
* [Coveralls Project](https://coveralls.io/github/johnstonskj/rdftools)
