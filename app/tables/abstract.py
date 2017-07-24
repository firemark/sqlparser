from typing import Tuple, List, Iterator, Dict, Type  # noqa
from abc import ABC, abstractmethod

from app.parser.boxes import ExprBox, NamedExprBox
from app.evalers.abstract import AbstractEvaler


class AbstractTable(ABC):
    EVALER = AbstractEvaler # type: Type[AbstractEvaler]
    SPECIAL_VARS = None  # type: Dict[str, ExprBox]

    def eval(self, expr: ExprBox):
        return self.EVALER(expr, special_vars=self.SPECIAL_VARS).eval()

    @abstractmethod
    def set_columns(self, exprs: List[NamedExprBox]):
        raise NotImplementedError('get_columns')

    @abstractmethod
    def set_where(self, expr: ExprBox):
        raise NotImplementedError('get_where')

    @abstractmethod
    def generate_data(self) -> Iterator[Tuple]:
        """yield rows with N cells"""
        raise NotImplementedError('generate_date')
