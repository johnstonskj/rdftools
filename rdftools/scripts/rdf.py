from subprocess import call

import rdftools

COMMANDS = ['validate', 'convert', 'select', 'shell', 'query']


def commands():
    import argparse
    parser = argparse.ArgumentParser(description='RDF tool')
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('subargs', nargs=argparse.REMAINDER)
    return (parser.prog, parser.parse_args())


def main():
    (process, cmd) = commands()
    LOG = rdftools.configure_logging(process, cmd.verbose)
    LOG.debug(cmd)

    LOG.info('Running command %s with args %s' % (cmd.command, cmd.subargs))
    process = ['rdf-' + cmd.command]
    if cmd.verbose > 0:
        process.append('-' + 'v' * 3)

    call(process + cmd.subargs)
