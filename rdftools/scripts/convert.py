#!/usr/bin/env python

import argparse
import rdflib

import rdftools

def add_args(parser):
    parser.add_argument('-o', '--output', type=argparse.FileType('w'))
    parser.add_argument('-w', '--write', action='store',
                        choices=rdftools.FORMATS)
    return parser

def main():
    (LOG, cmd) = rdftools.startup(add_args)
    
    graph = rdftools.read_all(cmd.input, cmd.read)
    
    rdftools.write(graph, cmd.output, cmd.write)
