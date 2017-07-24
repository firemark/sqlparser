from typing import Tuple, List, Iterator

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.sql.elements import ColumnElement  # noqa
from sqlalchemy.sql.expression import Select

from app.parser.boxes import ExprBox, NamedExprBox
from app.tables.abstract import AbstractTable
from app.evalers.sql import SqlEvaler


def create_base(uri):
    engine = create_engine(uri)
    base = automap_base()
    base.prepare(engine, reflect=True)
    return base


class SqlTable(AbstractTable):
    EVALER = SqlEvaler
    TABLE = None  # SQLAlchemy ORM table

    def __init__(self, connection):
        self.columns = []  # type: List[ColumnElement]
        self.where = None  # type: ColumnElement
        self.connection = connection

    def set_columns(self, exprs: List[NamedExprBox]):
        self.columns += [
            self._get_column_with_label(named_expr)
            for named_expr in exprs
        ]

    def set_where(self, expr: ExprBox):
        self.where = self.eval(expr)

    def _get_column_with_label(self, named_expr: NamedExprBox):
        column = self.eval(named_expr.expr)
        name = self._get_name_of_named_expr(named_expr)
        labeled_column = column.label(name)
        return labeled_column

    @staticmethod
    def _get_name_of_named_expr(named_expr: NamedExprBox) -> str:
        name_box = named_expr.name
        if name_box is not None:
            return name_box.value
        names = sorted(named_expr.expr.find_names())
        return '__'.join(names) or '??'

    def generate_select(self) -> Select:
        return Select(
            columns=self.columns,
            whereclause=self.where,
            from_obj=self.TABLE,
        )

    def generate_data(self) -> Iterator[Tuple]:
        select = self.generate_select()
        yield from self.connection(select)
