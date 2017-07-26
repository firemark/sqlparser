from pymongo.mongo_client import MongoClient

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import table

from sqlparser.tables.sql import SqlTable
from sqlparser.table_manager import TableManager
from sqlparser.tables.mongo import MongoTable

mongo = MongoClient('localhost', 6961)
engine = create_engine('postgresql://demo:demo@0:6960/demo')
manager = TableManager()


@manager.register('sql_airline')
class AirlineSqlTable(SqlTable):
    TABLE = table('airline')
    ENGINE = engine


@manager.register('mongo_airline')
class AirlineMongoTable(MongoTable):
    TABLE = mongo.demo.airline
