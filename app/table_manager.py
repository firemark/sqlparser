from app.parser.parser import parser
from app.parser.lex import lexer


class TableManager(object):

    def __init__(self):
        self.table_classes = {}

    def register(self, name: str, cls=None):
        def inner(cls):
            self.table_classes[name] = cls
            return cls

        return inner if cls is None else inner(cls)

    def execute_query(self, query: str):
        query_box = parser.parse(lexer.lex(query))
        table_name = query_box.froms[0].value
        table_class = self.table_classes[table_name]
        table = table_class()

        table.set_columns(query_box.exprs)

        if query_box.where is not None:
            table.set_where()

        for obj in table.generate_data():
            print(obj)
