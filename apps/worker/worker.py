import os
import time
import redis
from rq import Worker, Queue

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
LISTEN_QUEUES = ["default", "incidents"]

def run_worker():
    print(f"[*] Starting AIOps background worker connecting to {REDIS_URL}...")
    while True:
        try:
            conn = redis.from_url(REDIS_URL)
            conn.ping()
            print("[✓] Redis connection confirmed. Listening on queues:", LISTEN_QUEUES)
            queues = [Queue(name, connection=conn) for name in LISTEN_QUEUES]
            worker = Worker(queues, connection=conn)
            worker.work()
        except redis.exceptions.ConnectionError as e:
            print(f"[!] Redis connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"[!] Unexpected error in worker: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_worker()
