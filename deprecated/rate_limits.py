import asyncio
import datetime
from typing import Dict, List

from aiohttp import ClientResponse
from aiolimiter import AsyncLimiter


class BucketHandler:
    """
    Handles bucket specific rate limits
    {bucket_name: BucketHandler}
    """

    limit: int | None = None
    remaining: int | None = None
    reset: datetime.datetime | None = None
    retry_after: float | None = None
    prevent_429: bool = False
    cond = None

    def __init__(self, bucket: str):
        self.bucket = bucket

    def __repr__(self):
        return (
            f"RateLimit(bucket={self.bucket}, limit={self.limit}, remaining={self.remaining}, "
            f"reset={self.reset}, retry_after={self.retry_after})"
        )

    def check_limit_headers(self, r: ClientResponse):
        limits = {}
        header_attrs = {
            "X-RateLimit-Limit": "limit",
            "X-RateLimit-Remaining": "remaining",
            "X-RateLimit-Reset": "reset",
        }
        for key in header_attrs:
            value = r.headers.get(key)
            if value is not None:
                if key == "X-RateLimit-Reset":
                    value = datetime.datetime.fromtimestamp(float(value), datetime.UTC)
            limits[header_attrs[key]] = value
        for k, v in limits.items():
            setattr(self, k, v)

    async def __aenter__(self):
        self.cond = self.cond or asyncio.Condition(loop=asyncio.get_running_loop())  # type: ignore
        if self.prevent_429 is True:
            await self.cond.acquire()
            if self.remaining is not None and self.remaining == 0:
                now = datetime.datetime.now(datetime.UTC)
                to_wait = (self.reset - now).total_seconds() + 1  # type: ignore
                await asyncio.sleep(to_wait)
        return self

    async def __aexit__(self, *args):
        if self.prevent_429 is True:
            self.cond.release()  # type: ignore


class ClientRateLimits:
    buckets: Dict[str, BucketHandler] = dict()

    def __init__(self):
        self.global_limiter = AsyncLimiter(50, 1)  # 50 requests per second

    def currently_limited(self) -> List[str]:
        """
        Returns:
            Returns a list of the buckets (str) that are currently being limited.
        """
        now = datetime.datetime.now(datetime.UTC)
        limited = [
            k
            for k, v in self.buckets.items()
            if v.reset is not None and v.reset > now and v.remaining == 0
        ]
        return limited

    def any_limited(self) -> bool:
        """
        Returns:
            True if any bucket is being rate limited
        """
        return any(self.currently_limited())

    def is_limited(self, bucket: str):
        return bucket in self.currently_limited()
