from rply import LexerGenerator
import re

lg = LexerGenerator()

KEYWORDS = [
    'SELECT', 'FROM', 'AS', 'WHERE', 'LIMIT', 'OFFSET',
    'AND', 'OR', 'LIKE', 'GROUP BY'
]

lg.add('SELECT', 'SELECT', flags=re.IGNORECASE)
lg.add('FROM', 'FROM', flags=re.IGNORECASE)
lg.add('AS', 'AS', flags=re.IGNORECASE)
lg.add('WHERE', 'WHERE', flags=re.IGNORECASE)
lg.add('LIMIT', 'LIMIT', flags=re.IGNORECASE)
lg.add('OFFSET', 'OFFSET', flags=re.IGNORECASE)
lg.add('FLOAT', r'[+-]*(\d*\.\d+|\d+\.)')
lg.add('INTEGER', r'[+-]*\d+')
lg.add('STRING', r"'(\\'|[^'])+'")
lg.add('PAREN_LEFT', r'\(')
lg.add('PAREN_RIGHT', r'\)')
lg.add('OP_ADD', r'\+')
lg.add('OP_SUB', r'-')
lg.add('OP_MUL', r'\*')
lg.add('OP_DIV', r'/')
lg.add('OP_OR', r'OR', flags=re.IGNORECASE)
lg.add('OP_AND', r'AND', flags=re.IGNORECASE)
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
