# RDF Tools

This package consists of a set of command-line tools that do interesting things with RDF and SPARQL.

The functionality is provided by RDFLib, and while that provides a set of commands those provided here are somewhat more extensive and also based upon a common command framework that can be extended easily for more cases.

## Usage

The tooling uses a common starting command, `rdf`, that then executes sub-commands. As expected, the command has a help function and lists the supported sub-commands as _positional arguments_. These sub-commands also have their own help.

```bash
$ rdf -h
usage: rdf [-h] [-v] {validate,convert,select,query} ...

RDF tool

positional arguments:
  {validate,convert,select,query}
  subargs

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
```

The currently supported sub-commands are as follows.

* `convert` - convert files between different RDF representations (NTriples, Notation3, XML, ...).
* `query` - execute SPARQL queries over RDF files.
* `select` - simple projections from RDF files.
* `validate` - validate an RDF file.

An example, running a SPARQL query over a downloaded file is shown below.

```bash
rdf query -i ~/social.n3 -r n3 -q "SELECT DISTINCT ?person ?topic WHERE { ?person <http://example.org/social/relationship/1.0/likes> ?topic. }"
person                                         topic
============================================== =============================================
http://amazon.com/cprm/customers/1.0/Alice     http://amazon.com/cprm/entities/1.0/Diving
http://amazon.com/cprm/customers/1.0/Bob       http://amazon.com/cprm/entities/1.0/Diving
http://amazon.com/cprm/customers/1.0/Alice     http://amazon.com/cprm/entities/1.0/Shoes
3 rows returned in 1.629622 seconds.
```

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

The results from `startup` are a standard logger and an `ArgumentParser` `Namespace` object. The tool can then use the functions `read`, `read_into`, `read_all`, `write`, and `query` to perform common operations on RDF files.

## References

* [RDF Working Group](https://www.w3.org/2011/rdf-wg/wiki/Main_Page)
* [SPARQL Overview](https://www.w3.org/TR/sparql11-overview/)
* [RDFLib](https://github.com/RDFLib/rdflib)
