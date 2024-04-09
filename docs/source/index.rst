Welcome to discord_limits' documentation!
=========================================

.. toctree::
   :caption: Contents:

   client


Basic usage
===========

.. code:: py

   import discord_limits
   import os
   import asyncio

   limitsClient = discord_limits.DiscordClient(os.environ.get('TOKEN'))

   async def main():
      await limitsClient.create_message(123456789012345678, content='Hello World!')


   asyncio.get_event_loop().run_until_complete(main())


Requires:
=========

*  `aiolimiter <https://pypi.org/project/aiolimiter/>`__
*  `aiohttp <https://pypi.org/project/aiohttp/>`__


Based off of:
=============

*  `unbelipy <https://github.com/chrisdewa/unbelipy>`__
*  `discord.py <https://github.com/Rapptz/discord.py>`__