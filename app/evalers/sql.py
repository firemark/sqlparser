
from sqlalchemy.sql.functions import Function

from app.evalers.abstract import AbstractEvaler
from app.parser.boxes import FuncBox, NameBox
from sqlalchemy.sql import expression, column, literal


class SqlEvaler(AbstractEvaler):
    OPS = AbstractEvaler.OPS.copy()
    OPS.update({
        'OP_AND': expression.and_,
        'OP_OR': expression.or_,
    })

    def eval_integer(self):
        return literal(self.expr.value)

    def eval_string(self):
        return literal(self.expr.value)

    def eval_name(self):
        expr = self.expr  # type: NameBox
        return column(expr.value)

    def eval_func(self):
        expr = self.expr  # type: FuncBox
        args = [self.eval_again(arg) for arg in expr.args]
        return Function(self.expr.name, *args)
