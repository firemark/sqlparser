#!/usr/bin/env python3
import psycopg2

from random import randint
from datetime import date, timedelta

conn = psycopg2.connect(
    dbname='demo', user='demo', password='demo', host='postgres',
)
c = conn.cursor()
c.execute("""
    CREATE TABLE adv (
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      pricing_model INTEGER DEFAULT 0,
      cpa_goal NUMERIC(4, 2) DEFAULT 0 NOT NULL,
      roas_goal NUMERIC(4, 2) DEFAULT 0 NOT NULL);
""")

c.execute("""
    CREATE TABLE reports (
      adv_id INTEGER REFERENCES adv (id),
      report_dt DATE NOT NULL,
      imps INTEGER NOT NULL,
      clicks INTEGER NOT NULL,
      convs INTEGER NOT NULL,
      spend NUMERIC(10, 2) NOT NULL,
      revenue NUMERIC(10, 2) NOT NULL,
      PRIMARY KEY (adv_id, report_dt));
""")


def make_adv(i):
    obj = {
        'username': 'Adv-%d' % i,
        'email': 'adv_%d@foobar.com' % i,
        'pricing_model': i % 2,
        'cpa_goal': randint(2, 10),
        'roas_goal': randint(0, 10),
    }
    c.execute("""
        INSERT INTO adv (username, email, pricing_model, cpa_goal, roas_goal)
        VALUES (
            %(username)s, %(email)s, %(pricing_model)s,
            %(cpa_goal)s, %(roas_goal)s)
        RETURNING id;
    """, obj)
    adv_id = c.fetchone()[0]
    for day in range(365 * 2):
        make_report(adv_id, day)


def make_report(adv_id, day):
    obj = {
        'adv_id': adv_id,
        'report_dt': date(2017, 6, 6) + timedelta(days=day),
        'clicks': randint(100, 1000),
        'imps': randint(1000, 5000),
        'convs': randint(10, 250),
        'spend': randint(20, 300),
        'revenue': randint(10, 300),
    }
    c.execute("""
        INSERT INTO reports (
            adv_id, report_dt, imps, clicks, convs, spend, revenue)
        VALUES (
            %(adv_id)s, %(report_dt)s, %(imps)s, %(clicks)s, %(convs)s,
            %(spend)s, %(revenue)s)
    """, obj)


for i in range(20):
    make_adv(i)


conn.commit()
c.close()
conn.close()

print('Postgres Done!')
