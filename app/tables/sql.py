from typing import List

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm.query import Query

from app.parser.boxes import QueryBox, ExprBox
from app.tables.abstract import AbstractTable


def create_base(uri):
    engine = create_engine(uri)
    base = automap_base()
    base.prepare(engine, reflect=True)
    return base


class SqlTable(AbstractTable):
    TABLE = None
    query = None

    def set_columns(self, exprs: List[ExprBox]):
        columns = None

