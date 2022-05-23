from discord_limits.errors import *
import discord_limits

class ApplicationCommandPaths:

    def __init__(self, client: discord_limits.DiscordClient):
        if not isinstance(client, discord_limits.DiscordClient):
            raise TypeError('"client" must be an instance of discord_limits.DiscordClient')
        self._client = client

    # Application commands (global)

    async def get_global_application_commands(self, application_id: int) -> dict:
        """Fetch all of the global commands for an application.

        Parameters
        ----------
        application_id : int
            The application ID.

        Returns
        -------
        dict
            A list of application command objects.
        """        
        path = f'/applications/{application_id}/commands'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def create_global_application_command(self, application_id: int, payload: dict) -> dict:
        """Create a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        payload : dict
            The params to create the command with.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/commands'
        bucket = 'POST' + path
        return await self._client._request('POST', path, bucket, json=payload)

    async def get_global_application_command(self, application_id: int, command_id: int) -> dict:
        """Get a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def edit_global_application_command(self, application_id: int, command_id: int, payload: dict) -> dict:
        """Edit a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command with.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'description',
            'options',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request('PATCH', path, bucket, json=payload)

    async def delete_global_application_command(self, application_id: int, command_id: int) -> dict:
        """Delete a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.

        Returns
        -------
        dict
            The response from Discord.
        """        
        path = f'/applications/{application_id}/commands/{command_id}'
        bucket = 'DELETE' + path
        return await self._client._request('DELETE', path, bucket)

    async def bulk_overwrite_global_application_commands(self, application_id: int, payload: dict) -> dict:
        """Bulk edit global commands.

        Parameters
        ----------
        application_id : int
            The application ID.
        payload : dict
            The params to edit the commands with.

        Returns
        -------
        dict
            A list of application command objects.
        """        
        path = f'/applications/{application_id}/commands'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    # Application commands (guild)

    async def get_guild_application_commands(self, application_id: int, guild_id: int, with_localisations : bool = False) -> dict:
        """Fetch all of the guild commands for an application.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        with_localisations : bool, optional
            Whether to include full localisations dictionaries, by default False

        Returns
        -------
        dict
            A list of application command objects.
        """              
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def create_guild_application_command(self, application_id: int, guild_id: int, payload: dict) -> dict:
        """Create a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        payload : dict
            The params to create the command with.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'POST' + path
        return await self._client._request('POST', path, bucket, json=payload)

    async def get_guild_application_command(self, application_id: int, guild_id: int, command_id: int) -> dict:
        """Get a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def edit_guild_application_command(self, application_id: int, guild_id: int, command_id: int, payload: dict) -> dict:
        """Edit a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command with.

        Returns
        -------
        dict
            An application command object.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'description',
            'options',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request('PATCH', path, bucket, json=payload)

    async def delete_guild_application_command(self, application_id: int, guild_id: int, command_id: int) -> dict:
        """Delete a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.

        Returns
        -------
        dict
            The response from Discord.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}'
        bucket = 'DELETE' + path
        return await self._client._request('DELETE', path, bucket)

    async def bulk_overwrite_guild_application_commands(self, application_id: int, guild_id: int, payload: dict) -> dict:
        """Bulk overwrite guild commands.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        payload : dict
            The params to overwrite the commands with.

        Returns
        -------
        dict
            A list of application command objects.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)

    async def get_guild_application_command_permissions(self, application_id: int, guild_id: int) -> dict:
        """Fetch all of the guild application command permissions for an application.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.

        Returns
        -------
        dict
            A list of guild application command permissions objects.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/permissions'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def get_application_command_permissions(self, application_id: int, guild_id: int, command_id: int) -> dict:
        """Get permissions for a specific command for your application in a guild.

        Parameters
        ----------
        application_id : int
            _description_
        guild_id : int
            _description_
        command_id : int
            _description_

        Returns
        -------
        dict
            A guild application command permissions object.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions'
        bucket = 'GET' + path
        return await self._client._request('GET', path, bucket)

    async def edit_application_command_permissions(self, application_id: int, guild_id: int, command_id: int, payload: dict) -> dict:
        """Edit a guild application command permissions.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command permissions with.

        Returns
        -------
        dict
            A guild application command permissions object.
        """        
        path = f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions'
        bucket = 'PUT' + path
        return await self._client._request('PUT', path, bucket, json=payload)