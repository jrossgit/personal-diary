#!/bin/bash

set -e
set -u

python scripts/wait-for-it.py

python manage.py flush --no-input
python manage.py migrate

exec "$@"
