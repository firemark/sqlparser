from app.parser import boxes
import operator


class EvalerError(Exception):
    pass


class AbstractEvaler(object):
    expr = None  # type: boxes.ExprBox
    EVAL_METHODS = {
        boxes.StringBox: 'string',
        boxes.IntegerBox: 'integer',
        boxes.NameBox: 'name',
        boxes.FuncBox: 'func',
        boxes.OpBox: 'op',
    }
    OPS = {
        'OP_ADD': operator.add,
        'OP_SUB': operator.sub,
        'OP_MUL': operator.mul,
        'OP_DIV': operator.truediv,
        'OP_EQ': operator.eq,
        'OP_NEQ': operator.ne,
        'OP_LT': operator.lt,
        'OP_LTE': operator.le,
        'OP_GT': operator.gt,
        'OP_GTE': operator.ge,
        'OP_OR': operator.or_,
        'OP_AND': operator.and_,
    }

    def __init__(self, expr: boxes.ExprBox):
        self.expr = expr

    @classmethod
    def eval_again(cls, expr: boxes.ExprBox):
        return cls(expr).eval()

    def eval(self):
        expr_cls = type(self.expr)
        method_name = self.EVAL_METHODS.get(expr_cls)
        if method_name is None:
            raise EvalerError('Method to eval %s not found' % expr_cls.__name__)
        method = getattr(self, 'eval_%s' % method_name)
        return method()

    def eval_integer(self):
        raise NotImplementedError('eval_integer')

    def eval_string(self):
        raise NotImplementedError('eval_string')

    def eval_name(self):
        raise NotImplementedError('eval_name')

    def eval_func(self):
        raise NotImplementedError('eval_func')

    def eval_op(self):
        expr = self.expr  # type: boxes.OpBox
        left = self.eval_again(expr.left)
        right = self.eval_again(expr.right)
        op = expr.op
        func = self.OPS.get(op)
        if func is None:
            raise EvalerError('operator %s is not supported' % op, op)
        return func(left, right)

