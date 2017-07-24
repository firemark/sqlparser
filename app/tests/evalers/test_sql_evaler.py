from sqlalchemy.sql.elements import ColumnElement

from app.evalers.sql import SqlEvaler
from app.tests.test_expr_parser import parse_expr

import pytest


def evalize(query: str) -> ColumnElement:
    tree = parse_expr(query)
    statement = SqlEvaler(tree).eval()
    compiled_statement = statement.compile(
        compile_kwargs={"literal_binds": True},
    )
    return str(compiled_statement)


def test_sql_evaler_integer():
    assert evalize('1') == '1'


def test_sql_evaler_string():
    assert evalize("'string'") == "'string'"


def test_sql_evaler_column_name():
    assert evalize('username') == 'username'


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
