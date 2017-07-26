class EvalBox(object):
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
        'OP_EQ': 6,
        'OP_NEQ': 6,
        'OP_OR': 10,
        'OP_AND': 10,
    }

    def __init__(self, op_type: str, op: str):
        self.op_type = op_type
        self.op = op

    def _check_priority(self, eval_box: EvalBox) -> str:
        types = self.PRIORITY_TYPES
        if types[eval_box.type] > types[self.op_type]:
            return '(%s)' % eval_box.value
        else:
            return eval_box.value

    def _get_value(self, a, b):
        return '{left} {op} {right}'.format(
            left=self._check_priority(a),
            right=self._check_priority(b),
            op=self.op,
        )

    def __call__(self, a, b):
        return EvalBox(self.op_type, self._get_value(a, b))
