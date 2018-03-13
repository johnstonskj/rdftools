import i18n
from rdflib.namespace import RDF
import rdftools


def add_args(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--subjects', dest='select',
                       const='subjects', action='store_const')
    group.add_argument('-p', '--predicates', dest='select',
                       const='predicates', action='store_const')
    group.add_argument('-o', '--objects', dest='select',
                       const='objects', action='store_const')
    group.add_argument('-t', '--types', dest='select',
                       const='types', action='store_const')
    return parser


def selector(LOG, graph, primary, **kwargs):
    LOG.info(i18n.t('scripts.select_%s' % primary))
    for v in set(getattr(graph, primary)(**kwargs)):
        print(v)


def main():
    (LOG, cmd) = rdftools.startup('scripts.select_command', add_args)

    graph = rdftools.read_all(cmd.input, cmd.read)

    if cmd.select in ['subjects', 'predicates', 'objects']:
        selector(LOG, graph, cmd.select)
    elif cmd.select == 'types':
        selector(LOG, graph, 'objects', predicate=RDF.type)
