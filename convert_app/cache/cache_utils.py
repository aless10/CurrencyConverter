import json
import logging
from _md5 import md5
from functools import wraps

from flask import current_app, request, jsonify
from redis import exceptions as redis_exceptions

log = logging.getLogger(__name__)

REDIS_EXPIRE = 3600


def call_redis(cmd, *args, **kwargs):
    try:
        return cmd(*args, **kwargs)
    except (redis_exceptions.ConnectionError, redis_exceptions.TimeoutError):
        log.error(
            'connection to redis server failed: '
            'host=%s port=%s' % (
                current_app.config["REDIS_HOST"],
                current_app.config["REDIS_PORT"]))
        return None


def build_key_from_request(body):
    result = ":".join([f"{k}|{v}" for k, v in body.items()])
    return md5(result.encode('utf-8')).hexdigest()


def cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_app.config['USE_CACHE']:
            print("Here's the cache")
            from convert_app.cache.cache import redis_connection
            request_body = request.args
            cache_key = build_key_from_request(request_body)
            from_cache = call_redis(redis_connection.get, cache_key)
            print(f"Here's the cache {from_cache}")
            if from_cache is None:
                result = fn(*args, **kwargs)
                log.debug('cache get MISS setting key %s to value %s', cache_key, result)
                call_redis(redis_connection.set, cache_key, result.data, ex=REDIS_EXPIRE)
            else:
                print("Here's the cache call")
                log.debug('cache get HIT got value %s from key %s', from_cache, cache_key)
                # from_cache is bytes so we need to translate it into json
                json_cache = json.loads(from_cache.decode("utf-8"))
                result = jsonify(json_cache)
        else:
            result = fn(*args, **kwargs)
        return result
    return wrapper
