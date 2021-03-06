import datetime
import logging
import os
import uuid

from logging.config import fileConfig
from flask import Flask, g, request

from convert_app.api import blueprint
from convert_app.api.index import index
from convert_app.api.swagger import swaggerui_blueprint
from convert_app.cache.cache import setup_redis_connection
from convert_app.db.init_db import init_db

log = logging.getLogger(__name__)

blueprints = (index, swaggerui_blueprint, blueprint.v1, blueprint.views_v1)


def register_blueprint(flask_app, _blueprints=()):
    for flask_blueprint in _blueprints:
        flask_app.register_blueprint(flask_blueprint)


def register_request_callbacks(flask_app):
    def begin_request():
        g.start = datetime.datetime.now()
        g.x_request_id = request.headers.get('X-Request-ID', uuid.uuid4())
        flask_app.logger.info(
            "Received a new request x_request_id[%s] args[%s] method[%s] endpoint[%s]",
            g.x_request_id,
            request.args,
            request.method,
            request.path
        )

    def end_request(response):
        request.direct_passthrough = False
        duration = datetime.datetime.now() - g.start
        log.info(
            'PERF x_request_id[%s] time[%s] method[%s] endpoint[%s] status[%s]',
            g.x_request_id,
            duration,
            request.method,
            request.path,
            response.status
        )
        log.debug('RESPONSE x_request_id[%s]', g.x_request_id)
        response.headers['X-Request-ID'] = g.x_request_id
        response.headers['X-Time-Elapsed'] = duration
        return response

    flask_app.before_request(begin_request)
    flask_app.after_request(end_request)


def setup_logging(configuration):
    fileConfig(configuration.LOG_CONF, defaults=os.environ)


def create_app(config_obj):
    app = Flask('convert_app')
    app.config.from_object(config_obj)
    register_request_callbacks(app)
    register_blueprint(app, _blueprints=blueprints)
    app.url_map.strict_slashes = False
    setup_logging(config_obj)
    setup_redis_connection(app)
    init_db(config_obj)
    return app


def run_app(app):
    try:
        log.debug("Starting the Currency Converter Application with config: %s", app.config)
        app.run()
    except Exception:
        log.error("Error while running the application. Please check if you set the env variables: "
                  "CONVERT_APP_CONFIG: path to the config file;\n"
                  "LOG_PATH: path to log folder;\n"
                  "LOG_LEVEL: log level for the application;\n"
                  "LOG_CONF: path to log config file\n"
                  "REDIS_HOST_ADDRESS=host of the redis server (e.g 127.0.0.1)\n"
                  "REDIS_PORT_BIND=6379\n"
                  "USE_REDIS_CACHE=true if you want to use redis as cache else false\n"
                  "DATABASE_CONNECTION=mongodb connection string (e.g. mongodb://127.0.0.1:27017/)\n"
                  "DATA_SOURCE_URL=https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml")
        raise
