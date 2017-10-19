
from sqlparser.evalers.abstract import AbstractEvaler, EvalerError
from sqlparser.parser.boxes import TypeCastBox, NameBox
from sqlalchemy.sql import expression, column, literal, func, cast
from sqlalchemy.types import Integer, Numeric, Date, DateTime, Text, String


class SqlEvaler(AbstractEvaler):
    OPS = AbstractEvaler.OPS.copy()
    OPS.update({
        'OP_AND': expression.and_,
        'OP_OR': expression.or_,
    })
    FUNCTIONS = {
        'lower': func.lower,
        'upper': func.upper,
        'concat': func.concat,
        'length': func.length,
        'right': func.right,
        'left': func.left,
        'abs': func.abs,
        'reverse': func.reverse,
        'replace': func.replace,
        'sqrt': func.sqrt,
        'ceil': func.ceil,
        'floor': func.floor,
        'round': func.round,
        'sign': func.sign,
        'sum': func.sum,
        'avg': func.avg,
        'all': func.all,
        'any': func.any,
    }
    TYPES = {
        'int': Integer,
        'integer': Integer,
        'date': Date,
        'datetime': DateTime,
        'numeric': Numeric,
        'float': Numeric,
        'text': Text,
        'str': String,
        'character': String,
    }

    def eval_integer(self):
        return literal(self.expr.value)

    def eval_float(self):
        return literal(self.expr.value)

    def eval_string(self):
        return literal(self.expr.value)

    def eval_name(self):
        expr = self.expr  # type: NameBox
        return column(expr.value)

    def eval_typecast(self):
        expr = self.expr # type: TypeCastBox
        expr_type = self.TYPES.get(expr.to)
        if expr_type is None:
            raise EvalerError('type %s is not supported' % expr.to, expr.to)
        return cast(self.eval_again(expr.value), expr_type)

