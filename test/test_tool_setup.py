import pytest

import rdftools


@pytest.fixture
def translator():
    def reset():
        import i18n
        i18n.load_path = []

    yield reset()
    pass


def test_configure_translation(translator):
    rdftools.configure_translation()
    import i18n
    import locale
    # Ensure the messages files are added to the path
    assert len(i18n.load_path) == 1
    assert i18n.load_path[-1].endswith('rdftools/messages')
    # Ensure the locale is picked up from the system
    (lang, encoding) = locale.getlocale()
    assert lang.startswith(i18n.get('locale'))
    # Ensure the translation actually works!
    import sys
    name = sys._getframe().f_code.co_name
    assert i18n.t('test.test_case', name=name) == 'test %s?' % name


def test_configure_translation_forced(translator):
    rdftools.configure_translation(force_locale='tv')
    # Ensure we override the default system locale
    import i18n
    assert len(i18n.load_path) == 1
    assert i18n.get('locale') == 'tv'
    assert i18n.get('fallback') == 'en'


def test_configure_logging():
    logger = rdftools.configure_logging(name='test', level=2)
    import logging
    assert logger.getEffectiveLevel() == logging.DEBUG


def test_configure_argparse():
    parser = rdftools.configure_argparse('My Test', read_files=False)
    assert parser.description == 'My Test'
    command = parser.parse_args(['-vvv', '-b', 'http://example.org'])
    assert command.verbose == 3
    assert command.base == 'http://example.org'
    try:
        assert command.input is None
        pytest.fail('command object should have no attribute "input"')
    except AttributeError:
        pass


def test_configure_argparse_read():
    parser = rdftools.configure_argparse('My Test', read_files=True)
    assert parser.description == 'My Test'
    command = parser.parse_args(['-vvv', '-b', 'http://example.org',
                                 '-i', 'README.md', '-r', 'n3'])
    assert command.verbose == 3
    assert command.base == 'http://example.org'
    assert len(command.input) == 1
    assert command.input[0].name == 'README.md'
    assert command.read == 'n3'


def test_startup(translator):
    def add_args(parser):
        parser.add_argument('-q', '--query', action='store')
        return parser

    (log, cmd) = rdftools.startup('test.command', add_args,
                                  argv=['-vvv', '-b', 'http://example.org',
                                        '-q', 'select'])
    assert log is not None
    assert cmd is not None
