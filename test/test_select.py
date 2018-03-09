import pytest
import os
from unittest.mock import patch

from rdftools.scripts import select

sample_file = os.path.join(os.path.dirname(__file__), 'data/sample.n3')

expected_subjects = sorted("""http://example.org/social/people/1.0/OurFamily
http://example.org/social/people/1.0/Alice
http://example.org/social/people/1.0/Frank
http://example.org/social/people/1.0/Grace
http://example.org/social/people/1.0/Eve
http://example.org/social/people/1.0/Dave
http://example.org/social/people/1.0/Heidi
http://example.org/social/topics/1.0/Shoes
http://example.org/social/people/1.0/Bob
http://example.org/social/topics/1.0/Diving
http://example.org/social/people/1.0/Carol
""".split('\n'))[1:]

expected_predicates = sorted("""http://example.org/social/relationship/1.0/child
http://www.w3.org/1999/02/22-rdf-syntax-ns#type
http://example.org/social/relationship/1.0/parent
http://example.org/social/relationship/1.0/spouse
http://example.org/social/relationship/1.0/member
http://example.org/social/relationship/1.0/likes
""".split('\n'))[1:]

expected_objects = sorted("""http://example.org/social/people/1.0/Dave
http://example.org/social/people/1.0/Grace
http://example.org/social/people/1.0/Carol
http://example.org/social/topics/1.0/Shoes
http://example.org/social/people/1.0/Eve
http://example.org/social/people/1.0/OurFamily
http://example.org/social/topics/1.0/Topic
http://example.org/social/profile/1.0/Family
http://example.org/social/topics/1.0/Diving
http://example.org/social/profile/1.0/Person
http://example.org/social/people/1.0/Heidi
http://example.org/social/people/1.0/Alice
http://example.org/social/people/1.0/Frank
""".split('\n'))[1:]

expected_types = sorted("""http://example.org/social/topics/1.0/Topic
http://example.org/social/profile/1.0/Person
http://example.org/social/profile/1.0/Family
""".split('\n'))[1:]

test_parameters = [
    ('-s', expected_subjects),
    ('-p', expected_predicates),
    ('-o', expected_objects),
    ('-t', expected_types)
]


@pytest.mark.parametrize('param, expected', test_parameters)
def test_select_script_subjects(capsys, param, expected):
    with patch('sys.argv',
               ['test_select', '-i', sample_file, '-r', 'n3', param]):
        select.main()
        (out, err) = capsys.readouterr()
        out_lines = sorted([line for line in out.split('\n')
                            if not line == ''])
        assert out_lines == expected
