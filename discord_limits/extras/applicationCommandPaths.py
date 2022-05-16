from discord_limits.errors import *
import discord_limits

class ApplicationCommandPaths:

    def __init__(self, client: discord_limits.DiscordClient):
        if not isinstance(client, discord_limits.DiscordClient):
            raise TypeError('client must be an instance of discord_limits.DiscordClient')
        self._client = client

    # Application commands (global)

    async def get_global_commands(self, application_id: int):
        path = f'/applications/{application_id}/commands'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def get_global_command(self, application_id: int, command_id: int):
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def upsert_global_command(self, application_id: int, payload: dict):
        path = f'/applications/{application_id}/commands'
        bucket = 'POST' + path
        return await self._client._request('POST', path, bucket, json=payload)

    async def edit_global_command(self, application_id: int, command_id: int, payload: dict):
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'description',
            'options',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request('PATCH', path, bucket, json=payload)

    async def delete_global_command(self, application_id: int, command_id: int):
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'DELETE' + path
        return await self._client._request('DELETE', path, bucket)

    async def bulk_upsert_global_commands(self, application_id: int, payload: dict):
        path = f'/applications/{application_id}/commands'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    # Application commands (guild)

    async def get_guild_commands(self, application_id: int, guild_id: int):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def get_guild_command(self, application_id: int, guild_id: int, command_id: int):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def upsert_guild_command(self, application_id: int, guild_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'POST' + path
        return await self._client._request('POST', path, bucket, json=payload)

    async def edit_guild_command(self, application_id: int, guild_id: int, command_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'description',
            'options',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request('PATCH', path, bucket, json=payload)

    async def delete_guild_command(self, application_id: int, guild_id: int, command_id: int):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'DELETE' + path
        return await self._client._request('DELETE', path, bucket)

    async def bulk_upsert_guild_commands(self, application_id: int, guild_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    async def get_guild_application_command_permissions(self, application_id: int, guild_id: int):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/permissions'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def edit_application_command_permissions(self, application_id: int, guild_id: int, command_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    async def bulk_edit_guild_application_command_permissions(self, application_id: int, guild_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/permissions'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    async def bulk_edit_guild_application_command_permissions(self, application_id: int, guild_id: int, payload: dict):
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/permissions'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)