import pytest

import rdftools
from rdftools.scripts import shell

expected_commands = ['!', 'base', 'clear', 'close', 'connect', 'context',
                     'echo', 'exit', 'help', 'parse', 'predicates',
                     'prefix', 'prompt', 'query', 'serialize', 'show',
                     'subjects']


rdftools.configure_translation(force_locale='en')


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
    shell.prompt(None, '$test$')
    assert shell.PROMPT == '$test$ '


def test_echo(capsys):
    shell.echo(None, 'help!')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == 'help!'


def test_line_parser(capsys):
    shell.parse_input_line(None, 'echo help!')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == 'help!'


def test_line_parser_unknown(capsys):
    shell.parse_input_line(None, 'unknown help!')
    (out, err) = capsys.readouterr()
    out = out[:-1]  # Remove trailing \n
    assert out == 'Warning, unknown command: unknown.'
