# develop setup

`docker build -t sqlparser ..`

# airline demo

## setup

`docker-compose run --rm bash -c "cd /demo/airline/ && do_all.sh"`

## run

`docker-compose run --rm -e SQLPARSER_CONFIG=/demo/airline/docker_config.py`

# user and reports demo

## setup

`docker-compose run --rm sqlparser sh -c "cd /demo/user_and_reports/ && ./do_all.sh"`

## run

`docker-compose run --rm -e SQLPARSER_CONFIG=/demo/user_and_reports/config.py sqlparser`
