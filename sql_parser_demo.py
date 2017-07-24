from sqlalchemy.sql.expression import select, table

from app.evalers.sql import SqlEvaler
from app.parser.parser import parser
from app.parser.lex import lexer


def parse(query: str):
    query_box = parser.parse(lexer.lex(query))
    cols = []
    for expr in query_box.exprs:
        eval = SqlEvaler(expr.expr).eval()
        column = eval.label(expr.name.value if expr.name else str(eval))
        cols.append(column)
    statement = select(cols, from_obj=table('users'))
    return str(statement.compile(
        compile_kwargs={"literal_binds": True},
    ))


if __name__ == "__main__":
    from sys import argv
    print(parse(argv[1]))