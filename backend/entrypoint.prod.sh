#!/bin/bash

set -e
set -u

local database=$SQL_DATABASE
echo "  Creating user and database '$database'"
psql -v ON_ERROR_STOP=1 --username "$SQL_USER" <<-EOSQL
    CREATE USER $database;
    CREATE DATABASE $database;
    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL


exec "$@"
