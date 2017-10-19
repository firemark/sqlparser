from sqlparser.tests.test_parser import parse
from sqlparser.parser.boxes import (
    NameBox, StringBox, IntegerBox, ExprBox, OpBox, FuncBox, FloatBox,
    TypeCastBox, BooleanBox, NullBox, SingleOpBox,
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


def test_expr_float():
    assert parse_expr('1.0') == FloatBox('1.0')


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
        op='OP_AND',
        left=NameBox('a'),
        right=OpBox(
            op='OP_EQ',
            left=NameBox('b'),
            right=NameBox('c'),
        ),
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
    assert parse_expr('lower(b)') == FuncBox(
        name='lower',
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


def test_expr_bool_as_true():
    value = parse_expr('TRUE')
    assert isinstance(value, BooleanBox)
    assert value.value is True


def test_expr_bool_as_false():
    value = parse_expr('FALSE')
    assert isinstance(value, BooleanBox)
    assert value.value is False


def test_expr_null():
    assert parse_expr('NULL') == NullBox()


def test_expr_bitwise_or():
    assert parse_expr('a | b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_BITWISE_OR',
    )


def test_expr_bitwise_and():
    assert parse_expr('a & b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_BITWISE_AND',
    )


def test_expr_bitwise_xor():
    assert parse_expr('a ^ b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_BITWISE_XOR',
    )


def test_expr_module():
    assert parse_expr('a % b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_MOD',
    )


def test_expr_not():
    assert parse_expr('NOT a') == SingleOpBox(
        value=NameBox('a'),
        op='OP_NOT',
    )


def test_expr_bitwise_not():
    assert parse_expr('~ a') == SingleOpBox(
        value=NameBox('a'),
        op='OP_BITWISE_NOT',
    )


def test_expr_absolute_sign():
    assert parse_expr('@ a') == SingleOpBox(
        value=NameBox('a'),
        op='OP_ABSOLUTE',
    )


def test_expr_like():
    assert parse_expr('a LIKE b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_LIKE',
    )


def test_expr_not_like():
    assert parse_expr('a NOT LIKE b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_NOT_LIKE',
    )


def test_expr_in():
    assert parse_expr('a IN b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_IN',
    )


def test_expr_not_in():
    assert parse_expr('a NOT IN b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_NOT_IN',
    )


def test_expr_neg():
    assert parse_expr('-a') == SingleOpBox(
        value=NameBox('a'),
        op='OP_SUB',
    )


def test_expr_rshift():
    assert parse_expr('a >> b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_RSHIFT',
    )


def test_expr_lshift():
    assert parse_expr('a << b') == OpBox(
        left=NameBox('a'),
        right=NameBox('b'),
        op='OP_LSHIFT',
    )


def test_expr_typecast():
    assert parse_expr('a::INT') == TypeCastBox(
        value=NameBox('a'),
        to='int',
    )