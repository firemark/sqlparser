from app.evalers.abstract import AbstractEvaler, EvalerError
from app.parser.boxes import FuncBox, NameBox, SimpleExprBox


def formatize(op):

    def inner(a, b):
        return '({left} {op} {right})'.format(
            left=a,
            right=b,
            op=op,
        )

    return inner


class MongoWhereEvaler(AbstractEvaler):
    OPS = {key: formatize(op) for key, op in {
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

    # TODO: create MongoBox with type of value
    # TODO: dont add useless braces in eval_op

    def eval_integer(self):
        return str(self.expr.value)

    def eval_float(self):
        return str(self.expr.value)

    def eval_string(self):
        return repr(self.expr.value)

    def eval_name(self):
        expr = self.expr  # type: NameBox
        return 'this.%s' % expr.value

    def eval_func(self):
        # TODO: Support object (as string or array) methods
        expr = self.expr  # type: FuncBox
        args = [self.eval_again(arg) for arg in expr.args]
        return '{func}({args})'.format(
            func=expr.name,
            args=', '.join(args),
        )
