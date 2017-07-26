from sqlalchemy.sql.expression import table
from sqlparser.tests.test_parser import parse

from sqlparser.tables.sql import SqlTable
from sqlparser.tables.utils import special_vars


class MockSqlTable(SqlTable):
    SPECIAL_VARS = special_vars(
        x=42,
        y='42',
    )
    TABLE = table('users')


def evalize(query: str) -> str:
    tree = parse(query)
    table = MockSqlTable()
    table.set_columns(tree.exprs)
    if tree.where:
        table.set_where(tree.where)

    statement = table.generate_select()
    compiled_statement = statement.compile(
        compile_kwargs={"literal_binds": True},
    )
    return str(compiled_statement).replace('\n', '')


def test_sql_table_simple_query():
    assert evalize('SELECT a FROM users') == 'SELECT a AS a FROM users'


def test_sql_table_with_named_column():
    result = evalize('SELECT money AS dolars FROM users')
    assert result == 'SELECT money AS dolars FROM users'


def test_sql_table_with_complex_column():
    result = evalize('SELECT a + b FROM users')
    assert result == 'SELECT a + b AS a__b FROM users'


def test_sql_table_with_many_columns():
    result = evalize('SELECT a, b FROM users')
    assert result == 'SELECT a AS a, b AS b FROM users'


def test_sql_table_with_undefined_name():
    result = evalize('SELECT 40 + 2 FROM users')
    assert result == 'SELECT 40 + 2 AS "??" FROM users'


def test_sql_table_with_where_clause():
    result = evalize('SELECT id FROM users WHERE money > 5')
    assert result == 'SELECT id AS id FROM users WHERE money > 5'


def test_sql_table_with_special_vars():
    result = evalize('SELECT money + x FROM users WHERE lower(username) = y')
    assert result == (
        'SELECT money + 42 AS money__x FROM users '
        'WHERE lower(username) = \'42\''
    )
