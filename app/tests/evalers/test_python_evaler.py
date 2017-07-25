from app.evalers.python import PythonEvaler
from app.tests.test_expr_parser import parse_expr
from app.parser.boxes import StringBox, IntegerBox

import pytest


def evalize(query: str, special_vars: dict=None) -> str:
    tree = parse_expr(query)
    box = PythonEvaler(tree, special_vars=special_vars).eval()
    return box.value


def test_python_evaler_integer():
    assert evalize('1') == '1'


def test_python_evaler_string():
    assert evalize("'string'") == "'string'"


def test_python_evaler_float():
    assert evalize('1.1') == '1.1'


def test_python_evaler_column_name():
    assert evalize('username') == "obj['username']"


@pytest.mark.parametrize('op', [
    '+', '-', '*', '/', '!=', '>', '>=', '<=', '<',
])
def test_python_evaler_operator(op):
    assert evalize('val1 %s val2' % op) == "obj['val1'] %s obj['val2']" % op


def test_python_and_operator():
    assert evalize('val1 AND val2') == "obj['val1'] and obj['val2']"


def test_python_or_operator():
    assert evalize('val1 OR val2') == "obj['val1'] or obj['val2']"


def test_python_priority():
    assert evalize('a + b * c') == "obj['a'] + obj['b'] * obj['c']"


def test_python_priority_with_equal_ops():
    assert evalize('a + b - c') == "obj['a'] + obj['b'] - obj['c']"


def test_python_priority_with_braces():
    assert evalize('(a + b) * c') == "(obj['a'] + obj['b']) * obj['c']"


def test_python_name_with_spaces():
    assert evalize('"VAL WITH SPACES"') == "obj['VAL WITH SPACES']"


def test_python_set_special_var():
    special_vars = {
        'QUESTION_OF_LIFE': StringBox('42'),
        'TWO': IntegerBox('2'),
    }
    result = evalize('QUESTION_OF_LIFE = 40 + TWO', special_vars)
    assert result == "'42' == 40 + 2"


def test_convert_to_function():
    obj = dict(a=30, b=40, c=50)
    tree = parse_expr('(a * 2 + b > c + 50) * 2')
    # (30 * 2 + 40 > 50 + 50) * 2
    # (60 + 40 > 100) * 2
    # (100 > 100) * 2
    # False * 2
    # 0
    evaler = PythonEvaler(tree)
    function = evaler.convert_to_function()
    assert callable(function)
    assert function(obj) == 0
