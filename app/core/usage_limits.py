from dataclasses import dataclass

@dataclass(frozen=True)
class UsageLimit:
    max_requests: int


USAGE_LIMITS = {
    "free": UsageLimit(max_requests=10_000),
    "pro": UsageLimit(max_requests=200_000),
    "enterprise": UsageLimit(max_requests=5_000_000),
}
