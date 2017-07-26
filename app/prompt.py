import os
import traceback

from prompt_toolkit.contrib.completers.base import WordCompleter

from app.parser.lex import KEYWORDS

from prompt_toolkit import prompt
from prompt_toolkit.application import AbortAction
from prompt_toolkit.history import FileHistory
from prompt_toolkit.token import Token

from pygments.lexers.sql import SqlLexer


history_path = os.path.join(os.path.expanduser('~'), '.sqlparserlog')
sql_completer = WordCompleter(KEYWORDS, ignore_case=True)


def run_prompt(callback):
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
