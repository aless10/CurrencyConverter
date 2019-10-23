import configparser
import os


class ConvertAppConfiguration:
    config_parser = configparser.ConfigParser(os.environ)
    app_conf_path = os.environ["CONVERT_APP_CONFIG"]
    config_parser.read(app_conf_path)

    # Basic Flask Configuration values
    FLASK_ENV = config_parser.get('app', 'env')
    ENV = config_parser.get('app', 'env')
    DEBUG = config_parser.getboolean("app", "debug")
    TESTING = config_parser.getboolean("app", "testing")
    LOG_CONF = config_parser.get("logging", "log_conf_path")
    USE_CACHE = config_parser.getboolean("cache", "use_cache")
    REDIS_HOST = config_parser.get("cache", "redis_host")
    REDIS_PORT = config_parser.get("cache", "redis_port")
    DATABASE_CONNECTION_URI = config_parser.get("database", "db_connection")
    SOURCE_URL = config_parser.get("data", "source_url")
