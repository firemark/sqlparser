from typing import Tuple, List, Iterator, Dict, Type, TypeVar, Optional  # noqa
from abc import ABC, abstractmethod

from app.parser.boxes import ExprBox, NamedExprBox
from app.evalers.abstract import AbstractEvaler

T = TypeVar('EvalerType', bound=AbstractEvaler)


class AbstractTable(ABC):
    EVALER = AbstractEvaler # type: Type[T]
    SPECIAL_VARS = None  # type: Dict[str, ExprBox]

    def eval(self, expr: ExprBox, evaler_cls: Type[T]=None):
        evaler = self.make_evaler(expr, evaler_cls)
        return evaler.eval()

    def make_evaler(
            self, expr: ExprBox, evaler_cls=None) -> T:
        evaler_cls = evaler_cls or self.EVALER
        return evaler_cls(expr, special_vars=self.SPECIAL_VARS)

    @abstractmethod
    def set_columns(self, exprs: List[NamedExprBox]):
        raise NotImplementedError('get_columns')

    @abstractmethod
    def set_where(self, expr: ExprBox):
        raise NotImplementedError('get_where')

    @abstractmethod
    def set_limit(self, limit: int):
        raise NotImplementedError('set_limit')

    @abstractmethod
    def set_offset(self, offset: int):
        raise NotImplementedError('set_offset')

    @abstractmethod
    def generate_data(self) -> Iterator[Tuple]:
        """yield rows with N cells"""
        raise NotImplementedError('generate_date')

    @staticmethod
    def get_name_of_named_expr(named_expr: NamedExprBox) -> str:
        name_box = named_expr.name
        if name_box is not None:
            return name_box.value
        names = sorted(named_expr.expr.find_names())
        return '__'.join(names) or '??'
