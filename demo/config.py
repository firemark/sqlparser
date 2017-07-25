from sqlalchemy.sql.expression import table

from app.tables.sql import SqlTable, create_engine_and_base
from app.table_manager import TableManager

engine, base = create_engine_and_base('sqlite:///demo.db')
#connection = engine.get_connection()

manager = TableManager()


@manager.register('sql_airline')
class AirlineSqlTable(SqlTable):
    TABLE = table('airline')
    CONNECTION = engine
