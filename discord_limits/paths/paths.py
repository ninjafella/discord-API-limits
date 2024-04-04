from aiohttp import ClientResponse
from discord_limits.errors import *

from .applicationPaths import ApplicationPaths
from .auditPaths import AuditPaths
from .autoModerationPaths import AutoModerationPaths
from .channelPaths import ChannelPaths
from .emojiPaths import EmojiPaths
from .guildPaths import GuildPaths
from .interationsPaths import InteractionsPaths
from .invitePaths import InvitePaths
from .stagePaths import StagePaths
from .stickerPaths import StickerPaths
from .userPaths import UserPaths
from .webhookPaths import WebhookPaths


class Paths:

    def __init__(self, client):
        self._client = client
        self.application = ApplicationPaths(self._client)
        self.audit_logs = AuditPaths(self._client)
        self.auto_moderation = AutoModerationPaths(self._client)
        self.channel = ChannelPaths(self._client)
        self.emoji = EmojiPaths(self._client)
        self.guild = GuildPaths(self._client)
        self.interactions = InteractionsPaths(self._client)
        self.invite = InvitePaths(self._client)
        self.stage = StagePaths(self._client)
        self.sticker = StickerPaths(self._client)
        self.user = UserPaths(self._client)
        self.webhook = WebhookPaths(self._client)

    async def list_voice_regions(self) -> ClientResponse:
        """Get a list of voice regions.

        Returns
        -------
        ClientResponse
            A list of voice region objects.
        """
        path = "/voice/regions"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_gateway(self) -> ClientResponse:
        """Get the gateway URL.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/gateway"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket, auth=False)

    async def get_bot_gateway(self) -> ClientResponse:
        """Get the gateway URL for a bot.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/gateway/bot"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def application_info(self) -> ClientResponse:
        """Get the application info.

        Returns
        -------
        ClientResponse
            An application object.
        """
        path = "/oauth2/applications/@me"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def authorisation_info(self, bearer_token: str) -> ClientResponse:
        """Get the authorisation info.

        Parameters
        ----------
        bearer_token : str
            The bearer token to get the authorisation info for.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/oauth2/@me"
        bucket = "GET" + path
        return await self._client._request(
            "GET",
            path,
            bucket,
            headers={"Authorization": f"Bearer {bearer_token}"},
            auth=False,
        )  # auth is False as a bearer_token is used
