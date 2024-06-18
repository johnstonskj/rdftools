import argparse
import i18n
import logging
import os
import rdflib
import sys
from termcolor import colored
from timeit import default_timer as timer

__VERSION__ = '0.2.0'

__LOG__ = None

FORMATS = ['hext', 'json-ld', 'n3', 'nquads', 'nt', 'trig', 'trix', 'turtle', 'xml', 'pretty-xml']
FORMAT_DEFAULT = 'turtle'

HEADER_SEP = '='
COLUMN_SEP = '|'
EMPTY_LINE = ''
COLUMN_SPEC = '{:%d}'

USE_COLOR = False


def startup(description_key, add_args, read_files=True, argv=None):
    global __LOG__, USE_COLOR
    configure_translation()
    description = i18n.t(description_key)
    parser = configure_argparse(description, read_files)
    if callable(add_args):
        parser = add_args(parser)
    if argv is None:
        command = parser.parse_args()
    else:
        command = parser.parse_args(argv)
    USE_COLOR = command.use_color
    process = parser.prog
    __LOG__ = configure_logging(process, command.verbose)
    __LOG__.info(i18n.t('rdftools.started', tool=process, name=description))
    __LOG__.info(argv)
    return (__LOG__, command)


def configure_translation(force_locale=None):
    i18n.load_path.append(os.path.join(os.path.dirname(__file__), 'messages'))
    if force_locale is not None:
        i18n.set('locale', force_locale)
    i18n.set('fallback', 'en')


def configure_argparse(description, read_files=True):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('-b', '--base', action='store')
    if read_files:
        parser.add_argument('-i', '--input', metavar='FILE',
                            type=argparse.FileType('r'), nargs='*')
        parser.add_argument('-r', '--read', action='store', choices=FORMATS)
    parser.add_argument('-c', '--use-color', action='store_true')
    return parser


def configure_logging(name, level):
    global __LOG__
    logging.basicConfig(format='%(asctime)-15s %(module)s.%(funcName)s:' +
                        '%(lineno)d [%(levelname)s] %(message)s')
    logger = logging.getLogger(name)
    if level > 2:
        logger.setLevel(logging.INFO)
    elif level > 1:
        logger.setLevel(logging.DEBUG)
    elif level > 0:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.ERROR)
    logger.info(i18n.t('rdftools.logging', level=logger.getEffectiveLevel()))
    __LOG__ = logger
    return logger


def read_into(input, format, graph, base=None):
    start = end = 0
    if format is None:
        if input is None:
            format = FORMAT_DEFAULT
        else:
            format = rdflib.util.guess_format(input.name)
    if input is None:
        __LOG__.info(i18n.t('rdftools.read_stdin', format=format))
        start = timer()
        graph.parse(source=sys.stdin.buffer, format=format, publicID=base)
        end = timer()
    else:
        __LOG__.info(i18n.t('rdftools.read_file',
                     name=input.name, format=format))
        start = timer()
        graph.parse(source=input.name, format=format, publicID=base)
        end = timer()
    __LOG__.info(i18n.t('rdftools.read_complete',
                 len=len(graph), time=end - start))
    return graph


def read(input, format, base=None):
    graph = rdflib.Graph()
    return read_into(input, format, graph, base)


def read_all(inputs, format, base=None):
    graph = rdflib.Graph()
    for input in inputs:
        graph = read_into(input, format, graph, base)
    return graph


def write(graph, output, format, base=None):
    __LOG__.debug(i18n.t('rdftools.write', graph=graph, len=len(graph)))
    start = end = 0
    if format is None:
        if output is None:
            format = FORMAT_DEFAULT
        else:
            format = rdflib.util.guess_format(output.name)
    if output is None:
        __LOG__.info(i18n.t('rdftools.write_stdout', format=format))
        start = timer()
        data = graph.serialize(format=format, base=base)
        end = timer()
        try:
            # This fails on Travis ONLY for Python 3.4
            sys.stdout.buffer.write(data)
        except AttributeError:
            sys.stdout.write(data.decode('utf-8'))
    else:
        __LOG__.info(i18n.t('rdftools.write_file',
                     name=output.name, format=format))
        start = timer()
        graph.serialize(destination=output.name, format=format, base=base)
        end = timer()
    __LOG__.debug(i18n.t('rdftools.write_complete', time=(end - start)))


def get_terminal_width(default=80):
    import shutil
    return shutil.get_terminal_size((default, 20))[0]


def header(str):
    return colored(str, attrs=['reverse']) if USE_COLOR else str


def line(str):
    return colored(str, attrs=['dark']) if USE_COLOR else str


def comment(str):
    return colored(str, attrs=['dark']) if USE_COLOR else str


def report(columns, rows, timer=0):
    # TODO: Should also take this as a parameter? so "rdf query -c 80 -q ..."
    width = get_terminal_width()
    col_width = int((width - len(columns)) / len(columns))
    col_string = COLUMN_SPEC % col_width
    for column in columns:
        print(header(col_string.format(column)), end=line(COLUMN_SEP))
    print(EMPTY_LINE)

    for column in columns:
        print(line(HEADER_SEP * col_width), end=line(COLUMN_SEP))
    print(EMPTY_LINE)

    for row in rows:
        for col in columns:
            print(col_string.format(row[col]), end=line(COLUMN_SEP))
        print(EMPTY_LINE)

    if timer != 0:
        print(comment(i18n.t('rdftools.report_timed',
                      len=len(rows), time=timer)))
    else:
        print(comment(i18n.t('rdftools.report_timed',
                      len=len(rows))))
