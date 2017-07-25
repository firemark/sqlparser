from functools import reduce
from operator import or_
from typing import Callable, Tuple, List, Iterator, Set

from app.parser.boxes import ExprBox, NamedExprBox
from app.tables.abstract import AbstractTable
from app.evalers.mongo import MongoWhereEvaler
from app.evalers.python import PythonEvaler

from pymongo.cursor import CursorType

column_type = Tuple[str, Callable]


class MongoTable(AbstractTable):
    EVALER = MongoWhereEvaler
    TABLE = None  # MongoEngine database

    def __init__(self):
        self.columns = []  # type: List[column_type]
        self.query_columns = []  # type: Set[str]
        self.where = None  # type: str
        self.limit = None  # type: int
        self.offset = None  # type: int

    def set_columns(self, exprs: List[NamedExprBox]):
        self.query_columns |= reduce(
            or_,
            (expr.expr.find_names() for expr in exprs)
        )
        self.columns += [
            self._get_column_with_label(named_expr)
            for named_expr in exprs
        ]

    def set_where(self, expr: ExprBox):
        self.where = self.eval(expr).value

    def set_limit(self, limit: int):
        self.limit = limit

    def set_offset(self, offset: int):
        self.offset = offset

    def _get_column_with_label(self, named_expr: NamedExprBox) -> column_type:
        evaler = self.make_evaler(named_expr.expr, evaler_cls=PythonEvaler)
        column = evaler.convert_to_function()
        name = self.get_name_of_named_expr(named_expr)
        return name, column

    def generate_data(self) -> Iterator[Tuple]:
        yield [name for name, _ in self.columns]
        where = {'$where': self.where} if self.where else None,
        finds = self.TABLE.find(
            filter=where,
            projection={name: True for name in self.query_columns},
            cursor=CursorType.TAILABLE,
            limit=self.limit,
            skip=self.skip,
        )
        for obj in finds:
            yield [func(obj) for _, func in self.columns]
