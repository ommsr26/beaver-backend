import time
import threading
from typing import Dict

from app.core.rate_limits import RATE_LIMITS


class RateLimiter:
    def __init__(self):
        self.store: Dict[str, dict] = {}
        self.lock = threading.Lock()

    def is_allowed(self, api_key: str, plan: str) -> bool:
        limit = RATE_LIMITS.get(plan)

        if not limit:
            return False  # Unknown plan → block

        now = time.time()

        with self.lock:
            data = self.store.get(api_key)

            if not data:
                # First request
                self.store[api_key] = {
                    "window_start": now,
                    "count": 1
                }
                return True

            elapsed = now - data["window_start"]

            if elapsed > limit.window_seconds:
                # Reset window
                self.store[api_key] = {
                    "window_start": now,
                    "count": 1
                }
                return True

            if data["count"] >= limit.requests:
                return False

            data["count"] += 1
            return True


rate_limiter = RateLimiter()
