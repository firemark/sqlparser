from rply import LexerGenerator
import re

lg = LexerGenerator()

KEYWORDS = [
    'SELECT', 'FROM', 'AS', 'WHERE', 'LIMIT', 'OFFSET',
    'AND', 'OR', 'LIKE', 'GROUP BY'
]

OPERATORS = [
    'OP_ADD', 'OP_SUB',
    'OP_MUL', 'OP_DIV', 'OP_MOD',
    'OP_AND', 'OP_OR',
    'OP_LT', 'OP_GT',
    'OP_LTE', 'OP_GTE',
    'OP_EQ', 'OP_NEQ',
    'OP_BITWISE_OR', 'OP_BITWISE_AND', 'OP_BITWISE_XOR',
    'OP_LIKE', 'OP_NOT_LIKE',
    'OP_IN', 'OP_NOT_IN',
    'OP_LSHIFT', 'OP_RSHIFT',
]

SINGLE_OPERATORS = [
    'OP_NOT', 'OP_BITWISE_NOT',
    'OP_ABSOLUTE',
    'OP_ADD',
    'OP_SUB',
]

lg.add('SELECT', r'SELECT\b', flags=re.IGNORECASE)
lg.add('FROM', r'FROM\b', flags=re.IGNORECASE)
lg.add('AS', r'AS\b', flags=re.IGNORECASE)
lg.add('WHERE', r'WHERE\b', flags=re.IGNORECASE)
lg.add('LIMIT', r'LIMIT\b', flags=re.IGNORECASE)
lg.add('OFFSET', r'OFFSET\b', flags=re.IGNORECASE)
lg.add('GROUP_BY', r'GROUP\s+BY\b', flags=re.IGNORECASE)
lg.add('FLOAT', r'[+-]*(\d*\.\d+|\d+\.)')
lg.add('INTEGER', r'[+-]*\d+')
lg.add('STRING', r"'(\\'|[^'])+'")
lg.add('BOOL', r'TRUE\b|YES\b|NO\b|FALSE\b', flags=re.IGNORECASE)
lg.add('NULL', r'NULL\b', flags=re.IGNORECASE)
lg.add('PAREN_LEFT', r'\(')
lg.add('PAREN_RIGHT', r'\)')
lg.add('BRACKET_LEFT', r'\[')
lg.add('BRACKET_RIGHT', r'\]')
lg.add('OP_ADD', r'\+')
lg.add('OP_SUB', r'-')
lg.add('OP_MUL', r'\*')
lg.add('OP_DIV', r'/')
lg.add('OP_MOD', r'%')
lg.add('OP_LIKE', r'LIKE\b', flags=re.IGNORECASE)
lg.add('OP_NOT_LIKE', r'NOT\s*LIKE\b', flags=re.IGNORECASE)
lg.add('OP_IN', r'IN\b', flags=re.IGNORECASE)
lg.add('OP_NOT_IN', r'NOT\s*IN\b', flags=re.IGNORECASE)
lg.add('OP_OR', r'OR\b', flags=re.IGNORECASE)
lg.add('OP_AND', r'AND\b', flags=re.IGNORECASE)
lg.add('OP_NOT', r'NOT\b', flags=re.IGNORECASE)
lg.add('OP_IS', r'IS\b', flags=re.IGNORECASE)
lg.add('OP_BEETWEN', r'BEETWEN\b', flags=re.IGNORECASE)
lg.add('TYPECAST', '::')
lg.add('OP_BITWISE_NOT', '~')
lg.add('OP_BITWISE_AND', '&')
lg.add('OP_BITWISE_OR', '\|')
lg.add('OP_BITWISE_XOR', '\^')
lg.add('OP_ABSOLUTE', '@')
lg.add('OP_LTE', r'<=')
lg.add('OP_GTE', r'>=')
lg.add('OP_LSHIFT', r'<<')
lg.add('OP_RSHIFT', r'>>')
lg.add('OP_LT', r'<')
lg.add('OP_GT', r'>')
lg.add('OP_NEQ', r'!=')
lg.add('OP_EQ', r'=')
lg.add('NAME', r'"(\\"|[^"])+"|[a-zA-Z_]\w*')
lg.add('DOT', r'\.')
lg.add('COMMA', ',')

lg.ignore(r'\s+')

lexer = lg.build()
