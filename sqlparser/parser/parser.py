import functools
from types import GeneratorType
from typing import List, Optional

from rply import ParserGenerator
from rply.token import Token

from sqlparser.parser.boxes import (
    QueryBox, NameBox, ExprBox, StringBox,
    NamedExprBox, IntegerBox, OpBox, FuncBox,
    FloatBox,
    SingleOpBox, BooleanBox, TypeCastBox, NullBox)
from sqlparser.parser.lex import OPERATORS, SINGLE_OPERATORS


pg = ParserGenerator(
    [
        'SELECT', 'FROM', 'AS', 'WHERE', 'LIMIT', 'OFFSET',
        'NAME', 'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL',
        'COMMA', 'TYPECAST',
        'OP_ADD', 'OP_SUB',
        'OP_MUL', 'OP_DIV', 'OP_MOD',
        'OP_OR', 'OP_AND',
        'OP_LT', 'OP_GT',
        'OP_LTE', 'OP_GTE',
        'OP_EQ', 'OP_NEQ',
        'OP_BITWISE_OR', 'OP_BITWISE_AND', 'OP_BITWISE_XOR',
        'OP_NOT', 'OP_BITWISE_NOT', 'OP_ABSOLUTE',
        'OP_LSHIFT', 'OP_RSHIFT',
        'OP_LIKE', 'OP_NOT_LIKE',
        'OP_IN', 'OP_NOT_IN',
        'PAREN_LEFT', 'PAREN_RIGHT',
        #'BRACKET_LEFT', 'BRACKET_RIGHT',
    ],
    precedence=[
        ('right', ['PAREN_LEFT', 'PAREN_RIGHT']),
        ('left', ['OP_AND', 'OP_OR']),
        ('right', ['OP_NOT']),
        ('left', ['OP_LT', 'OP_GT', 'OP_EQ', 'OP_NEQ', 'OP_LTE', 'OP_GTE']),
        ('left', ['OP_BITWISE_OR', 'OP_BITWISE_AND', 'OP_BITWISE_XOR']),
        ('left', ['OP_LSHIFT', 'OP_RSHIFT']),
        ('left', ['OP_LIKE', 'OP_NOT_LIKE']),
        ('left', ['OP_IN', 'OP_NOT_IN']),
        ('left', ['OP_ADD', 'OP_SUB']),
        ('left', ['OP_MUL', 'OP_DIV', 'OP_MOD']),
        ('right', ['OP_ABSOLUTE', 'OP_BITWISE_NOT']),
        #('right', ['BRACKET_LEFT', 'BRACKET_RIGHT']),
    ]
)


def pr(*rules):
    if isinstance(rules[0], GeneratorType):
        rules = list(rules[0])

    def outer(func):
        @functools.wraps(func)
        def inner(p):
            # unpack tokens
            return func(*p)

        for gram in rules:  # set rules to decorated function
            pg.production(gram)(inner)

    return outer


@pr('main : query')
def main(query: QueryBox) -> QueryBox:
    return query


@pr('query : SELECT named_exprs FROM name optional_where optional_limit')
def query(
        _s,
        named_exprs: List[NamedExprBox],
        _f,
        from_name:NameBox,
        where:Optional[ExprBox],
        optional_limit:list) -> QueryBox:
    return QueryBox(
        named_exprs,
        [from_name],
        where=where,
        limit=optional_limit[0],
        offset=optional_limit[1],
    )


@pr('optional_where : WHERE expr')
def optional_where(_, expr: ExprBox) -> ExprBox:
    return expr


@pr('optional_where :')
def optional_where_without_where() -> None:
    return None


@pr('optional_limit : LIMIT INTEGER OFFSET INTEGER')
def optional_limit_with_offset(_l, limit: Token, _o, offset: Token) -> list:
    return [int(limit.getstr()), int(offset.getstr())]


@pr('optional_limit : LIMIT INTEGER')
def optional_limit(_, limit: Token) -> list:
    return [int(limit.getstr()), None]


@pr('optional_limit :')
def optional_limit_without_limit() -> list:
    return [None, None]


@pr('named_exprs : named_exprs COMMA named_expr')
def named_exprs(
        named_exprs: List[NameBox], _, named_expr: NameBox) -> List[NameBox]:
    return named_exprs + [named_expr]


@pr('named_exprs : named_expr')
def named_exprs_stop(named_expr: NameBox) -> List[NameBox]:
    return [named_expr]


@pr('named_expr : expr AS name')
def named_expr_with_as(expr: ExprBox, _, name: NameBox) -> NamedExprBox:
    return NamedExprBox(name, expr)


@pr('named_expr : expr name')
def named_expr_without_as(expr: ExprBox, name: NameBox) -> NamedExprBox:
    return NamedExprBox(name, expr)


@pr('named_expr : expr')
def named_expr_without_name(expr: ExprBox) -> NamedExprBox:
    return NamedExprBox(None, expr)


@pr('expr : PAREN_LEFT expr PAREN_RIGHT')
def expr_with_braces(_l, expr: ExprBox, _r) -> ExprBox:
    return expr


@pr('expr : name PAREN_LEFT func_args PAREN_RIGHT')
def expr_with_braces(name: NameBox, _l, exprs: List[ExprBox], _r) -> FuncBox:
    return FuncBox(name.value, args=exprs)


@pr('func_args : func_args COMMA expr')
def func_args_start(args: List[ExprBox], _, expr: ExprBox) -> List[ExprBox]:
    return args + [expr]


@pr('func_args : expr')
def func_args_stop(expr: ExprBox) -> List[ExprBox]:
    return [expr]


@pr('expr : expr %s expr' % expr for expr in OPERATORS)
def expr_as_op(left: ExprBox, op: Token, right: ExprBox) -> OpBox:
    return OpBox(op=op.gettokentype(), left=left, right=right)


@pr('expr : %s expr' % expr for expr in SINGLE_OPERATORS)
def expr_as_op(op: Token, value: ExprBox) -> SingleOpBox:
    return SingleOpBox(op=op.gettokentype(), value=value)


@pr('expr : expr TYPECAST NAME')
def expr_as_op(left: ExprBox, _, right: NameBox) -> TypeCastBox:
    return TypeCastBox(to=right.value, value=left)


@pr('expr : STRING')
def expr_as_string(string: Token) -> StringBox:
    return StringBox(string.getstr()[1:-1].replace("\'", "'"))


@pr('expr : INTEGER')
def expr_as_integer(integer: Token) -> IntegerBox:
    return IntegerBox(integer.getstr())


@pr('expr : FLOAT')
def expr_as_float(float_num: Token) -> FloatBox:
    return FloatBox(float_num.getstr())


@pr('expr : NULL')
def expr_as_null(_) -> NullBox:
    return NullBox()


@pr('expr : BOOL')
def expr_as_float(bool: Token) -> BooleanBox:
    return BooleanBox(bool.getstr())


@pr('expr : name')
def expr_as_name(name: NameBox) -> NameBox:
    return name


@pr('name : NAME')
def name(name: Token) -> NameBox:
    value = name.getstr()
    if value[0] == '"':
        value = value[1:-1].replace(r'\"', '"')
    return NameBox(value)


parser = pg.build()
