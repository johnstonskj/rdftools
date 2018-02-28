# RDF Tools

This package consists of a set of command-line tools that do interesting things with RDF and SPARQL.

The functionality is provided by RDFLib, and while that provides a set of commands those provided here are somewhat more extensive and also based upon a common command framework that can be extended easily for more cases.

## Usage

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

## Extending

TBD

* [RDF Working Group](https://www.w3.org/2011/rdf-wg/wiki/Main_Page)
* [SPARQL Overview](https://www.w3.org/TR/sparql11-overview/)
* [RDFLib](https://github.com/RDFLib/rdflib)
