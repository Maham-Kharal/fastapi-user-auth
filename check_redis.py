import asyncio
import redis
from arq import create_pool
from arq.connections import RedisSettings

def check_keys():
    r = redis.Redis(host='127.0.0.1', port=6380)
    keys = [k.decode() for k in r.keys('*')]
    print("=== REDIS KEYS ===")
    print("Keys count:", len(keys))
    for k in keys:
        print(f" - {k}")

    if r.exists("arq:queue"):
        queue_items = [x.decode() for x in r.zrange("arq:queue", 0, -1)]
        print("\n=== ARQ QUEUE ITEMS ===")
        for item in queue_items:
            print(f" - {item}")

if __name__ == "__main__":
    check_keys()
