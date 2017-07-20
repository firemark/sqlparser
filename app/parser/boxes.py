from typing import Optional, List


class Box(object):
    value = None

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '<{} value: {!r}>'.format(type(self).__name__, self.value)


class ExprBox(Box):
    pass


class StringBox(ExprBox):

    def __init__(self, value: str):
        self.value = value


class IntegerBox(ExprBox):

    def __init__(self, value: str):
        self.value = int(value)


class NameBox(ExprBox):

    def __init__(self, value: str):
        self.value = value


class FuncBox(ExprBox):

    def __init__(self, name: str, args: List[ExprBox]):
        self.name = name
        self.args = args

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

    def __repr__(self):
        return '<{} {} left: {!r} right: {!r}>'.format(
            type(self).__name__,
            self.op,
            self.left,
            self.right,
        )


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
            orders=None):
        self.exprs = exprs
        self.froms = froms
        self.where = where
        self.orders = orders

    def __repr__(self):
        return '<QueryBox>'
