from sqlalchemy.orm.query import Query

from app.evalers.sql import SqlEvaler
from app.parser.parser import parser
from app.parser.lex import lexer


def parse(query: str):
    query_box = parser.parse(lexer.lex(query))  # type: Querybox
    query = Query([])
    for expr in query_box.exprs:
        eval = SqlEvaler(expr.expr).eval()
        query.add_column(eval.label(expr.name.value or str(eval)))
        print(expr.name, eval)
    print(query)
