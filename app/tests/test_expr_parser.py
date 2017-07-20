from app.tests.test_parser import parse
from app.parser.boxes import (
    NameBox, StringBox, IntegerBox, ExprBox, OpBox, FuncBox,
)


def parse_expr(expr: str) -> ExprBox:
    query_box = parse('SELECT %s FROM z' % expr)
    assert len(query_box.exprs) == 1
    assert query_box.froms == [NameBox('z')]
    expr = query_box.exprs[0]
    assert expr.name is None
    return expr.expr


def test_expr_string():
    assert parse_expr("'string string'") == StringBox('string string')


def test_expr_int():
    assert parse_expr('42') == IntegerBox('42')


def test_expr_add():
    assert parse_expr('a + b') == OpBox(
        op='OP_ADD',
        left=NameBox('a'),
        right=NameBox('b'),
    )


def test_expr_multi_add_sub():
    assert parse_expr('a + b - c') == OpBox(
        op='OP_SUB',
        left=OpBox(
            op='OP_ADD',
            left=NameBox('a'),
            right=NameBox('b'),
        ),
        right=NameBox('c'),
    )


def test_expr_mul_order():
    assert parse_expr('a + b * c') == OpBox(
        op='OP_ADD',
        left=NameBox('a'),
        right=OpBox(
            op='OP_MUL',
            left=NameBox('b'),
            right=NameBox('c'),
        ),
    )


def test_expr_logic_order():
    assert parse_expr('a * b AND c') == OpBox(
        op='OP_AND',
        left=OpBox(
            op='OP_MUL',
            left=NameBox('a'),
            right=NameBox('b'),
        ),
        right=NameBox('c'),
    )


def test_expr_compare_order():
    assert parse_expr('a AND b = c') == OpBox(
        op='OP_EQ',
        left=OpBox(
            op='OP_AND',
            left=NameBox('a'),
            right=NameBox('b'),
        ),
        right=NameBox('c'),
    )


def test_expr_braces():
    assert parse_expr('a * (b + c)') == OpBox(
        op='OP_MUL',
        left=NameBox('a'),
        right=OpBox(
            op='OP_ADD',
            left=NameBox('b'),
            right=NameBox('c'),
        ),
    )


def test_expr_func():
    assert parse_expr('a(b)') == FuncBox(
        name='a',
        args=[
            NameBox('b'),
        ]
    )


def test_expr_func_with_args():
    assert parse_expr('a(b, c)') == FuncBox(
        name='a',
        args=[
            NameBox('b'),
            NameBox('c'),
        ]
    )
