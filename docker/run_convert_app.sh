#!/usr/bin/env bashexport HOME=$(pwd)export ENV=developmentexport PYTHONPATH=/appexport GUNICORN_HOST="0.0.0.0"export GUNICORN_PORT="5001"export GUNICORN_APP_PATH="${HOME}convert_app"export GUNICORN_APP_MODULE="convert_app.app:convert_app"export GUNICORN_WORKERS_NUMBER="1"export GUNICORN_TIMEOUT="60"export GUNICORN_BIND="${GUNICORN_HOST}:${GUNICORN_PORT}"gunicorn --reload --capture-output --bind ${GUNICORN_BIND} --workers ${GUNICORN_WORKERS_NUMBER} --timeout ${GUNICORN_TIMEOUT} ${GUNICORN_APP_MODULE}