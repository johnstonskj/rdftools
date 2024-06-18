import argparse
import i18n

import rdftools


def add_args(parser):
    parser.add_argument('-o', '--output', metavar='FILE', type=argparse.FileType('w'))
    parser.add_argument('-w', '--write', metavar='FORMAT', action='store',
                        choices=rdftools.FORMATS)
    return parser


def main():
    (LOG, cmd) = rdftools.startup('scripts.convert_command', add_args)
    try:
        graph = rdftools.read_all(cmd.input, cmd.read)
        rdftools.write(graph, cmd.output, cmd.write)
    except SyntaxError as ex:
        print(i18n.t('scripts.read_error', message=ex.message))
