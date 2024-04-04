from aiohttp import ClientResponse
from typing import List, Any

import discord_limits
from discord_limits.errors import *


class WebhookPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.

    Raises
    ------
    TypeError
        'client' must be of type `discord_limits.DiscordClient`.
    """

    def __init__(self, client: discord_limits.DiscordClient):
        self._client = client

    async def create_webhook(
        self, channel_id: int, name: str, reason: str | None = None
    ) -> ClientResponse:
        """Create a webhook.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to create the webhook in.
        name : str
            Name of the webhook (1-80 characters).
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A webhook object.
        """
        path = f"/channels/{channel_id}/webhooks"
        bucket = "POST" + path
        payload = {
            "name": name,
        }

        return await self._client._request(
            "POST", path, bucket, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_channel_webhooks(self, channel_id: int) -> ClientResponse:
        """Get a list of webhooks for a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get the webhooks for.

        Returns
        -------
        ClientResponse
            A list of webhook objects.
        """
        path = f"/channels/{channel_id}/webhooks"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_guild_webhooks(self, guild_id: int) -> ClientResponse:
        """Get a list of webhooks for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the webhooks for.

        Returns
        -------
        ClientResponse
            A list of webhook objects.
        """
        path = f"/guilds/{guild_id}/webhooks"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_webhook(self, webhook_id: int) -> ClientResponse:
        """Get a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to get.

        Returns
        -------
        ClientResponse
            A webhook object.
        """
        path = f"/webhooks/{webhook_id}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_webhook_with_token(
        self, webhook_id: int, webhook_token: str
    ) -> ClientResponse:
        """Get a webhook with a token.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to get.
        webhook_token : str
            The token of the webhook to get.

        Returns
        -------
        ClientResponse
            A webhook object.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket, auth=False)

    async def edit_webhook(
        self,
        webhook_id: int,
        name: str | None = None,
        channel_id: int | None = None,
        reason: str | None = None,
    ) -> ClientResponse:
        """Edit a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to edit.
        name : str, optional
            The default name of the webhook, by default None
        channel_id : int, optional
            The new channel id this webhook should be moved to, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A webhook object.
        """
        path = f"/webhooks/{webhook_id}"
        bucket = "PATCH" + path
        payload = {}
        if name is not None:
            payload["name"] = name
        if channel_id is not None:
            payload["channel_id"] = channel_id

        return await self._client._request(
            "PATCH", path, bucket, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def edit_webhook_with_token(
        self, webhook_id: int, webhook_token: str, name: str | None = None, reason: str | None = None
    ) -> ClientResponse:
        """Edit a webhook with a token.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to edit.
        webhook_token : str
            The token of the webhook to edit.
        name : str, optional
            The default name of the webhook, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A webhook object.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}"
        bucket = "PATCH" + path
        payload = {}

        if name is not None:
            payload["name"] = name

        return await self._client._request(
            "PATCH",
            path,
            bucket,
            json=payload,
            auth=False,
            headers={"X-Audit-Log-Reason": reason},
        )

    async def delete_webhook(
        self, webhook_id: int, reason: str | None = None
    ) -> ClientResponse:
        """Delete a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{webhook_id}"
        bucket = "DELETE" + path
        return await self._client._request(
            "DELETE", path, bucket, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_webhook_with_token(
        self, webhook_id: int, webhook_token: str, reason: str | None = None
    ) -> ClientResponse:
        """Delete a webhook with a token.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to delete.
        webhook_token : str
            The token of the webhook to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}"
        bucket = "DELETE" + path
        return await self._client._request(
            "DELETE", path, bucket, auth=False, headers={"X-Audit-Log-Reason": reason}
        )

    async def execute_webhook(
        self,
        webhook_id: int,
        webhook_token: str,
        wait: bool = False,
        thread_id: int | None = None,
        content: str | None = None,
        username: str | None = None,
        avatar_url: str | None = None,
        tts: bool = False,
        embeds: List[dict] | None = None,
        allowed_mentions: Any = None,
        components: List[Any] | None = None,
    ) -> ClientResponse:
        """Execute a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to execute.
        webhook_token : str
            The token of the webhook to execute.
        wait : bool, optional
            Waits for server confirmation of message send before response, and returns the created message body, by default False
        thread_id : int, optional
            Send a message to the specified thread within a webhook's channel, by default None
        content : str, optional
            The message contents (up to 2000 characters), by default None
        username : str, optional
            Override the default username of the webhook, by default None
        avatar_url : str, optional
            Override the default avatar of the webhook, by default None
        tts : bool, optional
            True if this is a TTS message, by default False
        embeds : List[dict], optional
            Embedded rich content, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            The components to include with the message, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.

        Raises
        ------
        InvalidParams
            If content or embeds are provided.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}"
        bucket = "POST" + path
        if content is None and embeds is None:
            raise InvalidParams("content or embeds must be provided")

        params = {}
        if wait is not None:
            params["wait"] = wait
        if thread_id is not None:
            params["thread_id"] = thread_id

        payload = {}

        if content is not None:
            payload["content"] = content
        if username is not None:
            payload["username"] = username
        if avatar_url is not None:
            payload["avatar_url"] = avatar_url
        if tts is not None:
            payload["tts"] = tts
        if embeds is not None:
            payload["embeds"] = embeds
        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions
        if components is not None:
            payload["components"] = components

        return await self._client._request(
            "POST", path, bucket, json=payload, params=params, auth=False
        )

    async def get_webhook_message(
        self, webhook_id: int, webhook_token: str, message_id: int, thread_id: int | None = None
    ) -> ClientResponse:
        """Get a message from a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to get the message from.
        webhook_token : str
            The token of the webhook to get the message from.
        message_id : int
            The ID of the message to get.
        thread_id : id, optional
            The ID of the thread to get the message from, by default None

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket, auth=False)

    async def edit_webhook_message(
        self,
        webhook_id: int,
        webhook_token: str,
        message_id: int,
        thread_id: int | None = None,
        content: str | None = None,
        embeds: List[dict] | None = None,
        allowed_mentions: Any = None,
        components: List[Any] | None = None,
    ) -> ClientResponse:
        """Edit a message from a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to edit the message from.
        webhook_token : str
            The token of the webhook to edit the message from.
        message_id : int
            The ID of the message to edit.
        thread_id : int, optional
            ID of the thread the message is in, by default None
        content : str, optional
            The message contents (up to 2000 characters), by default None
        embeds : List[dict], optional
            Embedded rich content, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            The components to include with the message, by default None

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
        bucket = "PATCH" + path

        payload = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
        }
        return await self._client._request(
            "PATCH", path, bucket, json=payload, auth=False
        )

    async def delete_webhook_message(
        self, webhook_id: int, webhook_token: str, message_id: int
    ) -> ClientResponse:
        """Delete a message from a webhook.

        Parameters
        ----------
        webhook_id : int
            The ID of the webhook to delete the message from.
        webhook_token : str
            The token of the webhook to delete the message from.
        message_id : int
            The ID of the message to delete.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
        bucket = "DELETE" + path
        return await self._client._request("DELETE", path, bucket, auth=False)
