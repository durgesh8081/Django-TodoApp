#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python -m gunicorn todoapp.asgi:application -k uvicorn.workers.UvicornWorker