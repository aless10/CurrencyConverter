#!/usr/bin/env bash

export HOME=$(pwd)


mkdir -p ${HOME}/local_run/logs
export ENV=development
export CONVERT_APP_CONFIG=${HOME}/local_run/local_config.ini
export LOG_CONF=${HOME}/local_run/local_log_config.ini
export LOG_PATH=${HOME}/local_run/logs
export LOG_LEVEL=DEBUG

export REDIS_CONF=${HOME}/conf/redis.conf
export USE_REDIS_CACHE=true
export REDIS_HOST_ADDRESS="127.0.0.1"
export REDIS_PORT_BIND=6379

export PYTHONPATH=${HOME}

export GUNICORN_HOST="0.0.0.0"
export GUNICORN_PORT="5001"
export GUNICORN_APP_PATH="${PYTHONPATH}convert_app"
export GUNICORN_APP_MODULE="helixa_app.app:convert_app"
export GUNICORN_WORKERS_NUMBER="1"
export GUNICORN_TIMEOUT="60"
export GUNICORN_BIND="${GUNICORN_HOST}:${GUNICORN_PORT}"

redis-server ${REDIS_CONF}
# RUNNING MONGO DAEMON
mongod --config /usr/local/etc/mongod.conf

gunicorn --reload --capture-output --bind ${GUNICORN_BIND} --workers ${GUNICORN_WORKERS_NUMBER} --timeout ${GUNICORN_TIMEOUT} ${GUNICORN_APP_MODULE}
