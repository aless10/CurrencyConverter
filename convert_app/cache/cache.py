from redis import StrictRedis

redis_connection = None


def setup_redis_connection(_app):

    global redis_connection
    if _app.config['USE_CACHE']:
        redis_connection = StrictRedis(
            host=_app.config['REDIS_HOST'],
            port=_app.config['REDIS_PORT'],
            db=0
        )
