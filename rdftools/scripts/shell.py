import atexit
from collections import namedtuple
import rdflib
import os
import os.path
import pprint
import readline
import subprocess
import sys
from timeit import default_timer as timer

import rdftools

WELCOME = 'RDF Shell, v0.1.0.'
COMMANDS = {}

def add_command(command, name=None):
    if name is None:
        name = command.__name__
    COMMANDS[name] = command

def command_completer(text, index):
    possibles = [command for command in COMMANDS.keys() if command.startswith(text)]
    if index < len(possibles):
        return possibles[index]
    else:
        return None

def base(context, args):
    """ base [URI]
        Set the base URI to be used when parsing model files."""
    args2 = args.strip().split()
    if len(args2) == 0:
        if not context['base'] is None:
            print('BASE %s' % context['base'])
    elif len(args2) >= 1:
        uri = args2[0].strip()
        if uri.startswith('<') and uri.endswith('>'):
            context['base'] = uri
        else:
            print('URI must be enclosed in <>')
    return context
add_command(base)

def prefix(context, args):
    """ prefix [pre: URI]
        Set a prefix to represent a URI."""
    args2 = args.strip().split()
    if len(args2) == 0:
        for (pre, uri) in context['graph'].namespaces():
            print('PREFIX %s: %s' % (pre, uri))
    elif len(args2) == 2:
        pre = args2[0].strip()
        if pre.endswith(':'):
            pre = pre[:-1] # TODO check for ''?
            uri = args2[1].strip()
            context['graph'].bind(pre, uri)
        else:
            print('prefix must end with ":"')
    else:
        print('expecting 2 arguments')            
    return context
add_command(prefix)

SimpleFile = namedtuple('SimpleFile', ['name'])

def parse(context, args):
    """ parse filename [format=n3]
        Read a file into the current context graph."""
    args2 = args.strip().split()
    format = 'n3'
    if len(args2) >= 2:
        format = args2[1].strip()
        if not format in rdftools.FORMATS:
            print('format %s, not known!' % format)
    if len(args2) >= 1:
        try:
            context['graph'] = rdftools.read_into(SimpleFile(args2[0]), format, context['graph'], context['base'])
            print('Graph updated with %d statements.' % len(context['graph']))
        except:
            print("Unexpected error:", sys.exc_info()[1])
    else:
        print('invalid parameters')
    return context
add_command(parse)

def serialize(context, args):
    """ serialize filename [format=n3]
        Write the current context graph into a file."""
    args2 = args.strip().split()
    format = 'n3'
    if len(args2) >= 2:
        format = args2[1].strip()
        if not format in rdftools.FORMATS:
            print('format %s, not known!' % format)
    if len(args2) >= 1:
        try:
            rdftools.write(context['graph'], SimpleFile(args2[0]), format)
            print('file %s written' % args2[0])
        except:
            print("Unexpected error:", sys.exc_info()[1])
    else:
        print('invalid parameters')
    return context
add_command(serialize)

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
                print('select returned no results.')
        elif sparql[:3].upper() == 'ASK':
            print('ask returned %s.' % bool(results))
        # construct and describe return statements
        # update returns?
        else:
            print(results);
    else:
        print('no query (SELECT, ASK, DESCRIBE, CONSTRUCT, UPDATE) specified!')
    return context
add_command(query)

def subjects(context, ignored):
    """ subjects
        Display subjects in current context."""
    for s in set(context['graph'].subjects()):
        print(s)
    return context
add_command(subjects)

def predicates(context, ignored):
    """ predicates
        Display predicates in current context."""
    for p in set(context['graph'].predicates()):
        print(p)
    return context
add_command(predicates)

def connect(context, uri):
    """ connect URI
        Connect to a store (TBD)."""
    print('TODO: finish me')
    return context
add_command(connect)

def close(context, ignored):
    """ close
        Close the current store connection, if one exists."""
    print('TODO: finish me')
    return context
add_command(close)

def context(context, ignored):
    """ context
        Display the current context."""
    print('BASE %s' % context['base'])
    for (pre, uri) in context['graph'].namespaces():
        print('PREFIX %s: %s' % (pre, uri))
    print('')
    print('Graph       ID %s' % context['graph']._Graph__identifier)
    print('         store %s' % context['graph']._Graph__store)
    print('context aware? %s' % context['graph'].context_aware)
    print('formula aware? %s' % context['graph'].formula_aware)
    print('default union? %s' % context['graph'].default_union)
    print('')
    return context
add_command(context)

def clear(context, args):
    """ clear [base | prefix pre: URI]
        Clear the current context."""
    return {'base': None, 'graph': rdflib.Graph()}
add_command(clear)

def exec_command(context, args):
    """ ! [command]
        Execute a command in a sub-shell."""
    subprocess.call(args, shell=True)
    return context
add_command(exec_command, '!')

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
            print(' %s' % cmd)
        else:
            print(text)
    return context
add_command(help)

def exit(context, args):
    """ exit
        Exit the shell."""
    pass
add_command(exit)

def prompt(context, args):
    """ prompt text
        Set the prompt used in the shell."""
    global PROMPT
    PROMPT = args + ' '
    return context
add_command(prompt)

def configure_readline():
    histfile = os.path.join(os.path.expanduser("~"), ".rdfsh_hist")
    if not os.path.exists(histfile):
        with open(histfile, 'w'): pass    
    try:
        readline.set_completer(command_completer)
        readline.parse_and_bind("tab: complete")
        readline.read_history_file(histfile)
        atexit.register(readline.write_history_file, histfile)
    except IOError as e:
        print('readline configuration exception: %s' % e)

def parse_rcfile(context):
    rcfile = os.path.join(os.path.expanduser("~"), ".rdfshrc")
    if os.path.exists(rcfile):
        file = open(rcfile, 'rt')
        for line in file:
            parse_input_line(context, line)
        file.close()

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
            print('Unknown command: %s' % cmd)
    return context

PROMPT = '> '

def run_loop(context):
    while True:
        try:
            input_line = input(PROMPT)
            if input_line.strip() == 'exit':
                close(context, None)
                clear(context, None)
                sys.exit(0)
            context = parse_input_line(context, input_line)
        except EOFError:
            break


def main():
    (LOG, cmd) = rdftools.startup('RDF/SPARQL shell.', add_args=None)
    print(WELCOME)
    configure_readline()
    context = clear(None, None)
    parse_rcfile(context)
    run_loop(context)
