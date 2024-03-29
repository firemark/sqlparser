from pymongo.mongo_client import MongoClient

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import table

from sqlparser.tables.sql import SqlTable
from sqlparser.table_manager import TableManager
from sqlparser.tables.mongo import MongoTable
from sqlparser.tables.utils import special_vars

mongo = MongoClient('mongo')
engine = create_engine('postgresql://demo:demo@postgres/demo')
manager = TableManager()
specials = special_vars(
    HOUR=60,
    PORTLAND='Portland, OR'
)


@manager.register('sql_airline')
class AirlineSqlTable(SqlTable):
    TABLE = table('airline')
    ENGINE = engine
    SPECIAL_VARS = specials


@manager.register('mongo_airline')
class AirlineMongoTable(MongoTable):
    TABLE = mongo.demo.airline
    SPECIAL_VARS = specials
