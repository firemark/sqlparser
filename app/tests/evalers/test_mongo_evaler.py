from app.evalers.mongo import MongoWhereEvaler
from app.tests.test_expr_parser import parse_expr
from app.parser.boxes import StringBox, IntegerBox

import pytest


def evalize(query: str, special_vars: dict=None) -> str:
    tree = parse_expr(query)
    mongo_box = MongoWhereEvaler(tree, special_vars=special_vars).eval()
    return mongo_box.value


def test_mongo_evaler_integer():
    assert evalize('1') == '1'


def test_mongo_evaler_string():
    assert evalize("'string'") == "'string'"


def test_mongo_evaler_float():
    assert evalize('1.1') == '1.1'


def test_mongo_evaler_column_name():
    assert evalize('username') == 'this.username'


@pytest.mark.parametrize('op', [
    '+', '-', '*', '/', '!=', '>', '>=', '<=', '<',
])
def test_mongo_evaler_operator(op):
    assert evalize('val1 %s val2' % op) == 'this.val1 %s this.val2' % op


def test_mongo_and_operator():
    assert evalize('val1 AND val2') == 'this.val1 && this.val2'


def test_mongo_or_operator():
    assert evalize('val1 OR val2') == 'this.val1 || this.val2'


def test_mongo_priority():
    assert evalize('a + b * c') == 'this.a + this.b * this.c'


def test_mongo_priority_with_equal_ops():
    assert evalize('a + b - c') == 'this.a + this.b - this.c'


def test_mongo_priority_with_braces():
    assert evalize('(a + b) * c') == '(this.a + this.b) * this.c'


def test_name_with_spaces():
    assert evalize('"VAL WITH SPACES"') == "this['VAL WITH SPACES']"


def test_set_special_var():
    special_vars = {
        'QUESTION_OF_LIFE': StringBox('42'),
        'TWO': IntegerBox('2'),
    }
    result = evalize('QUESTION_OF_LIFE = 40 + TWO', special_vars)
    assert result == "'42' == 40 + 2"

