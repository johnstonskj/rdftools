import pytest

import rdftools
from rdftools.scripts import shell
from test.sample_data import input_file

expected_commands = ['!', 'base', 'clear', 'close', 'connect', 'context',
                     'echo', 'exit', 'help', 'parse', 'predicates',
                     'prefix', 'prompt', 'query', 'serialize', 'show',
                     'subjects']

rdftools.configure_translation(force_locale='en')


def new_context():
    return shell.clear(None, '')


@pytest.mark.parametrize('command', expected_commands)
def test_command_added(command):
    assert command in shell.COMMANDS


def test_add_command():
    @shell.command
    def graph(context, args):
        """ graph name
            Return the contents of a named graph."""
        return context

    assert 'graph in shell.COMMANDS'


def test_renamed_command():
    assert '!' in shell.COMMANDS
    assert 'exec_command' not in shell.COMMANDS


def test_command_help(capsys):
    shell.help(None, 'clear')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == """ clear [base | prefix pre:]
        Clear the current context."""


def test_command_help_none(capsys):
    shell.help(None, 'foo')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == ''


expected_possibles = [
    (0, 'clear'),
    (1, 'close'),
    (2, 'connect'),
    (3, 'context'),
    (4, None)
]


@pytest.mark.parametrize('index, text', expected_possibles)
def test_command_completion(index, text):
    possibles = shell.command_completer('c', index)
    assert possibles == text


def test_prompt():
    prompt_str = '$test$'
    shell.prompt(None, prompt_str)
    assert shell.PROMPT == '%s ' % prompt_str


def test_echo(capsys):
    echo_str = 'help!'
    shell.echo(None, echo_str)
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == echo_str


def test_line_parser(capsys):
    echo_str = 'help!'
    shell.parse_input_line(None, 'echo %s' % echo_str)
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == echo_str


def test_line_parser_unknown(capsys):
    shell.parse_input_line(None, 'unknown command, help!')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == 'Warning, unknown command: unknown.'


def test_base(capsys):
    base_uri = '<http://example.org/stuff#>'
    context = new_context()
    assert context['base'] is None
    context = shell.base(context, base_uri)
    context = shell.base(context, '')
    (out, err) = capsys.readouterr()
    assert out.index('BASE %s' % base_uri) >= 0


@pytest.mark.skip(reason='TODO')
def test_base_bad_uri():
    pass


def test_prefix(capsys):
    prefix_str = 's: http://example.org/stuff#'
    context = new_context()
    context = shell.prefix(context, prefix_str)
    context = shell.prefix(context, '')
    (out, err) = capsys.readouterr()
    assert out.index(prefix_str) >= 0


@pytest.mark.skip(reason='TODO')
def test_prefix_bad_prefix():
    pass


@pytest.mark.skip(reason='TODO')
def test_prefix_bad_uri():
    pass


def test_parse(capsys):
    context = new_context()
    context = shell.parse(context, input_file)
    assert len(context['graph']) == 25


@pytest.mark.skip(reason='TODO')
def test_parse_bad_format():
    pass


def test_subjects(capsys):
    context = new_context()
    context = shell.parse(context, input_file)
    context = shell.subjects(context, '')
    (out, err) = capsys.readouterr()
    # Skip first line (result of parse) and last line (blank)
    subjects = out.split('\n')[1:-1]
    assert len(subjects) == 11
    for subject in subjects:
        assert subject.startswith('http://example.org/social/')


def test_predicates(capsys):
    context = new_context()
    context = shell.parse(context, input_file)
    context = shell.predicates(context, '')
    (out, err) = capsys.readouterr()
    # Skip first line (result of parse) and last line (blank)
    predicates = out.split('\n')[1:-1]
    assert len(predicates) == 6
    for predicate in predicates[:-1]:
        assert (predicate.startswith('http://example.org/social/') or
                predicate == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
