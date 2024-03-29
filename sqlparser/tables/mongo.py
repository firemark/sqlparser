from functools import reduce
from operator import or_
from typing import Callable, Tuple, List, Iterator, Set

from pymongo.collection import Collection

from sqlparser.parser.boxes import ExprBox, NamedExprBox
from sqlparser.tables.abstract import AbstractTable
from sqlparser.evalers.mongo import MongoWhereEvaler
from sqlparser.evalers.python import PythonEvaler

from pymongo.cursor import CursorType

column_type = Tuple[str, Callable]


# TODO: we need reimplenent query


class MongoTable(AbstractTable):
    EVALER = MongoWhereEvaler
    TABLE = None  # type: Collection

    def __init__(self):
        super().__init__()
        self.columns = []  # type: List[column_type]
        self.query_columns = set()  # type: Set[str]
        self.where = None  # type: str
        self.limit = 0  # type: int
        self.offset = 0  # type: int
        self.group_by = []

    def set_columns(self, exprs: List[NamedExprBox]):
        self.columns += [
            self._get_column_with_label(named_expr)
            for named_expr in exprs
        ]
        self._fill_used_columns(named_expr.expr for named_expr in exprs)

    def set_where(self, expr: ExprBox):
        self.where = self.eval(expr).value
        self._fill_used_columns([expr])

    def set_limit(self, limit: int):
        self.limit = limit or 0

    def set_offset(self, offset: int):
        self.offset = offset or 0

    def set_group_by(self, exprs: List[ExprBox]):
        # TODO: implement in generate_data method
        self.group_by = [self.eval(expr).value for expr in exprs]
        self._fill_used_columns(exprs)

    def _get_column_with_label(self, named_expr: NamedExprBox) -> column_type:
        evaler = self.make_evaler(named_expr.expr, evaler_cls=PythonEvaler)
        column = evaler.convert_to_function()
        name = self.get_name_of_named_expr(named_expr)
        return name, column

    def generate_data(self) -> Iterator[Tuple]:
        self.before_execute()
        yield [name for name, _ in self.columns]
        where = {'$where': self.where} if self.where else None
        cursor = self.TABLE.find(
            filter=where,
            projection={name: True for name in self.query_columns},
            #cursor_type=CursorType.TAILABLE,
            limit=self.limit,
            skip=self.offset,
        )
        self.after_execute()
        try:
            for obj in cursor.batch_size(20):
                yield [func(obj) for _, func in self.columns]
        finally:
            cursor.close()

