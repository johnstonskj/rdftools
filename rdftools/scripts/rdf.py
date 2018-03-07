import i18n
from subprocess import call

import rdftools

COMMANDS = ['validate', 'convert', 'select', 'shell', 'query']


def commands():
    import argparse
    parser = argparse.ArgumentParser(description=i18n.t('scripts.rdf_command'))
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('subargs', nargs=argparse.REMAINDER)
    return (parser.prog, parser.parse_args())


def main():
    rdftools.configure_translation()
    (process, cmd) = commands()
    LOG = rdftools.configure_logging(process, cmd.verbose)
    LOG.debug(cmd)

    LOG.info(i18n.t('scripts.rdf_call', name=cmd.command, params=cmd.subargs))
    process = ['rdf-' + cmd.command]
    if cmd.verbose > 0:
        process.append('-' + 'v' * cmd.verbose)

    call(process + cmd.subargs)
