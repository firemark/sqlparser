#!/usr/bin/env sh
set -e

./download_data.sh
./set_to_postgres.py
./set_to_mongo.py

