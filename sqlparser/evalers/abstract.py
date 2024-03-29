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
        boxes.TypeCastBox: 'typecast',
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
        'OP_BITWISE_XOR': operator.xor,
        'OP_BITWISE_AND': operator.and_,
        'OP_BITWISE_OR': operator.or_,
        'OP_IN': lambda a, b: a in b,
        'OP_NOT_INT': lambda a, b: a not in b,
    }
    SINGLE_OPS = {
        'OP_NOT': operator.not_,
        'OP_BITWISE_NOT': operator.inv,
        'OP_ABSOLUTE': operator.abs,
        'OP_SUB': operator.neg,
    }
    FUNCTIONS = {}

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
    def eval_typecast(self):
        raise NotImplementedError('eval_typecast')

    def eval_name_or_special(self):
        name = self.expr  # type: boxes.NameBox
        value = name.get_real_value()
        special_var = self.special_vars.get(value)
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

    def eval_single_op(self):
        expr = self.expr  # type: boxes.OpBox
        value = self.eval_again(expr.value)
        op = expr.op
        func = self.SINGLE_OPS.get(op)
        if func is None:
            raise EvalerError('single operator %s is not supported' % op, op)
        return func(value)

    def eval_func(self):
        expr = self.expr  # type: boxes.FuncBox
        args = [self.eval_again(arg) for arg in expr.args]
        name = expr.name
        func = self.FUNCTIONS.get(name.lower())
        if func is None:
            raise EvalerError('unknown function %s' % name, name)
        return func(*args)
