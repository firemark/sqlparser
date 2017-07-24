from rply import LexerGenerator

lg = LexerGenerator()

lg.add('SELECT', 'SELECT')
lg.add('FROM', 'FROM')
lg.add('AS', 'AS')
lg.add('WHERE', 'WHERE')
lg.add('INTEGER', r'[+-]*\d+')
lg.add('PAREN_LEFT', r'\(')
lg.add('PAREN_RIGHT', r'\)')
lg.add('OP_ADD', r'\+')
lg.add('OP_SUB', r'-')
lg.add('OP_MUL', r'\*')
lg.add('OP_DIV', r'/')
lg.add('OP_OR', r'OR')
lg.add('OP_AND', r'AND')
lg.add('OP_LTE', r'<=')
lg.add('OP_GTE', r'>=')
lg.add('OP_LT', r'<')
lg.add('OP_GT', r'>')
lg.add('OP_NEQ', r'!=')
lg.add('OP_EQ', r'=')
lg.add('NAME', r'"(\\"|[^"])+"|[a-zA-Z_]\w*')
lg.add('STRING', r"'(\\'|[^'])+'")
lg.add('DOT', r'\.')
lg.add('COMMA', ',')

lg.ignore(r'\s+')

lexer = lg.build()
