from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimit:
    requests: int
    window_seconds: int


RATE_LIMITS = {
    "free": RateLimit(requests=60, window_seconds=60),       # 60 req / min
    "pro": RateLimit(requests=600, window_seconds=60),       # 600 req / min
    "enterprise": RateLimit(requests=5000, window_seconds=60),
}
