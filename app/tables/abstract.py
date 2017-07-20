from typing import List, Iterator

from app.parser.boxes import ExprBox


class AbstractTable(object):

    def set_columns(self, exprs: List[ExprBox]):
        raise NotImplementedError('get_columns')

    def set_where(self, exprs: List[ExprBox]):
        raise NotImplementedError('get_where')

    def generate_data(self) -> Iterator[List]:
        """yield rows with N cells"""
        raise NotImplementedError('generate_date')
        yield []
