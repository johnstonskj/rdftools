import pytest
from unittest.mock import patch

from rdftools.scripts import convert
from test.sample_data import input_file

sample_triples = sorted([
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/parent> <http://example.org/social/people/1.0/Carol> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Dave> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Heidi> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/spouse> <http://example.org/social/people/1.0/Alice> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/likes> <http://example.org/social/topics/1.0/Diving> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/child> <http://example.org/social/people/1.0/Heidi> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/member> <http://example.org/social/people/1.0/OurFamily> .',  # noqa: 501
    '<http://example.org/social/topics/1.0/Diving> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/topics/1.0/Topic> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/child> <http://example.org/social/people/1.0/Eve> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Heidi> <http://example.org/social/relationship/1.0/member> <http://example.org/social/people/1.0/OurFamily> .',  # noqa: 501
    '<http://example.org/social/people/1.0/OurFamily> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Family> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Grace> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Frank> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Carol> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/likes> <http://example.org/social/topics/1.0/Diving> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/parent> <http://example.org/social/people/1.0/Dave> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/member> <http://example.org/social/people/1.0/OurFamily> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/likes> <http://example.org/social/topics/1.0/Shoes> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Grace> <http://example.org/social/relationship/1.0/member> <http://example.org/social/people/1.0/OurFamily> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://example.org/social/relationship/1.0/child> <http://example.org/social/people/1.0/Frank> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Bob> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Alice> <http://example.org/social/relationship/1.0/child> <http://example.org/social/people/1.0/Grace> .',  # noqa: 501
    '<http://example.org/social/people/1.0/Eve> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/profile/1.0/Person> .',  # noqa: 501
    '<http://example.org/social/topics/1.0/Shoes> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/social/topics/1.0/Topic> .'  # noqa: 501
])


def test_convert_script(capsys):
    with patch('sys.argv',
               ['test_convert', '-i', input_file, '-r', 'n3', '-w', 'nt']):
        convert.main()
        (out, err) = capsys.readouterr()
        out_lines = sorted([line for line in out.split('\n')
                            if not line == ''])
        assert out_lines == sample_triples


# Note that the following four files can be considered common across all
# scripts as they exercise the command line validation and file parsing
# used in all of them.
def test_convert_script_no_file(capsys):
    expected_err = "No such file or directory: 'non_existent_file'"
    with patch('sys.argv',
               ['test_convert', '-i', 'non_existent_file', '-r', 'n3',
                '-w', 'nt']):
        try:
            convert.main()
            pytest.fail('expecting: %s' % expected_err)
        except SystemExit:
            (out, err) = capsys.readouterr()
            assert err.index(expected_err) >= 0


def test_convert_script_bad_read(capsys):
    expected_err = "error: argument -r/--read: invalid choice: 'python'"
    with patch('sys.argv',
               ['test_convert', '-i', input_file, '-r', 'python',
                '-w', 'nt']):
        try:
            convert.main()
            pytest.fail('expecting: %s' % expected_err)
        except SystemExit:
            (out, err) = capsys.readouterr()
            assert err.index(expected_err) >= 0


def test_convert_script_bad_format(capsys):
    expected_err = "expected directive or statement"
    with patch('sys.argv',
               ['test_convert', '-i', __file__, '-r', 'n3',
                '-w', 'nt']):
        convert.main()
        (out, err) = capsys.readouterr()
        assert out.index(expected_err) >= 0


def test_convert_script_bad_write(capsys):
    expected_err = "error: argument -w/--write: invalid choice: 'python'"
    with patch('sys.argv',
               ['test_convert', '-i', input_file, '-r', 'n3',
                '-w', 'python']):
        try:
            convert.main()
            pytest.fail('expecting: %s' % expected_err)
        except SystemExit:
            (out, err) = capsys.readouterr()
            assert err.index(expected_err) >= 0
