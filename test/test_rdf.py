import pytest
from unittest.mock import patch

from rdftools.scripts import rdf


def test_rdf_script(capfd):
    # We use capfd, not capsys, because the output we want to capture comes
    # from the subprocess spawned by rdf, not rdf itself.
    expected_out = 'usage: rdf-query [-h] [-v] [-b BASE] [-i [INPUT [INPUT ...]]]'  # noqa: 501
    with patch('sys.argv',
               ['test_rdf', '-v', 'query', '-h']):
        rdf.main()
        (out, err) = capfd.readouterr()
        assert out.startswith(expected_out)


expected_err = """usage: test_rdf [-h] [-v] {validate,convert,select,shell,query} ...
test_rdf: error: argument command: invalid choice: 'foobar' (choose from 'validate', 'convert', 'select', 'shell', 'query')
"""  # noqa: 501


def test_rdf_script_bad_command(capsys):
    with patch('sys.argv',
               ['test_rdf', 'foobar', '-h']):
        try:
            rdf.main()
            pytest.fail('expecting: %s' % expected_err)
        except SystemExit:
            (out, err) = capsys.readouterr()
            assert err == expected_err
