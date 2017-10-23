#!/usr/bin/env python3
import sqlite3
import csv
import os

if os.path.isfile('demo.db'):
    os.remove('demo.db')
conn = sqlite3.connect('demo.db')

c = conn.cursor()
c.execute("""
    CREATE TABLE airline (
      "year" INTEGER,
      "month" INTEGER,
      "day" INTEGER,
      "carrier" TEXT,
      "origin" TEXT,
      "origin_city" TEXT,
      "dest" TEXT,
      "dest_city" TEXT,
      "cancelled" INTEGER,
      "air_time" INTEGER,
      "distance" INTEGER,
      "arr_time" TEXT,
      "dep_time" TEXT
    );
""")


with open('data.csv') as f:
    reader = csv.DictReader(f)
    for obj in reader:
        c.execute(
            """
              INSERT INTO airline
              (year, month, day, origin, dest, origin_city, dest_city,
              cancelled, air_time, distance, carrier, arr_time, dep_time)
              VALUES
              (:YEAR, :MONTH, :DAY_OF_MONTH, :ORIGIN, :DEST,
              :ORIGIN_CITY_NAME, :DEST_CITY_NAME,
              :CANCELLED, :AIR_TIME, :DISTANCE, :CARRIER, :ARR_TIME, :DEP_TIME)
            """,
            obj
        )

conn.commit()
c.close()
conn.close()
