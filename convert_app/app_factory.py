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


def register_blueprint(flask_app, blueprints=()):
    for flask_blueprint in blueprints:
        flask_app.register_blueprint(flask_blueprint)


def register_request_callbacks(flask_app):
    def begin_request():
        g.start = datetime.datetime.now()
        g.x_request_id = request.headers.get('X-Request-ID', uuid.uuid4())
        flask_app.logger.info(
            "Received a new request x_request_id[%s] body[%s] method[%s] endpoint[%s]",
            g.x_request_id,
            request.json,
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
    register_blueprint(app, blueprints=(index, swaggerui_blueprint, blueprint.v1,))
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
                  "LOG_CONF: path to log config file")
        raise
