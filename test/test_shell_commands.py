import pytest

import rdftools
from rdftools.scripts import shell
from test.sample_data import input_file, input_file_count

expected_commands = ['!', 'base', 'clear', 'close', 'connect', 'context',
                     'echo', 'exit', 'help', 'parse', 'predicates',
                     'prefix', 'prompt', 'query', 'serialize', 'show',
                     'subjects']

rdftools.configure_translation(force_locale='en')


def test_log_output(capsys):
    expected_out = [
        ('information message'),
        ('warning message'),
        ('error message'),
        ("exception message module 'rdftools.scripts.shell' has no attribute 'foo'",  # noqa: 501
         "exception message 'module' object has no attribute 'foo'"),
        ('')]
    log = rdftools.configure_logging('shell', 3)
    shell.LOG = log
    shell.info('information message')
    shell.warning('warning message')
    shell.error('error message')
    try:
        shell.foo()
    except AttributeError as ex:
        shell.exception('exception message', ex)
    (out, err) = capsys.readouterr()
    for num, line in enumerate(out.split('\n')):
        assert line in expected_out[num]


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

    assert 'graph' in shell.COMMANDS


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
    context = new_context()
    shell.prompt(context, prompt_str)
    assert context.prompt == '%s ' % prompt_str


def test_echo(capsys):
    echo_str = 'help!'
    shell.echo(None, echo_str)
    (out, err) = capsys.readouterr()
    assert out.strip() == echo_str


def test_line_parser(capsys):
    echo_str = 'help!'
    shell.parse_input_line(None, 'echo %s' % echo_str)
    (out, err) = capsys.readouterr()
    assert out.strip() == echo_str


def test_line_parser_unknown(capsys):
    shell.parse_input_line(None, 'unknown command, help!')
    (out, err) = capsys.readouterr()
    assert out.strip() == 'Warning, unknown command: unknown.'


def test_base(capsys):
    base_uri = '<http://example.org/stuff#>'
    context = new_context()
    assert context.base is None
    context = shell.base(context, base_uri)
    context = shell.base(context, '')
    (out, err) = capsys.readouterr()
    assert out.index('BASE %s' % base_uri) >= 0


bad_uris = [('http://ex.org'), ('<http://ex.org'), ('http://ex.org>')]


@pytest.mark.parametrize('uri', bad_uris)
def test_base_bad_uri(capsys, uri):
    context = new_context()
    context = shell.base(context, uri)
    (out, err) = capsys.readouterr()
    assert out.index('Warning') == 0


def test_prefix(capsys):
    prefix_str = 's: <http://example.org/stuff#>'
    context = new_context()
    context = shell.prefix(context, prefix_str)
    context = shell.prefix(context, '')
    (out, err) = capsys.readouterr()
    assert out.index(prefix_str) >= 0


bad_prefixes = [('s'), ('s*s:'), ('_:')]


@pytest.mark.parametrize('prefix', bad_prefixes)
def test_prefix_bad_prefix(capsys, prefix):
    context = new_context()
    context = shell.prefix(context, prefix + ' <http://example.org/stuff#>')
    (out, err) = capsys.readouterr()
    assert out.index('Warning') == 0


@pytest.mark.parametrize('uri', bad_uris)
def test_prefix_bad_uri(capsys, uri):
    context = new_context()
    context = shell.prefix(context, 'ex:' + uri)
    (out, err) = capsys.readouterr()
    assert out.index('Warning') == 0


def test_context(capsys):
    context = new_context()
    context = shell.base(context, '<http://example.org/stuff#>')
    context = shell.prefix(context, 'c: <http://example.org/concepts#>')
    context = shell.parse(context, input_file)
    context = shell.context(context, '')
    (out, err) = capsys.readouterr()
    assert out.index('BASE <http://example.org/stuff#>') >= 0
    assert out.index('PREFIX c: <http://example.org/concepts#>') >= 0
    assert out.index('size 25 statements') >= 0


def test_parse(capsys):
    context = new_context()
    context = shell.parse(context, input_file)
    assert len(context.graph) == input_file_count


def test_parse_bad_format(capsys):
    context = new_context()
    context = shell.parse(context, input_file + ' text')
    (out, err) = capsys.readouterr()
    assert out.index('Warning') == 0


def test_parse_no_file(capsys):
    context = new_context()
    context = shell.parse(context, input_file + '_noexist')
    (out, err) = capsys.readouterr()
    assert out.index('Error, unexpected problem reading file.') == 0


def test_serialize(tmpdir):
    expected_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
</rdf:RDF>
"""
    p = tmpdir.mkdir("tests").join("sample_out.xml")
    context = new_context()
    context = shell.serialize(context, str(p) + ' xml')
    written = p.read()
    assert written == expected_xml


def test_serialize_bad_file(capsys, tmpdir):
    p = tmpdir.mkdir("tests").join("/dir/doesnt/exist/sample_out.xml")
    context = new_context()
    context = shell.serialize(context, str(p) + ' xml')
    (out, err) = capsys.readouterr()
    assert out.index('Error, unexpected problem writing file.') == 0


def test_show(capsys):
    context = new_context()
    context = shell.parse(context, input_file)
    context = shell.show(context, 'nt')
    (out, err) = capsys.readouterr()
    lines = [line for line in out.split('\n')[1:] if not line == '']
    assert len(lines) == input_file_count
    for line in lines:
        if not line == '':
            assert line.startswith('<')
            assert line.endswith('> .')


queries = [
    ('SELECT DISTINCT ?type WHERE { ?s a ?type }',
     'type', 3),
    ('SELECT DISTINCT ?person ?topic WHERE { ?person <http://example.org/social/relationship/1.0/likes> ?topic. } ORDER BY ?person',  # noqa: 501
     'person,topic', 3)
]


@pytest.mark.parametrize('query, cols, rows', queries)
def test_query(capsys, query, cols, rows):
    context = new_context()
    context = shell.parse(context, input_file)
    context = shell.query(context, query)
    (out, err) = capsys.readouterr()
    lines = [line for line in out.split('\n')[1:] if not line == '']
    header = [col.strip() for col in lines[0].split('|')
              if not col.strip() == '']
    assert set(header) == set(cols.split(','))
    assert set(lines[1]) == {'|', '='}
    assert lines[-1].startswith('%d rows returned' % rows)


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
