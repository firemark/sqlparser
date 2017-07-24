from typing import List, Iterator

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.sql.elements import ColumnElement  # noqa
from sqlalchemy.sql.expression import select, table

from app.parser.boxes import QueryBox, ExprBox, NamedExprBox
from app.tables.abstract import AbstractTable
from app.evalers.sql import SqlEvaler


def create_base(uri):
    engine = create_engine(uri)
    base = automap_base()
    base.prepare(engine, reflect=True)
    return base


class SqlTable(AbstractTable):
    TABLE = None  # SQLAlchemy ORM table

    def __init__(self):
        self.columns = []  # type: ColumnElement

    def set_columns(self, exprs: List[NamedExprBox]):
        self.columns = [
            self._get_column_with_label(named_expr)
            for named_expr in exprs
        ]

    def _get_column_with_label(self, named_expr: NamedExprBox):
        column = SqlEvaler(named_expr.expr).eval()
        namebox = named_expr.name
        name = namebox.value if namebox else str(column)
        labeled_column = column.label(name)
        return labeled_column

    def generate_data(self) -> Iterator[List]:
        yield []

