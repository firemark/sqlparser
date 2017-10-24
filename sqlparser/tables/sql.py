from typing import Tuple, List, Iterator, Set

from sqlalchemy.sql.elements import ColumnElement  # noqa
from sqlalchemy.sql.expression import Select, ColumnClause

from sqlparser.parser.boxes import ExprBox, NamedExprBox
from sqlparser.tables.abstract import AbstractTable
from sqlparser.evalers.sql import SqlEvaler


class SqlTable(AbstractTable):
    EVALER = SqlEvaler
    TABLE = None  # SQLAlchemy ORM table
    ENGINE = None

    def __init__(self):
        super().__init__()
        self.columns = []  # type: List[ColumnElement]
        self.where = None  # type: ColumnElement
        self.limit = None  # type: int
        self.offset = None  # type: int
        self.group_by = []  # type: List[ColumnElement]
        self.joins = []

    def set_columns(self, exprs: List[NamedExprBox]):
        self.columns += [
            self._get_column_with_label(named_expr)
            for named_expr in exprs
        ]
        self._fill_used_columns(named_expr.expr for named_expr in exprs)

    def set_where(self, expr: ExprBox):
        self.where = self.eval(expr)
        self._fill_used_columns([expr])

    def set_limit(self, limit: str):
        self.limit = limit

    def set_offset(self, offset: int):
        self.offset = offset

    def set_group_by(self, exprs: List[ExprBox]):
        self.group_by = [self.eval(expr) for expr in exprs]
        self._fill_used_columns(exprs)

    def _get_column_with_label(self, named_expr: NamedExprBox):
        column = self.eval(named_expr.expr)
        name = self.get_name_of_named_expr(named_expr)
        labeled_column = column.label(name)
        return labeled_column

    def get_table(self):
        return self.TABLE

    def add_join(
            self,
            child_table,
            parent_column_name,
            child_column_name,
            is_outer=False):
        parent_column = ColumnClause(parent_column_name)
        child_column = ColumnClause(child_column_name)
        condition = (parent_column == child_column)
        self.joins.append((child_table, condition, is_outer))

    def get_used_columns(self):
        return self.used_columns

    def generate_select(self) -> Select:
        table = self.get_table()

        for child_table, condition, is_outer in self.joins:
            if is_outer:
                table = table.outerjoin(child_table, condition)
            else:
                table = table.join(child_table, condition)

        select = Select(
            columns=self.columns,
            whereclause=self.where,
            from_obj=table,
            limit=self.limit,
            offset=self.offset,
            group_by=self.group_by or None,
        )
        return select

    def generate_data(self) -> Iterator[Tuple]:
        self.before_execute()
        select = self.generate_select()
        result = self.ENGINE.execute(select)
        self.after_execute()
        yield result.keys()
        yield from result
