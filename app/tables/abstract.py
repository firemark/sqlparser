from typing import Tuple, List, Iterator, Dict, Type  # noqa

from app.parser.boxes import ExprBox, NamedExprBox
from app.evalers.abstract import AbstractEvaler


class AbstractTable(object):
    EVALER = AbstractEvaler # type: Type[AbstractEvaler]
    SPECIAL_VARS = None  # type: Dict[str, ExprBox]

    def eval(self, expr: ExprBox):
        return self.EVALER(expr, special_vars=self.SPECIAL_VARS).eval()

    def set_columns(self, exprs: List[NamedExprBox]):
        raise NotImplementedError('get_columns')

    def set_where(self, expr: ExprBox):
        raise NotImplementedError('get_where')

    def generate_data(self) -> Iterator[Tuple]:
        """yield rows with N cells"""
        raise NotImplementedError('generate_date')
