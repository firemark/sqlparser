from pymongo.mongo_client import MongoClient

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import table


from sqlparser.tables.sql import SqlTable
from sqlparser.table_manager import TableManager
from sqlparser.tables.mongo import MongoTable
from sqlparser.tables.utils import special_vars, sql

mongo = MongoClient('mongo')
engine = create_engine('postgresql://demo:demo@postgres/demo')
manager = TableManager()

reports_specials = special_vars(
    cpa=sql('sum(reports.spend) / sum(reports.convs)'),
    cpc=sql('sum(reports.spend) / sum(reports.clicks)'),
    cpm=sql('sum(reports.revenue) / sum(reports.imps)'),
    ctr=sql('sum(reports.clicks)::float / sum(reports.imps)'),
    roas=sql('sum(reports.convs) / sum(reports.revenue)'),
    imps=sql('sum(reports.imps)'),
    clicks=sql('sum(reports.clicks)'),
    convs=sql('sum(reports.convs)'),
    spend=sql('sum(reports.spend)'),
    revenue=sql('sum(reports.revenue)'),
    report_dt=sql('reports.report_dt'),
)

specials = special_vars(
    is_cpa=sql('pricing_model = 0'),
    is_cpm=sql('pricing_model = 1'),
)
specials.update(reports_specials)


@manager.register('sql_adv')
class AirlineSqlTable(SqlTable):
    TABLE = table('adv')
    ENGINE = engine
    SPECIAL_VARS = specials

    def before_execute(self):
        used_columns = self.get_used_columns()
        if not any(var in used_columns for var in reports_specials):
            return

        report_table = table('reports')
        self.add_join(report_table, 'id', 'adv_id')
        if not self.group_by:
            self.set_group_by([sql('id')])


@manager.register('mongo_adv')
class AirlineMongoTable(MongoTable):
    TABLE = mongo.demo.adv
    SPECIAL_VARS = specials
