import argparse
import logging
import rdflib
import sys
from timeit import default_timer as timer

__FORMAT__ = '%(asctime)-15s %(module)s.%(funcName)s %(lineno)d [%(levelname)s] - %(message)s'
__LOG__ = None

FORMATS = ['nt', 'n3', 'trix', 'rdfa', 'xml']

def startup(description, add_args):
    global __LOG__
    parser = configure_argparse(description)
    if callable(add_args):
        parser = add_args(parser)
    command = parser.parse_args()
    process = parser.prog
    __LOG__ = configure_logging(process, command.verbose)
    __LOG__.info('%s started.', process)
    return (__LOG__, command)
    
def configure_argparse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('-b', '--base', action='store')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-r', '--read', action='store', choices=FORMATS)
    # return argparse.ArgumentParser(parents=[parser])
    # implies parent specifies add_help=False
    return parser

def configure_logging(name, level):
    global __LOG__
    logging.basicConfig(format=__FORMAT__)
    logger = logging.getLogger(name)
    if level > 2:
        logger.setLevel(logging.DEBUG)
    elif level > 1:
        logger.setLevel(logging.INFO)
    elif level > 0:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.ERROR)
    logger.info('Log level set to %s',logger.getEffectiveLevel())
    __LOG__ = logger
    return logger

def read_into(input, format, graph, base=None):
    start = end = 0
    if format is None:
        if input is None:
            format = FORMATS[0]
        else:
            format = rdflib.util.guess_format(input.name)
    if input is None:
        __LOG__.info('reading from STDIN, format is %s',format)
        start = timer()
        graph.parse(source=sys.stdin.buffer, format=format, publicID=base)
        end = timer()
    else:
        __LOG__.info('reading from file %s, format is %s', input.name, format)
        start = timer()
        graph.parse(source=input.name, format=format, publicID=base)
        end = timer()
    __LOG__.info("Graph has %s statements, read in %f seconds." % (len(graph), end - start))
    return graph
    
def read(input, format, base=None):
    graph = rdflib.Graph()
    return read_into(input, format, graph, base)

def read_all(inputs, format, base=None):
    graph = rdflib.Graph()
    for input in inputs:
        graph = read_into(input, format, graph, base)
    return graph

def write(graph, output, format):
    __LOG__.debug('writing graph=%s, %d statements.' % (graph, len(graph)))
    start = end = 0
    if format is None:
        if output is None:
            format = FORMATS[0]
        else:
            format = rdflib.util.guess_format(output.name)
    if output is None:
        __LOG__.info('writing to STDOUT, format is %s' % format)
        start = timer()
        data = graph.serialize(format=format)
        end = timer()
        sys.stdout.buffer.write(data)
    else:
        __LOG__.info('writing to file %s, format is %s' %  (output.name, format))
        start = timer()
        graph.serialize(destination=output.name, format='nt')
        end = timer()
    __LOG__.debug('write took %f seconds.' % (end - start)) 

def get_terminal_width(default=80):
    import shutil
    return shutil.get_terminal_size((default,20))[0]

def report(columns, rows, timer=0):
    width = get_terminal_width()
    col_width = int((width - len(columns)) / len(columns))
    col_string = '{:' + str(col_width) + '}'
    for column in columns:
        print(col_string.format(column), end=" ")
    print("")
    
    for column in columns:
        print('=' * col_width, end=" ")
    print("")

    for row in rows:
        for col in columns:
            print(col_string.format(row[col]), end=" ")
        print("")

    if timer != 0:
        print('%d rows returned in %f seconds.' % (len(rows), timer))
    else:
        print('%d rows returned.' % len(rows))
