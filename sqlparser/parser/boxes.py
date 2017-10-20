from functools import reduce
from operator import or_
from typing import Optional, List, Union, Set
from decimal import Decimal


Numerable = Union[str, int, float]


class Box(object):
    value = None

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '<{} value: {!r}>'.format(type(self).__name__, self.value)


class ExprBox(Box):

    def find_names(self) -> Set[str]:
        raise NotImplementedError('find_names')


class SimpleExprBox(ExprBox):

    def find_names(self) -> Set[str]:
        return set()


class StringBox(SimpleExprBox):

    def __init__(self, value: str):
        self.value = value


class IntegerBox(SimpleExprBox):

    def __init__(self, value: Numerable):
        self.value = int(value)


class FloatBox(SimpleExprBox):

    def __init__(self, value: Numerable):
        self.value = Decimal(value)


class NullBox(SimpleExprBox):
    pass


class BooleanBox(SimpleExprBox):
    TRUE_VALUES = {'TRUE', 'YES'}
    value = False  # type: bool

    def __init__(self, value: Union[bool, str]):
        if isinstance(value, bool):
            self.value = value
        self.value = value.upper() in self.TRUE_VALUES


class NameBox(ExprBox):

    def __init__(self, value: str):
        self.value = value

    def find_names(self) -> Set[str]:
        return {self.value}


class FuncBox(ExprBox):

    def __init__(self, name: str, args: List[ExprBox]):
        self.name = name
        self.args = args

    def find_names(self) -> Set[str]:
        return reduce(or_, (expr.find_names() for expr in self.args))

    def __repr__(self):
        return '<{} {} expr: {!r}>'.format(
            type(self).__name__,
            self.name,
            self.args,
        )


class OpBox(ExprBox):

    def __init__(self, op: str, left: ExprBox, right: ExprBox):
        self.op = op
        self.left = left
        self.right = right

    def find_names(self) -> Set[str]:
        return self.left.find_names() | self.right.find_names()

    def __repr__(self):
        return '<{} {} left: {!r} right: {!r}>'.format(
            type(self).__name__,
            self.op,
            self.left,
            self.right,
        )


class SingleOpBox(ExprBox):

    def __init__(self, op: str, value: ExprBox):
        self.op = op
        self.value = value

    def find_names(self) -> Set[str]:
        return self.value.find_names()

    def __repr__(self):
        return '<{} {} value: {!r}>'.format(
            type(self).__name__,
            self.op,
            self.value,
        )


class TypeCastBox(ExprBox):

    def __init__(self, to: str, value: ExprBox):
        self.to = to.lower()
        self.value = value

    def find_names(self) -> Set[str]:
        return self.value.find_names()



class ColumnNameBox(Box):

    def __init__(self, left_name: Optional[NameBox], right_name: NameBox):
        self.table_name = left_name or left_name.value  # Optional[str]
        self.column_name = right_name.value  # NameBox

    def __repr__(self):
        return '<{} table: {!r} column: {!r}>'.format(
            type(self).__name__,
            self.table_name,
            self.column_name,
        )


class NamedExprBox(Box):

    def __init__(self, name: Optional[NameBox], expr: ExprBox):
        self.name = name  # type: Optional[NameBox]
        self.expr = expr  # type: ExprBox

    def __repr__(self):
        return '<{} name: {!r} expr: {!r}>'.format(
            type(self).__name__,
            self.name,
            self.expr,
        )


class QueryBox(Box):

    def __init__(
            self,
            exprs: List[NamedExprBox],
            froms: List[NameBox],
            where: Optional[ExprBox]=None,
            group_by: Optional[List[ExprBox]]=None,
            limit: Optional[int]=None,
            offset: Optional[int]=None,
            orders=None):
        self.exprs = exprs
        self.froms = froms
        self.where = where
        self.group_by = group_by
        self.orders = orders
        self.limit = limit
        self.offset = offset

    def __repr__(self):
        return '<QueryBox>'


