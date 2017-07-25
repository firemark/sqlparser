import sys
from importlib.machinery import SourceFileLoader

config = sys.argv[1]
module = SourceFileLoader('config.config', config).load_module()
manager = module.manager

if len(sys.argv) > 2:
    query = sys.argv[2]
    manager.execute_query(query)
    exit(0)

try:
    while True:
        query = input('SQLPARSER> ')
        manager.execute_query(query)
except KeyboardInterrupt:
    pass
