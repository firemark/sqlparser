from app.evalers.abstract import AbstractEvaler, EvalerError
from app.parser.boxes import FuncBox, NameBox


class MongoBox(object):
    __slots__ = ('type', 'value')

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value


class OpFormatizer(object):
    """
        Join two 'stringed' eval values
        with single operator
        to one 'stringed' eval
    """

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

    def __init__(self, op_type: str, op: str):
        self.op_type = op_type
        self.op = op

    def _check_priority(self, mongo_box: MongoBox) -> str:
        types = self.PRIORITY_TYPES
        if types[mongo_box.type] > types[self.op_type]:
            return '(%s)' % mongo_box.value
        else:
            return mongo_box.value

    def _get_value(self, a, b):
        return '{left} {op} {right}'.format(
            left=self._check_priority(a),
            right=self._check_priority(b),
            op=self.op,
        )

    def __call__(self, a, b):
        return MongoBox(self.op_type, self._get_value(a, b))


class MongoWhereEvaler(AbstractEvaler):
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
        'OP_OR': '||',
        'OP_AND': '&&',
    }.items()}

    def eval_integer(self):
        return MongoBox('INT', str(self.expr.value))

    def eval_float(self):
        return MongoBox('FLOAT', str(self.expr.value))

    def eval_string(self):
        return MongoBox('STRING', repr(self.expr.value))

    def eval_name(self):
        expr = self.expr  # type: NameBox
        value = expr.value
        format = 'this.%s' if value.isalnum() else 'this[%r]'
        return MongoBox('VAR', format % value)

    def eval_func(self):
        # TODO: Support object (like string or array) methods
        expr = self.expr  # type: FuncBox
        args = [self.eval_again(arg).value for arg in expr.args]
        value = '{func}({args})'.format(
            func=expr.name,
            args=', '.join(args),
        )
        return MongoBox('FUNC', value)
