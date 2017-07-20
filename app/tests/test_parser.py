from pprint import pprint
from app.parser.parser import parser
from app.parser.lex import lexer
from app.parser.boxes import QueryBox, NameBox, NamedExprBox, OpBox


def parse(data: str) -> QueryBox:
    pprint(list(lexer.lex(data)))  # for debug data when test has failed
    return parser.parse(lexer.lex(data))


def test_parser_simple_query():
    assert parse('SELECT x FROM z') == QueryBox(
        exprs=[
            NamedExprBox(None, NameBox('x')),
        ],
        froms=[NameBox('z')],
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
