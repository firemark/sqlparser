from rply import LexerGenerator
import re

lg = LexerGenerator()

KEYWORDS = [
    'SELECT', 'FROM', 'AS', 'WHERE', 'LIMIT', 'OFFSET',
    'AND', 'OR', 'LIKE', 'GROUP BY'
]

lg.add('SELECT', r'SELECT\b', flags=re.IGNORECASE)
lg.add('FROM', r'FROM\b', flags=re.IGNORECASE)
lg.add('AS', r'AS\b', flags=re.IGNORECASE)
lg.add('WHERE', r'WHERE\b', flags=re.IGNORECASE)
lg.add('LIMIT', r'LIMIT\b', flags=re.IGNORECASE)
lg.add('OFFSET', r'OFFSET\b', flags=re.IGNORECASE)
lg.add('FLOAT', r'[+-]*(\d*\.\d+|\d+\.)')
lg.add('INTEGER', r'[+-]*\d+')
lg.add('STRING', r"'(\\'|[^'])+'")
lg.add('PAREN_LEFT', r'\(')
lg.add('PAREN_RIGHT', r'\)')
lg.add('OP_ADD', r'\+')
lg.add('OP_SUB', r'-')
lg.add('OP_MUL', r'\*')
lg.add('OP_DIV', r'/')
lg.add('OP_OR', r'OR\b', flags=re.IGNORECASE)
lg.add('OP_AND', r'AND\b', flags=re.IGNORECASE)
lg.add('OP_LTE', r'<=')
lg.add('OP_GTE', r'>=')
lg.add('OP_LT', r'<')
lg.add('OP_GT', r'>')
lg.add('OP_NEQ', r'!=')
lg.add('OP_EQ', r'=')
lg.add('NAME', r'"(\\"|[^"])+"|[a-zA-Z_]\w*')
lg.add('DOT', r'\.')
lg.add('COMMA', ',')

lg.ignore(r'\s+')

lexer = lg.build()
