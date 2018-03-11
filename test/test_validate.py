import pytest
from unittest.mock import patch

from rdftools.scripts import validate
from test.sample_data import input_file


def test_validate_success(capsys):
    with patch('sys.argv',
               ['test_validate', '-i', input_file, '-r', 'n3']):
        validate.main()


def test_validate_fail(capsys):
    with patch('sys.argv',
               ['test_validate', '-i', __file__, '-r', 'n3']):
        try:
            validate.main()
            pytest.fail('expecting to sys.exit with failure')
        except SystemExit as ex:
            assert ex.code == 1
