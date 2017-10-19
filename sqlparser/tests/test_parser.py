from pprint import pprint
from sqlparser.parser.parser import parser
from sqlparser.parser.lex import lexer
from sqlparser.parser.boxes import QueryBox, NameBox, NamedExprBox, OpBox


def parse(data: str) -> QueryBox:
    pprint(list(lexer.lex(data)))  # for debug data when test has failed
    return parser.parse(lexer.lex(data))


def test_parser_simple_query():
    assert parse('SELECT x FROM z') == QueryBox(
        exprs=[
            NamedExprBox(None, NameBox('x')),
        ],
        froms=[NameBox('z')],
        where=None,
        limit=None,
        offset=None,
        group_by=None,
    )


def test_parser_with_many_columns():
    assert parse('SELECT a, b, c FROM z').exprs == [
        NamedExprBox(None, NameBox('a')),
        NamedExprBox(None, NameBox('b')),
        NamedExprBox(None, NameBox('c')),
    ]


def test_parser_with_named_column():
    assert parse('SELECT a AS named FROM z').exprs == [
        NamedExprBox(name=NameBox('named'), expr=NameBox('a')),
    ]


def test_parser_with_named_column_without_as():
    assert parse('SELECT a named FROM z').exprs == [
        NamedExprBox(name=NameBox('named'), expr=NameBox('a')),
    ]


def test_parser_with_named_column_with_strings():
    assert parse('SELECT "a-a" AS "named" FROM z').exprs == [
        NamedExprBox(name=NameBox('named'), expr=NameBox('a-a')),
    ]


def test_parser_where():
    assert parse('SELECT a FROM z WHERE a = b').where == OpBox(
        op='OP_EQ',
        left=NameBox('a'),
        right=NameBox('b'),
    )


def test_parser_limit():
    query = parse('SELECT a FROM z LIMIT 5')
    assert query.limit == 5
    assert query.offset is None


def test_parser_offset():
    query = parse('SELECT a FROM z LIMIT 5 OFFSET 5')
    assert query.limit == 5
    assert query.offset == 5


def test_group_by():
    query = parse('SELECT a FROM z GROUP BY foo + bar, foo')
    assert query.group_by == [
        OpBox(
            op='OP_ADD',
            left=NameBox('foo'),
            right=NameBox('bar'),
        ),
        NameBox('foo'),
    ]