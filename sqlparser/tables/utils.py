from typing import Dict

from sqlparser.parser import boxes


class SpecialVarError(Exception):
    pass


def special_vars(**kwargs) -> Dict[str, boxes.ExprBox]:
    return {
        key: replace_object_to_expr(value)
        for key, value in kwargs.items()
    }


def replace_object_to_expr(obj) -> boxes.ExprBox:
    if isinstance(obj, int):
        return boxes.IntegerBox(obj)
    elif isinstance(obj, str):
        return boxes.StringBox(obj)
    elif isinstance(obj, boxes.ExprBox):
        return obj
    else:
        raise SpecialVarError(
            'special var {!r} has not supported type: {}'.format(
                obj, type(obj).__name__
            ), obj
        )
