"""
Tests
"""

from httplink import unescape, parse_link_header
import pytest


def test_unescape() -> None:
    """
    Test unescape function.
    """
    assert unescape('') == ''
    assert unescape('foo') == 'foo'
    assert unescape(r'\r\n') == 'rn'
    assert unescape(r'foo\\b\ar') == r'foo\bar'

    with pytest.raises(ValueError, match='Trailing backslash'):
        unescape(r'foo\\bar\baz\quuz\\''\\')


def test_parse() -> None:
    """
    Test parse_link_header function.
    """
    with pytest.raises(ValueError, match='Bad link'):
        parse_link_header('''</> </>''')

    assert not parse_link_header('')
    assert not parse_link_header(',')
    assert not parse_link_header(' ,, ,,, ,, ')

    result = parse_link_header('''</>''')
    assert not result.links[0]
    assert result.links[0].rel == set()

    result = parse_link_header('''<http://example.com/TheBook/chapter2>; rel="previous"; title="previous chapter"''')
    assert result['previous'].target == 'http://example.com/TheBook/chapter2'
    assert result['previous'].rel == {'previous'}
    assert result['PrEvIoUs']['TiTlE'] == 'previous chapter'
    assert 'PREVious' in result
    assert 'PREVios' not in result

    result = parse_link_header('''</>; rel="http://example.net/foo"''')
    assert result['http://example.net/foo'].target == '/'

    result = parse_link_header('''</terms>; rel="copyright"; Anchor="#foo"''')
    assert len(result) == 1
    assert result.links[0].attributes == [('rel', 'copyright'), ('Anchor', '#foo')]
    assert result['copyright']['ANCHOR'] == '#foo'
    assert 'anchor' in result['copyright']

    result = parse_link_header('''
        </TheBook/chapter2>;
         rel="previous"; title*=UTF-8'de'letztes%20Kapitel,
         </TheBook/chapter4>;
         rel="next"; title*=UTF-8'de'n%c3%a4chstes%20Kapitel
    ''')
    assert len(result) == 2
    assert result['previous']['title'] == 'letztes Kapitel'
    assert result['next']['title'] == 'nächstes Kapitel'
    assert 'nächstes' in repr(result)

    result = parse_link_header('''<http://example.org/>; rel="start http://example.net/relation/other"''')
    assert result['start'] is result['http://example.net/relation/other']
    assert result['start'].rel == {'start', 'http://example.net/relation/other'}

    with pytest.raises(ValueError, match='Bad extended value'):
        parse_link_header('''</>; foo*=bar''')

    with pytest.raises(ValueError, match='Only UTF-8'):
        parse_link_header('''<https://www.example.net/>; attr*=ebcdic'web'%85%97%89%83@%86%81%89%93%25''')
