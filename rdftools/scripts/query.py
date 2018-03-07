import i18n
from timeit import default_timer as timer

import rdftools


def add_args(parser):
    parser.add_argument('-q', '--query', action='store')
    return parser


def main():
    (LOG, cmd) = rdftools.startup('scripts.query_command', add_args)

    graph = rdftools.read_all(cmd.input, cmd.read)

    LOG.info(i18n.t('scripts.query_started'))
    LOG.debug(cmd.query)
    start = timer()
    results = graph.query(cmd.query)
    end = timer()
    LOG.debug(i18n.t('scripts.query_rows', len=len(results)))
    if len(results) > 0:
        columns = results.bindings[0].keys()
        LOG.debug(i18n.t('scripts.query_columns',
                  names=', '.join([str(c) for c in columns])))
        rdftools.report(columns, results,  end - start)
    else:
        LOG.info(i18n.t('scripts.query_no_results'))
