from sqlparser.evalers.abstract import AbstractEvaler, EvalerError
from sqlparser.evalers.utils import OpFormatizer, EvalBox
from sqlparser.parser.boxes import FuncBox, NameBox

from typing import Callable, Any


class PythonEvaler(AbstractEvaler):
    OPS = {key: OpFormatizer(key, op) for key, op in {
        'OP_ADD': '+',
        'OP_SUB': '-',
        'OP_MUL': '*',
        'OP_DIV': '/',
        'OP_EQ': '==',
        'OP_NEQ': '!=',
        'OP_LT': '<',
        'OP_LTE': '<=',
        'OP_GT': '>',
        'OP_GTE': '>=',
        'OP_OR': 'or',
        'OP_AND': 'and',
    }.items()}
    TYPES = {
        'int': 'int',
        'integer': 'int',
        'date': 'date',
        'datetime': 'datetime',
        'numeric': 'Decimal',
        'float': 'Decimal',
        'text': 'str',
        'str': 'str',
        'character': 'str',
    }

    def eval_integer(self):
        return EvalBox('INT', str(self.expr.value))

    def eval_float(self):
        return EvalBox('FLOAT', str(self.expr.value))

    def eval_string(self):
        return EvalBox('STRING', repr(self.expr.value))

    def eval_name(self):
        expr = self.expr  # type: NameBox
        value = expr.value
        return EvalBox('VAR', 'obj.get(%r)' % value)

    def eval_typecast(self):
        expr = self.expr  # type: TypeCastBox
        expr_type = self.TYPES.get(expr.to)  # type: str
        if expr_type is None:
            raise EvalerError('type %s is not supported' % expr.to, expr.to)
        value = '{type}({arg})'.format(
            type=expr_type,
            arg=self.eval_again(expr.value).value,
        )

        return EvalBox('FUNC', value)

    def eval_func(self):
        raise EvalerError('Functions in Python Evaler are not supported')
        # TODO: Support object (like string or array) methods
        expr = self.expr  # type: FuncBox
        args = [self.eval_again(arg).value for arg in expr.args]
        value = '{func}({args})'.format(
            func=expr.name,
            args=', '.join(args),
        )
        return EvalBox('FUNC', value)

    def convert_to_function(self) -> Callable[[dict], Any]:
        evaled_string = 'lambda obj: %s' % self.eval().value
        return eval(evaled_string)  # I hope this is 'save'
