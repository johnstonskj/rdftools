import i18n
import rdftools


def add_args(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--subjects', dest='select',
                       const='s', action='store_const')
    group.add_argument('-p', '--predicates', dest='select',
                       const='p', action='store_const')
    group.add_argument('-o', '--objects', dest='select',
                       const='o', action='store_const')
    group.add_argument('-t', '--types', dest='select',
                       const='t', action='store_const')
    return parser


def main():
    (LOG, cmd) = rdftools.startup('scripts.select_command', add_args)

    graph = rdftools.read_all(cmd.input, cmd.read)

    if cmd.select == 's':
        LOG.info(i18n.t('scripts.select_subjects'))
        for s in set(graph.subjects()):
            print(s)
    elif cmd.select == 'p':
        LOG.info(i18n.t('scripts.select_predicates'))
        for s in set(graph.predicates()):
            print(s)
    elif cmd.select == 'o':
        LOG.info(i18n.t('scripts.select_objects'))
        for s in set(graph.objects()):
            print(s)
    elif cmd.select == 't':
        LOG.info(i18n.t('scripts.select_types'))
        for s in set(graph.objects(
                predicate='http://www.w3.org/1999/02/22-rdf-syntax-ns#type')):
            print(s)
