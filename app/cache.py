import redis
import json 
import hashlib 

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True
)

def check_redis_conection():
    try:
        return redis_client.ping()
    except redis.RedisError:
        return False


def create_cache_key(question, context=""):
    content = question + context
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_cached_result(question,context=""):
    key = create_cache_key(question,context)

    try:
        cached_data = redis_client.get(key)

        if cached_data:
            return json.loads(cached_data) 

        return None

    except (redis.RedisError, json.JSONDecodeError):
        return None

def set_cached_result(question, context, result, expiration=3600):
    key = create_cache_key(question, context)

    try:
        redis_client.set(
            key,
            json.dumps(result),
            ex=expiration
        )
        return True

    except (redis.RedisError, TypeError, ValueError):
        return False       