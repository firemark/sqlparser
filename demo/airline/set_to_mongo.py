#!/usr/bin/env python
from pymongo import MongoClient
import csv

conn = MongoClient('localhost', 6961)
db = conn.demo
airline = db.airline


with open('data.csv') as f:
    reader = csv.DictReader(f)
    for obj in reader:
        obj['CANCELLED'] = bool(obj['CANCELLED'])
        obj['YEAR'] = int(obj['YEAR'])
        obj['MONTH'] = int(obj['MONTH'])
        obj['DAY_OF_MONTH'] = int(obj['DAY_OF_MONTH'])
        obj['AIR_TIME'] = float(obj['AIR_TIME']) if obj['AIR_TIME'] else None
        obj['DISTANCE'] = float(obj['DISTANCE']) if obj['DISTANCE'] else None

        obj = {key.lower(): value for key, value in obj.items()}
        airline.insert_one(obj)

conn.close()
