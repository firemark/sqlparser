from app.evalers.abstract import AbstractEvaler
from app.evalers.utils import OpFormatizer, EvalBox
from app.parser.boxes import FuncBox, NameBox


class MongoOpFormatizer(OpFormatizer):
    PRIORITY_TYPES = {
        'STRING': 0,
        'INT': 0,
        'FLOAT': 0,
        'BOOL': 0,
        'VAR': 0,
        'FUNC': 0,
        'OP_MUL': 2,
        'OP_DIV': 2,
        'OP_ADD': 4,
        'OP_SUB': 4,
        'OP_LT': 6,
        'OP_LTE': 6,
        'OP_GT': 6,
        'OP_GTE': 6,
        'OP_EQ': 8,
        'OP_NEQ': 8,
        'OP_OR': 10,
        'OP_AND': 10,
    }


class MongoWhereEvaler(AbstractEvaler):
    OPS = {key: MongoOpFormatizer(key, op) for key, op in {
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
        'OP_OR': '||',
        'OP_AND': '&&',
    }.items()}

    def eval_integer(self):
        return EvalBox('INT', str(self.expr.value))

    def eval_float(self):
        return EvalBox('FLOAT', str(self.expr.value))

    def eval_string(self):
        return EvalBox('STRING', repr(self.expr.value))

    def eval_name(self):
        expr = self.expr  # type: NameBox
        value = expr.value
        format = 'this.%s' if value.isalnum() else 'this[%r]'
        return EvalBox('VAR', format % value)

    def eval_func(self):
        # TODO: Support object (like string or array) methods
        expr = self.expr  # type: FuncBox
        args = [self.eval_again(arg).value for arg in expr.args]
        value = '{func}({args})'.format(
            func=expr.name,
            args=', '.join(args),
        )
        return EvalBox('FUNC', value)
