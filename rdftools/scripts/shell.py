import atexit
from collections import namedtuple
import rdflib
import os
import os.path
import readline
import subprocess
import sys
from timeit import default_timer as timer

import rdftools

WELCOME = 'RDF Tools shell. Version %s' % rdftools.__VERSION__
COMMANDS = {}


def info(text):
    print(text)


def warning(text):
    print('Warning. %s' % text)


def error(text):
    print('Error. %s' % text)


def exception(text, ex=None):
    if ex is None:
        error('%s %s: %s' % (text, sys.exc_info()[0], sys.exc_info()[1]))
        # LOG.exception(sys.exc_info()[2])
    else:
        error('%s. %s' % (text, ex))


def command(name_or_func):
    cmdname = None

    def decorator(func):
        COMMANDS[cmdname] = func

        def wrapper(context, args):
            return func(context, args)
        return wrapper

    if callable(name_or_func):
        cmdname = name_or_func.__name__
        return decorator(name_or_func)
    else:
        cmdname = name_or_func
        return decorator


def command_completer(text, index):
    possibles = [command for command in COMMANDS.keys()
                 if command.startswith(text)]
    if index < len(possibles):
        return possibles[index]
    else:
        return None


@command
def base(context, args):
    """ base [URI]
        Set the base URI to be used when parsing model files."""
    args2 = args.strip().split()
    if len(args2) == 0:
        if not context['base'] is None:
            info('BASE %s' % context['base'])
    elif len(args2) >= 1:
        uri = args2[0].strip()
        if uri.startswith('<') and uri.endswith('>'):
            context['base'] = uri
        else:
            warning('URI must be enclosed in <>')
    return context


@command
def prefix(context, args):
    """ prefix [pre: URI]
        Set a prefix to represent a URI."""
    args2 = args.strip().split()
    if len(args2) == 0:
        for (pre, uri) in context['graph'].namespaces():
            info('PREFIX %s: %s' % (pre, uri))
    elif len(args2) == 2:
        pre = args2[0].strip()
        if pre.endswith(':'):
            # TODO check for '?'
            pre = pre[:-1]
            uri = args2[1].strip()
            context['graph'].bind(pre, uri)
        else:
            warning('prefix must end with ":"')
    else:
        warning('expecting 2 arguments')
    return context


SimpleFile = namedtuple('SimpleFile', ['name'])


@command
def parse(context, args):
    """ parse filename [format=n3]
        Read a file into the current context graph."""
    args2 = args.strip().split()
    format = 'n3'
    if len(args2) >= 2:
        format = args2[1].strip()
        if format not in rdftools.FORMATS:
            warning('format %s, not known!' % format)
    if len(args2) >= 1:
        try:
            context['graph'] = rdftools.read_into(
                SimpleFile(args2[0]), format,
                context['graph'], context['base'])
            info('Graph updated with %d statements.' % len(context['graph']))
        except:  # noqa: E722
            exception('Parsing error')
    else:
        warning('invalid parameters')
    return context


@command
def serialize(context, args):
    """ serialize filename [format=n3]
        Write the current context graph into a file."""
    args2 = args.strip().split()
    format = 'n3'
    if len(args2) >= 2:
        format = args2[1].strip()
        if format not in rdftools.FORMATS:
            warning('format %s, not known!' % format)
    if len(args2) >= 1:
        try:
            rdftools.write(context['graph'], SimpleFile(args2[0]), format)
            info('file %s written' % args2[0])
        except:  # noqa: E722
            exception("Unexpected error:")
    else:
        warning('invalid parameters')
    return context


@command
def show(context, args):
    """ show format=n3
        Display current context graph in format."""
    args2 = args.strip().split()
    format = 'n3'
    if len(args2) == 1:
        format = args2[0].strip()
        if format not in rdftools.FORMATS:
            warning('format %s, not known' % format)
            format = 'n3'
    rdftools.write(context['graph'], None, format)
    return context


QUERY_FORMS = ['SELECT', 'ASK', 'DESCRIBE', 'CONSTRUCT', 'UPDATE']


@command
def query(context, args):
    """ query sparql
        Run SPARQL query."""
    sparql = args.strip()
    if len(sparql) > 6:
        start = timer()
        results = context['graph'].query(sparql)
        end = timer()
        if sparql[:6].upper() == 'SELECT':
            if len(results) > 0:
                columns = results.bindings[0].keys()
                rdftools.report(columns, results,  end - start)
            else:
                info('select returned no results.')
        elif sparql[:3].upper() == 'ASK':
            info('ask returned %s.' % bool(results))
        # construct and describe return statements
        # update returns?
        else:
            info(results)
    else:
        warning('no valid query specified (%s)',
                ', '.join(QUERY_FORMS))
    return context


@command
def subjects(context, ignored):
    """ subjects
        Display subjects in current context."""
    for s in set(context['graph'].subjects()):
        info(s)
    return context


@command
def predicates(context, ignored):
    """ predicates
        Display predicates in current context."""
    for p in set(context['graph'].predicates()):
        info(p)
    return context


@command
def connect(context, uri):
    """ connect URI
        Connect to a store (TBD)."""
    warning('TODO: finish me')
    return context


def is_open(context):
    return False


@command
def close(context, ignored):
    """ close
        Close the current store connection, if one exists."""
    warning('TODO: finish me')
    return context


@command
def context(context, ignored):
    """ context
        Display the current context."""
    if not context['base'] is None:
        info('BASE %s' % context['base'])
    for (pre, uri) in context['graph'].namespaces():
        info('PREFIX %s: %s' % (pre, uri))
    info('')
    info('Graph        ID %s' % context['graph']._Graph__identifier)
    info('|         store %s' % context['graph']._Graph__store)
    info('|          size %d statements' % len(context['graph']))
    info('|context aware? %s' % context['graph'].context_aware)
    info('|formula aware? %s' % context['graph'].formula_aware)
    info('|default union? %s' % context['graph'].default_union)
    info('')
    return context


@command
def clear(context, args):
    """ clear [base | prefix pre:]
        Clear the current context."""
    # TODO: clear base/prefix
    return {'base': None, 'graph': rdflib.Graph()}


@command('!')
def exec_command(context, args):
    """ ! [command]
        Execute a command in a sub-shell."""
    subprocess.call(args, shell=True)
    return context


@command
def help(context, args):
    """ help [command]
        Display help on built-in shell commands."""
    keys = sorted(COMMANDS.keys())
    if len(args) > 0:
        # TODO: validate args
        keys = [args]
    for cmd in keys:
        text = COMMANDS[cmd].__doc__
        if text is None:
            info(' %s' % cmd)
        else:
            info(text)
    return context


@command
def exit(context, args):
    """ exit
        Exit the shell."""
    pass


@command
def echo(context, args):
    """ echo text
        Echo back the following text."""
    info(args)
    return context


@command
def prompt(context, args):
    """ prompt text
        Set the prompt used in the shell."""
    global PROMPT
    PROMPT = args + ' '
    return context


def configure_readline():
    histfile = os.path.join(os.path.expanduser("~"), ".rdfsh_hist")
    if not os.path.exists(histfile):
        with open(histfile, 'w'):
            pass
    try:
        readline.set_completer(command_completer)
        readline.parse_and_bind("tab: complete")
        readline.read_history_file(histfile)
        atexit.register(readline.write_history_file, histfile)
    except IOError as e:
        exception('readline configuration exception', e)


def parse_cmdfile(context, filename):
    if os.path.exists(filename):
        info('reading commands from file %s' % filename)
        file = open(filename, 'rt')
        for line in file:
            parse_input_line(context, line)
        file.close()
    else:
        warning('file named %s does not exist' % filename)


def parse_input_line(context, line):
    line = line.strip()
    if line != '':
        space = line.find(' ')
        if space > 0:
            cmd = line[:space]
            line = line[space+1:]
        else:
            cmd = line
            line = ''
        if cmd in COMMANDS:
            context = COMMANDS[cmd](context, line)
        else:
            warning('Unknown command: %s' % cmd)
    return context


PROMPT = '> '


def run_loop(context):
    while True:
        try:
            input_line = input(PROMPT)
            if input_line.strip() == 'exit':
                if is_open(context):
                    close(context, None)
                clear(context, None)
                sys.exit(0)
            context = parse_input_line(context, input_line)
        except EOFError:
            break


def main():
    global LOG
    (LOG, cmd) = rdftools.startup('RDF/SPARQL shell.',
                                  add_args=None, read_files=False)
    info(WELCOME)
    configure_readline()
    context = clear(None, None)
    context['base'] = cmd.base
    parse_cmdfile(context, os.path.join(os.path.expanduser("~"), ".rdfshrc"))
    run_loop(context)
