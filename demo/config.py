from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import table

from app.tables.sql import SqlTable
from app.table_manager import TableManager

engine = create_engine('sqlite:///demo.db')
manager = TableManager()


@manager.register('sql_airline')
class AirlineSqlTable(SqlTable):
    TABLE = table('airline')
    ENGINE = engine
