from sqlparser.parser.lex import lexer


def get_token(data):
    return lexer.lex(data).next().name


def test_name():
    assert get_token('column') == 'NAME'


def test_quoted_name():
    assert get_token('"super \\" name"') == 'NAME'


def test_int():
    assert get_token('5') == 'INTEGER'


def test_string():
    assert get_token("'a \\'string") == 'STRING'


def test_float():
    assert get_token("+-1.0") == 'FLOAT'


def test_float_only_part():
    assert get_token(".1") == 'FLOAT'


def test_float_only_base():
    assert get_token("1.") == 'FLOAT'


def test_select():
    assert get_token('SELECT') == 'SELECT'
