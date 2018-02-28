#!/usr/bin/env python

import rdflib
import sys
from timeit import default_timer as timer

import rdftools

def add_args(parser):
    parser.add_argument('-q', '--query', action='store')
    return parser

def main():
    (LOG, cmd) = rdftools.startup(add_args)
    
    graph = rdftools.read_all(cmd.input, cmd.read)
    
    LOG.info('Executing query...')
    LOG.debug(cmd.query)
    start = timer()
    results = graph.query(cmd.query)
    end = timer()
    LOG.debug('rows: %d' % len(results))
    columns = results.bindings[0].keys()
    LOG.debug('columns: %s' % (', '.join([str(c) for c in columns])))

    rdftools.report(columns, results,  end - start)
