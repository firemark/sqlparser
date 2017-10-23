#!/usr/bin/env python3
import psycopg2
import csv

conn = psycopg2.connect(
    dbname='demo', user='demo', password='demo',
    host='postgres',
)
c = conn.cursor()
c.execute("""
    CREATE TABLE airline (
      "year" INTEGER CONSTRAINT "year" NOT NULL,
      "month" INTEGER CONSTRAINT "month" NOT NULL,
      "day" INTEGER CONSTRAINT "day" NOT NULL,
      "carrier" VARCHAR(255),
      "origin" VARCHAR(255),
      "origin_city" VARCHAR(255),
      "dest" VARCHAR(255),
      "dest_city" VARCHAR(255),
      "cancelled" BOOL,
      "air_time" NUMERIC NULL,
      "distance" NUMERIC NULL,
      "arr_time" VARCHAR(4),
      "dep_time" VARCHAR(4)
    );
""")


with open('data.csv') as f:
    reader = csv.DictReader(f)
    for obj in reader:
        obj['CANCELLED'] = bool(obj['CANCELLED'])
        obj['AIR_TIME'] = float(obj['AIR_TIME']) if obj['AIR_TIME'] else None
        obj['DISTANCE'] = float(obj['DISTANCE']) if obj['DISTANCE'] else None

        c.execute(
            """
              INSERT INTO airline
              ("year", "month", "day", origin, dest, origin_city, dest_city,
              cancelled, air_time, distance, carrier, arr_time, dep_time)
              VALUES
              (%(YEAR)s, %(MONTH)s, %(DAY_OF_MONTH)s, %(ORIGIN)s, %(DEST)s,
              %(ORIGIN_CITY_NAME)s, %(DEST_CITY_NAME)s,
              %(CANCELLED)s, %(AIR_TIME)s, %(DISTANCE)s,
              %(CARRIER)s, %(ARR_TIME)s, %(DEP_TIME)s)
            """,
            obj
        )

conn.commit()
c.close()
conn.close()
