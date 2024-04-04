from typing import Any

from aiohttp import ClientResponse

import discord_limits
from discord_limits.errors import *


class AutoModerationPaths:
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

    async def list_auto_moderation_rules(self, guild_id: int) -> ClientResponse:
        """Get a list of all rules currently configured for guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get rules from.

        Returns
        -------
        ClientResponse
            List of auto moderation rule objects.
        """
        path = f"/guilds/{guild_id}/auto-moderation/rules"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_auto_moderation_rule(
        self, guild_id: int, rule_id: int
    ) -> ClientResponse:
        """Get a single rule.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get rule from.
        rule_id : int
            The ID of the rule that is to be retrieved.

        Returns
        -------
        ClientResponse
            A auto moderation rule object.
        """
        path = f"/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def create_auto_moderation_rule(
        self, guild_id: int, **options: Any
    ) -> ClientResponse:
        """Create a new rule.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create a rule in.

        Returns
        -------
        ClientResponse
            A auto moderation rule object.
        """
        path = f"/guilds/{guild_id}/auto-moderation/rules"
        bucket = "POST" + path
        valid_keys = (
            "name",
            "event_type",
            "trigger_type",
            "trigger_metadata",
            "actions",
            "enabled",
            "exempt_roles",
            "exempt_channels",
        )
        payload = {k: v for k, v in options.items() if k in valid_keys}
        return await self._client._request("POST", path, bucket, json=payload)

    async def modify_auto_moderation_rule(
        self, guild_id: int, rule_id: int, **options: Any
    ) -> ClientResponse:
        """Modify an existing rule.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to modify a rule in.
        rule_id : int
            The ID of the rule that is to be modified.

        Returns
        -------
        ClientResponse
            A auto moderation rule object.
        """
        path = f"/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        bucket = "PATCH" + path
        valid_keys = (
            "name",
            "event_type",
            "trigger_metadata",
            "actions",
            "enabled",
            "exempt_roles",
            "exempt_channels",
        )
        payload = {k: v for k, v in options.items() if k in valid_keys}
        return await self._client._request("PATCH", path, bucket, json=payload)

    async def delete_auto_moderation_rule(
        self, guild_id: int, rule_id: int
    ) -> ClientResponse:
        """Delete a rule.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete a rule from.
        rule_id : int
            The ID of the rule that is to be deleted.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/auto-moderation/rules/{rule_id}"
        bucket = "DELETE" + path
        return await self._client._request("DELETE", path, bucket)
