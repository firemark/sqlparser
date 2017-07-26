import sys
import os
import argparse

parser = argparse.ArgumentParser(
    description='Execute query and return data',
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

from importlib.machinery import SourceFileLoader
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

from sqlparser.prompt import run_prompt
run_prompt(execute)
