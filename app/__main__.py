import sys
from importlib.machinery import SourceFileLoader

config, query = sys.argv[1:3]
module = SourceFileLoader('config.config', config).load_module()
manager = module.manager
manager.execute_query(query)
