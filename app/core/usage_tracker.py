import datetime
import threading
from typing import Dict

from app.core.usage_limits import USAGE_LIMITS


class UsageTracker:
    def __init__(self):
        self.cache: Dict[str, dict] = {}
        self.lock = threading.Lock()

    def _current_month(self) -> str:
        now = datetime.datetime.utcnow()
        return f"{now.year}-{now.month}"

    def increment(self, api_key: str, plan: str) -> bool:
        """
        Returns False if limit exceeded
        """
        limit = USAGE_LIMITS.get(plan)
        if not limit:
            return False

        month = self._current_month()

        with self.lock:
            data = self.cache.get(api_key)

            if not data or data["month"] != month:
                self.cache[api_key] = {
                    "month": month,
                    "count": 1
                }
                return True

            if data["count"] >= limit.max_requests:
                return False

            data["count"] += 1
            return True


usage_tracker = UsageTracker()
