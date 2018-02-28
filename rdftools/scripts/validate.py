import sys

import rdftools

def main():
    (LOG, cmd) = rdftools.startup('RDF file validator.', add_args=None)

    for input in cmd.input:
        LOG.info('Validating file %s' % input)
        try:
            graph = rdftools.read(input, cmd.read)
            LOG.info('File validated successfully')
        except:
            LOG.warning('File validation failed', exc_info=True)
            sys.exit(1)
