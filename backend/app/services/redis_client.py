import redis

# Connect Python to Redis
# Redis runs on localhost port 6379 via Docker
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def get_redis():
    return r


def test_connection():
    try:
        r.ping()
        print("Redis Connected Successfully!")
        return True
    except Exception as e:
        print(f"Redis Error: {e}")
        return False