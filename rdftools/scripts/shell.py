import atexit
from collections import namedtuple
import i18n
import rdflib
import os
import os.path
import readline
import subprocess
import sys
from termcolor import colored, cprint
from timeit import default_timer as timer

import rdftools

SPACE = ' '
BLANK_LINE = ''
QUERY_FORMS = ['SELECT', 'ASK', 'DESCRIBE', 'CONSTRUCT', 'UPDATE']

LOG = None
COMMANDS = {}


SimpleFile = namedtuple('SimpleFile', ['name'])


class ShellContext(object):

    def __init__(self):
        self.prompt = '>>> '
        self.base = None
        self.graph = rdflib.Graph()


def info(text):
    print(text)


def warning(text):
    if LOG is not None:
        LOG.warning(text)
    if rdftools.USE_COLOR:
        cprint(text, 'yellow')
    else:
        print(text)


def error(text):
    if LOG is not None:
        LOG.error(text)
    if rdftools.USE_COLOR:
        cprint(text, 'red')
    else:
        print(text)


def exception(text, ex=None):
    if LOG is not None:
        LOG.exception(text, ex)
    if ex is None:
        error('%s %s: %s' % (text, sys.exc_info()[0], sys.exc_info()[1]))
        # LOG.exception(sys.exc_info()[2])
    else:
        error('%s %s' % (text, ex))


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
    possibles = sorted([command for command in COMMANDS.keys()
                        if command.startswith(text)])
    if index < len(possibles):
        return possibles[index]
    else:
        return None


def parse_uri(uri):
    if uri.startswith('<') and uri.endswith('>'):
        return uri[1:-1]
    else:
        warning(i18n.t('shell.invalid_uri'))
        return None


@command
def base(context, args):
    """ base [URI]
        Set the base URI to be used when parsing model files."""
    args2 = args.strip().split()
    if len(args2) == 0:
        if context.base is not None:
            if rdftools.USE_COLOR:
                info('BASE <%s>' % colored(context.base, attrs=['underline']))
            else:
                info('BASE <%s>' % context.base)
    elif len(args2) >= 1:
        base = parse_uri(args2[0].strip())
        if base is not None:
            context.base = base
    return context


def parse_prefix(pre):
    if pre.endswith(':'):
        pre = pre[:-1]
        if pre == '' or pre.isalnum():
            return pre
        else:
            warning(i18n.t('shell.invalid_prefix_char'))
    else:
        warning(i18n.t('shell.invalid_prefix'))
    return None


@command
def prefix(context, args):
    """ prefix [pre: URI]
        Set a prefix to represent a URI."""
    args2 = args.strip().split()
    if len(args2) == 0:
        for (pre, uri) in context.graph.namespaces():
            if rdftools.USE_COLOR:
                info('PREFIX %s: <%s>.' %
                     (colored(pre, attrs=['bold']),
                      colored(uri, attrs=['underline'])))
            else:
                info('PREFIX %s: <%s>.' % (pre, uri))
    elif len(args2) == 2:
        pre = parse_prefix(args2[0].strip())
        if pre is not None:
            uri = parse_uri(args2[1].strip())
            context.graph.bind(pre, uri)
    else:
        warning(i18n.t('shell.invalid_param_num', count=2))
    return context


def get_format(args, place=2):
    format = 'n3'
    if len(args) >= place:
        _format = args[place-1].strip()
        if _format in rdftools.FORMATS:
            format = _format
        else:
            warning(i18n.t('shell.invalid_format', format=_format))
    return format


@command
def parse(context, args):
    """ parse filename [format=n3]
        Read a file into the current context graph."""
    args2 = args.strip().split()
    format = get_format(args2)
    if len(args2) >= 1:
        try:
            context.graph = rdftools.read_into(
                SimpleFile(args2[0]), format,
                context.graph, context.base)
            info(i18n.t('shell.graph_updated', len=len(context.graph)))
        except SyntaxError as ex:
            error(i18n.t('shell.file_read_err', err=ex))
        except IOError as ex:
            error(i18n.t('shell.file_read_err', err=ex))
    else:
        warning(i18n.t('shell.invalid_params'))
    return context


@command
def serialize(context, args):
    """ serialize filename [format=n3]
        Write the current context graph into a file."""
    args2 = args.strip().split()
    format = get_format(args2)
    if len(args2) >= 1:
        try:
            rdftools.write(context.graph, SimpleFile(args2[0]), format)
        except IOError as ex:
            exception(i18n.t('shell.file_write_err', err=ex))
    else:
        warning(i18n.t('shell.invalid_params'))
    return context


@command
def show(context, args):
    """ show format=n3
        Display current context graph in format."""
    args2 = args.strip().split()
    format = get_format(args2, place=1)
    rdftools.write(context.graph, None, format)
    return context


@command
def query(context, args):
    """ query sparql
        Run SPARQL query."""
    sparql = args.strip()
    if len(sparql) > 6:
        start = timer()
        results = context.graph.query(sparql)
        end = timer()
        if sparql[:6].upper() == 'SELECT':
            if len(results) > 0:
                columns = results.bindings[0].keys()
                rdftools.report(columns, results,  end - start)
            else:
                info(i18n.t('shell.query_no_results'))
        elif sparql[:3].upper() == 'ASK':
            info(i18n.t('shell.ask_results'), results=bool(results))
        # construct and describe return statements
        # update returns?
        else:
            info(results)
    else:
        warning(i18n.t('shell.query_form_err'), forms=', '.join(QUERY_FORMS))
    return context


def graph_select(context, component):
    for s in set(getattr(context.graph, component)()):
        info(s)
    return context


@command
def subjects(context, ignored):
    """ subjects
        Display subjects in current context."""
    return graph_select(context, 'subjects')


@command
def predicates(context, ignored):
    """ predicates
        Display predicates in current context."""
    return graph_select(context, 'predicates')


@command
def connect(context, uri):
    """ connect URI
        Connect to a store (TBD)."""
    warning(i18n.t('shell.to_do'))
    return context


def is_open(context):
    return False


@command
def close(context, ignored):
    """ close
        Close the current store connection, if one exists."""
    warning(i18n.t('shell.to_do'))
    return context


@command
def context(context, ignored):
    """ context
        Display the current context."""
    context = base(context, BLANK_LINE)
    context = prefix(context, BLANK_LINE)
    info(BLANK_LINE)
    # TODO: i18n the block below.
    info('Graph        ID %s' % context.graph._Graph__identifier)
    info('|          type %s' % type(context.graph).__name__)
    info('|         store %s' % context.graph._Graph__store)
    info('|          size %d statements' % len(context.graph))
    info('|context aware? %s' % context.graph.context_aware)
    info('|formula aware? %s' % context.graph.formula_aware)
    info('|default union? %s' % context.graph.default_union)
    info(BLANK_LINE)
    return context


@command
def clear(context, args):
    """ clear [base | prefix pre:]
        Clear the current context."""
    return ShellContext()


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
        if cmd in COMMANDS:
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
    if not args == '':
        context.prompt = args + SPACE
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
        exception(i18n.t('shell.readline_err'), e)


def parse_cmdfile(context, filename):
    if os.path.exists(filename):
        info(i18n.t('shell.read_file', name=filename))
        file = open(filename, 'rt')
        for line in file:
            parse_input_line(context, line)
        file.close()


def parse_input_line(context, line):
    line = line.strip()
    if line != BLANK_LINE:
        space = line.find(SPACE)
        if space > 0:
            cmd = line[:space]
            line = line[space+1:]
        else:
            cmd = line
            line = BLANK_LINE
        if cmd in COMMANDS:
            context = COMMANDS[cmd](context, line)
        else:
            warning(i18n.t('shell.unknown_cmd', command=cmd))
    return context


def run_loop(context):
    while True:
        try:
            input_line = input(context.prompt)
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
    (LOG, cmd) = rdftools.startup('shell.command',
                                  add_args=None, read_files=False)
    info(i18n.t('shell.welcome', version=rdftools.__VERSION__))
    configure_readline()
    context = clear(None, None)
    context.base = cmd.base
    parse_cmdfile(context, os.path.join(os.path.expanduser("~"), ".rdfshrc"))
    run_loop(context)
