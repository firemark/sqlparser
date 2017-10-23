import sys
import os
import argparse

from importlib.machinery import SourceFileLoader


def main():
    parser = argparse.ArgumentParser(
        description='Execute query and return data',
    )
    parser.add_argument('query', nargs='?', help='SQL query')
    parser.add_argument(
        '-c', '--config',
        default=os.environ.get('SQLPARSER_CONFIG'),
        help='filepath to config file')
    parser.add_argument(
        '-o', '--output',
        help='pythonpath to output class (default csv)',
        default=os.environ.get('SQLPARSER_OUTPUT'))

    args = parser.parse_args()
    if args.config is None:
        sys.stderr.write('Please set env SQLPARSER_CONFIG or set -c flag!\n')
        exit(1)

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

if __name__ == "__main__":
    main()
