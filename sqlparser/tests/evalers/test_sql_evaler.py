from sqlalchemy.sql.elements import ColumnElement

from sqlparser.evalers.abstract import EvalerError
from sqlparser.evalers.sql import SqlEvaler
from sqlparser.tests.test_expr_parser import parse_expr
from sqlparser.parser.boxes import StringBox, IntegerBox

import pytest


def evalize(query: str, special_vars: dict=None) -> str:
    tree = parse_expr(query)
    statement = SqlEvaler(tree, special_vars=special_vars).eval()
    compiled_statement = statement.compile(
        compile_kwargs={"literal_binds": True},
    )
    return str(compiled_statement)


def test_sql_evaler_integer():
    assert evalize('1') == '1'


def test_sql_evaler_string():
    assert evalize("'string'") == "'string'"


def test_sql_evaler_float():
    assert evalize('1.1') == '1.1'


def test_sql_evaler_column_name():
    assert evalize('username') == 'username'


def test_sql_evaler_column_name_with_table():
    assert evalize('users.username') == 'users.username'


def test_sql_evaler_function():
    assert evalize('lower(username)') == 'lower(username)'


@pytest.mark.parametrize('op', [
    '+', '-', '*', '/', '=', '!=', '>', '>=', '<=', '<',
])
def test_sql_evaler_operator(op):
    assert evalize('val1 %s val2' % op) == 'val1 %s val2' % op


def test_sql_and_operator():
    assert evalize('val1 AND val2') == 'val1 AND val2'


def test_sql_or_operator():
    assert evalize('val1 OR val2') == 'val1 OR val2'


def test_sql_set_special_var():
    special_vars = {
        'QUESTION_OF_LIFE': StringBox('42'),
        'TWO': IntegerBox('2'),
        'foo.bar': StringBox('foo')
    }
    result = evalize('QUESTION_OF_LIFE = 40 + TWO + foo.bar', special_vars)
    assert result == "'42' = 40 + 2 + 'foo'"


def test_sql_unknown_function():
    with pytest.raises(EvalerError) as exp:
        evalize('foobarito(5)')

    assert exp.value.args == ('unknown function foobarito', 'foobarito')


def test_sql_typecasting():
    assert evalize('\'5\'::float') == 'CAST(\'5\' AS NUMERIC)'


def test_sql_unknown_typecasting():
    with pytest.raises(EvalerError) as exp:
        evalize('5::foobarito')

    assert exp.value.args == ('type foobarito is not supported', 'foobarito')
