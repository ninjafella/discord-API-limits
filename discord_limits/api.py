import asyncio
import warnings

from aiohttp import ClientResponse, ClientSession

from .errors import *
from .paths import Paths
from .rate_limits import BucketHandler, ClientRateLimits


class DiscordClient(Paths):
    """
    Parameters
    ----------
    token : str
        The token to use for the request.
    token_type : str, optional
        The type of token provided ('bot', 'bearer', 'user', None), by default 'bot'
    prevent_rate_limits : bool, optional
        Whether the client will sleep through ratelimits to prevent 429 errors, by default True
    retry_rate_limits : bool, optional
        Whether the client will sleep and retry after 429 errors, by default True
    api_version : int, optional
        The Discord API version to use (6, 7, 8, 9, 10), by default 10
    """

    def __init__(
        self,
        token: str | None,
        token_type: str | None = "bot",
        prevent_rate_limits: bool = True,
        retry_rate_limits: bool = True,
        api_version: int = 10,
    ):
        super().__init__(self)

        if api_version < 6:
            raise InvalidParams("API version must be 6 or higher.")
        elif api_version < 9:
            warnings.warn(
                f"API version {api_version} is now deprecated by Discord, some endpoints may not work as expected.",
                UserWarning,
            )

        if token_type == "bot":
            self.token = f"Bot {token}"
            self.token_type = token_type
        elif token_type == "bearer":
            self.token = f"Bearer {token}"
            self.token_type = token_type
        elif token_type == "user":
            warnings.warn(
                "Use a user token at your own risk as (depending on your usage) it could be against Discord's ToS. If you are using this token for a bot, you should use the 'bot' token_type instead.",
                UserWarning,
            )
            self.token = f"{token}"
            self.token_type = token_type
        else:
            self.token = None
            self.token_type = None

        self._prevent_rate_limits = prevent_rate_limits
        self._retry_rate_limits = retry_rate_limits
        self.rate_limits = ClientRateLimits(prevent_rate_limits=prevent_rate_limits)
        self._base_url = f"https://discord.com/api/v{api_version}"
        self._base_url_len = len(self._base_url)

    def set_new_token(self, token: str | None, token_type: str | None = "bot") -> None:
        """Set a new token to use.

        Parameters
        ----------
        token : str
            The new token to use for the request.
        token_type : str, optional
            The type of token provided ('bot', 'bearer', 'user', None), by default 'bot'
        """
        if token_type == "bot":
            self.token = f"Bot {token}"
        elif token_type == "bearer":
            self.token = f"Bearer {token}"
        elif token_type == "user":
            warnings.warn(
                "Use a user token at your own risk as (depending on your usage) it could be against Discord's ToS. If you are using this token for a bot, you should use the 'bot' token_type instead.",
                UserWarning,
            )
            self.token = token
        else:
            self.token = None

    def _get_bucket_handler(self, bucket: str):
        bucket_handler = self.rate_limits.buckets.get(bucket)
        if bucket_handler is None:
            bucket_handler = self.rate_limits.buckets[bucket] = BucketHandler(
                bucket=bucket
            )
        return bucket_handler

    async def _request(
        self,
        method: str,
        path: str,
        bucket: str,
        headers: dict = {},
        json: dict | None = None,
        params: dict | None = None,
        auth: bool = True,
    ) -> ClientResponse:  # type: ignore
        if auth:
            if self.token_type is None:
                raise InvalidParams(
                    "No token has been set. Please set the auth parameter to False or set a token with set_new_token()."
                )
            headers["Authorization"] = self.token
        cs = ClientSession()

        url = self._base_url + path

        request_manager = cs.request(
            method, url, json=json, params=params, headers=headers
        )

        bucket_handler = self._get_bucket_handler(bucket)
        bucket_handler.prevent_429 = self._prevent_rate_limits
        async with self.rate_limits.global_limiter:
            async with bucket_handler as bh:
                async with cs:
                    r = await request_manager
                    bh.check_limit_headers(
                        r
                    )  # sets up the bucket rate limit attributes w/ response headers
                try:
                    if await self._check_response(response=r, bucket=bucket):
                        return r
                except TooManyRequests as e:
                    if self._retry_rate_limits is True:
                        response_data = await r.json()
                        timeout = response_data["retry_after"] + 1
                        await asyncio.sleep(timeout)
                        # reschedule same request
                        return await self._request(
                            method,
                            path,
                            bucket,
                            headers=headers,
                            json=json,
                            params=params,
                            auth=auth,
                        )
                    else:
                        raise e
                except NotFound as e:
                    raise e
                except UnknownError as e:
                    raise e

    async def _check_response(self, response: ClientResponse, bucket: str):
        """Checks API response for errors. Returns True only on 300 > status >= 200"""
        status = response.status
        reason = response.reason

        if 300 > status >= 200:
            return True
        elif status == 429:
            data = await response.json()
            message = data["message"]
            if "global" in data:
                text = f"Global rate limit. {data['message']}"
            else:
                text = f"{message}"

            retry_after = float(data.get("retry_after"))
            bucket_handler = self._get_bucket_handler(bucket)
            bucket_handler.retry_after = retry_after

            raise TooManyRequests(f"{text}, bucket: {bucket}")
        elif status == 400:
            raise BadRequest(
                f'Error Code: "{status}" Reason: "{reason}", bucket {bucket}'
            )
        elif status == 401:
            raise Unauthorized(
                f'Error Code: "{status}" Reason: "{reason}", bucket {bucket}'
            )
        elif status == 403:
            raise Forbidden(
                f'Error Code: "{status}" Reason: "{reason}", bucket {bucket}'
            )
        elif status == 404:
            raise NotFound(
                f'Error Code: "{status}" Reason: "{reason}", bucket {bucket}'
            )
        elif status == 500:
            raise InternalServerError(
                f'Error Code: "{status}" Reason: "{reason}", bucket {bucket}'
            )
        else:
            error_text = f'Error code: "{status}" Reason: "{reason}"'
            if status in api_errors:
                raise api_errors[status](error_text)
            else:
                raise UnknownError(error_text)
