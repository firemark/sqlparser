import os
import traceback

from prompt_toolkit.contrib.completers.base import WordCompleter

from sqlparser.parser.lex import KEYWORDS

from prompt_toolkit import prompt
from prompt_toolkit.application import AbortAction
from prompt_toolkit.history import FileHistory

from pygments.lexers.sql import SqlLexer


def run_prompt(callback):
    history_path = os.environ.get('SQLPARSER_PROMPTLOG')
    if history_path is None:
        history_path = os.path.join(os.path.expanduser('~'), '.sqlparserlog')
    sql_completer = WordCompleter(KEYWORDS, ignore_case=True)
    print('SQLPARSER!! Ctrl-C to cancel query, Ctrl-D to Exit')
    print()
    history = FileHistory(history_path)
    while True:
        try:
            query = prompt(
                'SQLPARSER >> ',
                history=history,
                on_abort=AbortAction.RETRY,
                lexer=SqlLexer,
                completer=sql_completer,
            )
        except EOFError:
            print('Bye!')
            exit(0)
        try:
            callback(query)
        except:
            traceback.print_exc()
