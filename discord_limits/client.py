import asyncio
import warnings
from sys import version_info as python_version

from aiohttp import ClientResponse, ClientSession
from aiohttp import __version__ as aiohttp_version

from . import __version__
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

        self.user_agent: str = (
            f"DiscordBot (https://github.com/ninjafella/discord-API-limits {__version__}) Python/{python_version[0]}.{python_version[1]}.{python_version[2]} aiohttp/{aiohttp_version}"
        )

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
