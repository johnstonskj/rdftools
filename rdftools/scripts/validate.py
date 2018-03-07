import i18n
import sys

import rdftools


def main():
    (LOG, cmd) = rdftools.startup('RDF file validator.', add_args=None)

    for input in cmd.input:
        LOG.info(i18n.t('scripts.validate_started', name=input))
        try:
            rdftools.read(input, cmd.read)
            LOG.info(i18n.t('scripts.validate_succeeded'))
        except:  # noqa: E722
            LOG.warning(i18n.t('scripts.validate_failed', exc_info=True))
            sys.exit(1)
