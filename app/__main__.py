import sys
import os
import argparse
import traceback

from importlib.machinery import SourceFileLoader
from prompt_toolkit import prompt
from prompt_toolkit.application import AbortAction
from prompt_toolkit.history import FileHistory


parser = argparse.ArgumentParser(
    description='Execute query and return data'
)
parser.add_argument('query', nargs='?', help='SQL query')
parser.add_argument(
    '-c', '--config',
    help='filepath to config file',
    required=True)
parser.add_argument(
    '-o', '--output',
    help='pythonpath to output class (default csv)',
    default=None)

args = parser.parse_args()

module = SourceFileLoader('config.config', args.config).load_module()
manager = module.manager


def execute(query):
    manager.execute_query(query, output_cls=args.output)


if args.query:
    execute(args.query)
    exit(0)

if not os.isatty(0):
    try:
        for query in sys.stdin:
            if not query:
                continue
            execute(query)
    except (KeyboardInterrupt, EOFError):
        pass
    exit(0)


history_path = os.path.join(os.path.expanduser('~'), '.sqlparserlog')
history = FileHistory(history_path)
while True:
    try:
        query = prompt(
            'SQLPARSER >> ',
            history=history,
            on_abort=AbortAction.RETRY,
        )
    except EOFError:
        print('Bye!')
        exit(0)
    try:
        execute(query)
    except:
        traceback.print_exc()
    finally:
        history.append(query)
