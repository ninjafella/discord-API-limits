from typing import TYPE_CHECKING

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class StickerPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: 'DiscordClient'):
        self._client = client

    async def get_sticker(self, sticker_id: int) -> ClientResponse:
        """Get a sticker.

        Parameters
        ----------
        sticker_id : int
            The ID of the sticker to get.

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/stickers/{sticker_id}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def list_nitro_sticker_packs(self) -> ClientResponse:
        """List all nitro sticker packs.

        Returns
        -------
        ClientResponse
            A list of sticker pack objects.
        """
        path = "/sticker-packs"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def list_guild_stickers(self, guild_id: int) -> ClientResponse:
        """List all stickers in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to list stickers for.

        Returns
        -------
        ClientResponse
            A list of sticker objects.
        """
        path = f"/guilds/{guild_id}/stickers"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    async def get_guild_sticker(self, guild_id: int, sticker_id: int) -> ClientResponse:
        """Get a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the sticker for.
        sticker_id : int
            The ID of the sticker to get.

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        bucket = "GET" + path
        return await self._client._request("GET", path, bucket)

    """
    async def create_guild_sticker(self, guild_id: int, payload, file, reason) -> ClientResponse:
        initial_bytes = file.fp.read(16)

        try:
            mime_type = _get_mime_type_for_image(initial_bytes)
        except ValueError:
            if initial_bytes.startswith(b'{') -> ClientResponse:
                mime_type = 'application/json'
            else:
                mime_type = 'application/octet-stream'
        finally:
            file.reset()

        form = [
            {
                'name': 'file',
                'value': file.fp,
                'filename': file.filename,
                'content_type': mime_type,
            }
        ]

        for k, v in payload.items() -> ClientResponse:
            form.append(
                {
                    'name': k,
                    'value': v,
                }
            )

        return await self._client._request(
            Route('POST', '/guilds/{guild_id}/stickers', guild_id=guild_id: int), form=form, files=[file], reason=reason
        )
    """

    async def modify_guild_sticker(
        self,
        guild_id: int,
        sticker_id: int,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: str | None = None,
        reason: str | None = None,
    ) -> ClientResponse:
        """Modify a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to modify the sticker for.
        sticker_id : int
            The ID of the sticker to modify.
        name : str, optional
            Name of the sticker (2-30 characters), by default None
        description : str, optional
            Description of the sticker (2-100 characters), by default None
        tags : str, optional
            Autocomplete/suggestion tags for the sticker (max 200 characters), by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        bucket = "PATCH" + path
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags

        return await self._client._request(
            "PATCH", path, bucket, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_guild_sticker(
        self, guild_id: int, sticker_id: int, reason: str | None = None
    ) -> ClientResponse:
        """Delete a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete the sticker for.
        sticker_id : int
            The ID of the sticker to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        bucket = "DELETE" + path
        return await self._client._request(
            "DELETE", path, bucket, headers={"X-Audit-Log-Reason": reason}
        )
