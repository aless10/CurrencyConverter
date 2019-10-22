import os
from unittest import mock
import flask
import pytest

from convert_app.app_factory import create_app

pytest_plugins = ['tests.fixtures_test_db']

LOCAL_SERVER_NAME = '127.0.0.1:5000'


class TestConfiguration:
    TESTING = True
    SERVER_NAME = LOCAL_SERVER_NAME
    LOG_CONF = "local_run/local_log_config.ini"
    USE_CACHE = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    DATABASE_CONNECTION_URI = "mongodb://"


@pytest.fixture
def app(mock_config):
    """Create and configure a new app instance for each test."""
    with mock.patch("convert_app.app_factory.setup_logging"):
        test_app = create_app(TestConfiguration)
        with test_app.app_context():
            yield test_app


@pytest.fixture
def mock_config(monkeypatch):
    monkeypatch.setenv('CONVERT_APP_CONFIG', os.path.join(os.path.dirname(__file__), 'test_local_config.ini'))


@pytest.fixture
def dummy_api(app):
    dummy_blueprint = flask.blueprints.Blueprint('dummy blueprint',
                                                 __name__,
                                                 url_prefix='/api/dummy')
    app.register_blueprint(dummy_blueprint)
    return dummy_blueprint


def register_app_endpoints(app):
    from convert_app.api.blueprint import v1
    app.register_blueprint(v1)


@pytest.fixture
def client(app):
    """A test client for the app."""
    register_app_endpoints(app)
    return app.test_client()


def raise_exception(*args, **kwargs):
    raise Exception("Function that raises exception")
