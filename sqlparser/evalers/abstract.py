from typing import Dict

from sqlparser.parser import boxes
from abc import ABC, abstractmethod
import operator


class EvalerError(Exception):
    pass


class AbstractEvaler(ABC):
    expr = None  # type: boxes.ExprBox
    special_vars = None  # type: Dict[str, boxes.ExprBox]
    EVAL_METHODS = {
        boxes.StringBox: 'string',
        boxes.FloatBox: 'float',
        boxes.IntegerBox: 'integer',
        boxes.NameBox: 'name_or_special',
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
        'OP_OR': lambda a, b: a or b,
        'OP_AND': lambda a, b: a and b,
    }

    def __init__(self, expr: boxes.ExprBox, special_vars=None):
        self.expr = expr
        self.special_vars = special_vars or {}

    def eval_again(self, expr: boxes.ExprBox):
        cls = type(self)
        return cls(expr, special_vars=self.special_vars).eval()

    def eval(self):
        expr_cls = type(self.expr)
        method_name = self.EVAL_METHODS.get(expr_cls)
        if method_name is None:
            raise EvalerError('Method to eval %s not found' % expr_cls.__name__)
        method = getattr(self, 'eval_%s' % method_name)
        return method()

    @abstractmethod
    def eval_integer(self):
        raise NotImplementedError('eval_integer')

    @abstractmethod
    def eval_float(self):
        raise NotImplementedError('eval_float')

    @abstractmethod
    def eval_string(self):
        raise NotImplementedError('eval_string')

    @abstractmethod
    def eval_name(self):
        raise NotImplementedError('eval_name')

    @abstractmethod
    def eval_func(self):
        raise NotImplementedError('eval_func')

    def eval_name_or_special(self):
        name = self.expr  # type: boxes.NameBox
        special_var = self.special_vars.get(name.value)
        if special_var is None:
            return self.eval_name()
        return self.eval_again(special_var)

    def eval_op(self):
        expr = self.expr  # type: boxes.OpBox
        left = self.eval_again(expr.left)
        right = self.eval_again(expr.right)
        op = expr.op
        func = self.OPS.get(op)
        if func is None:
            raise EvalerError('operator %s is not supported' % op, op)
        return func(left, right)

