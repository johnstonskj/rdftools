import os
import pytest
from unittest.mock import patch

from rdftools.scripts import query

sample_file = os.path.join(os.path.dirname(__file__), 'data/sample.n3')

expected_out = sorted([
    'http://example.org/social/profile/1.0/Person',
    'http://example.org/social/topics/1.0/Topic',
    'http://example.org/social/profile/1.0/Family',
])


def test_query_script(capsys):
    with patch('sys.argv',
               ['test_query', '-i', sample_file, '-r', 'n3', '-q',
                'SELECT DISTINCT ?type WHERE { ?s a ?type }']):
        query.main()
        (out, err) = capsys.readouterr()
        out_lines = sorted([line for line in out.split('\n')
                            if line.startswith('http://')])
        assert len(out_lines) == len(expected_out)
        for (index, line) in enumerate(expected_out):
            assert out_lines[index].startswith(line)


def test_query_script_empty(capsys):
    expected = "query returned no results."
    with patch('sys.argv',
               ['test_convert', '-i', sample_file, '-r', 'n3', '-q',
                'SELECT DISTINCT ?type WHERE { ?s a <http://example.org/people/me> }']):  # noqa: 501
        query.main()
        (out, err) = capsys.readouterr()
        assert out.index(expected) >= 0


def test_query_script_bad_sparql(capsys):
    import pyparsing
    expected_err = "Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}"  # noqa: 501
    with patch('sys.argv',
               ['test_convert', '-i', sample_file, '-r', 'n3', '-q',
                'WHAT IS SPARQL?']):
        try:
            query.main()
            pytest.fail('expecting: %s' % expected_err)
        except pyparsing.ParseException as ex:
            assert str(ex).index(expected_err) >= 0
