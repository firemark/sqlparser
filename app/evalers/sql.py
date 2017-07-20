from sqlalchemy.sql.functions import Function

from app.evalers.abstract import AbstractEvaler
from sqlalchemy.sql import expression


class SqlEvaler(AbstractEvaler):
    OPS = AbstractEvaler.OPS.copy()
    OPS.update({
        'OP_AND': expression.and_,
        'OP_OR': expression.or_,
    })

    def eval_integer(self):
        return self.expr.value

    def eval_string(self):
        return self.expr.value

    def eval_func(self):
        args = [self.eval_again(arg) for arg in self.expr.args]
        return Function(self.expr.name, args)
