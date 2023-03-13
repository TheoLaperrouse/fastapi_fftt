import jsonpickle
import redis

def redis_connect() -> redis.client.Redis:
    '''Connection to the redis container'''
    redis_connection = redis.Redis(
        host="redis",
        port=6379,
        db=0,
        socket_timeout=5,
    )
    return redis_connection

def cache(func):
    """Add a decorator to use cache on function"""
    def wrapper(*args, **kwargs):
        key = jsonpickle.encode((func.__name__, args, kwargs))
        if redis_client.exists(key):
            result = jsonpickle.decode(redis_client.get(key))
        else:
            result = func(*args, **kwargs)
            redis_client.set(key, jsonpickle.encode(result))
        return result
    return wrapper

redis_client = redis_connect()
