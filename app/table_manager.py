from app.parser.parser import parser
from app.parser.lex import lexer
from app.output.csv_output import CsvOutput
from app.parser.boxes import QueryBox
from app.tables.abstract import AbstractTable

from sys import stdout



class TableManager(object):

    def __init__(self):
        self.table_classes = {}

    def register(self, name: str, cls=None):
        def inner(cls):
            self.table_classes[name] = cls
            return cls

        return inner if cls is None else inner(cls)

    def execute_query(self, query: str, stream=None, output_cls=None):
        output_cls = output_cls or CsvOutput
        output = output_cls()
        query_box = parser.parse(lexer.lex(query))  # type: QueryBox
        table_name = query_box.froms[0].value
        table_class = self.table_classes[table_name]
        table = table_class()  # type: AbstractTable

        table.set_columns(query_box.exprs)

        if query_box.where is not None:
            table.set_where(query_box.where)

        if query_box.limit is not None:
            table.set_limit(query_box.limit)

        if query_box.offset is not None:
            table.set_offset(query_box.offset)

        stream = stream or stdout
        generator = table.generate_data()
        first_row = next(generator)

        stream.write(output.parse_first_row(first_row))
        for row in generator:
            stream.write(output.parse_row(row))
