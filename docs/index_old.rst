discord_limits
==============

.. _a-simple-library-to-asynchronously-make-api-requests-to-discord-without-having-to-worry-about-ratelimits:

A simple library to asynchronously make API requests to Discord without having to worry about ratelimits.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <br>

.. _currently-this-library-has-only-been-tested-on-39:

Currently this library has only been tested on 3.9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--------------

Basic usage
===========

.. code:: py

   import discord_limits
   import os

   client = discord_limits.DiscordClient(os.environ.get('TOKEN'))

   channel_id = 123456789012345678
   await client.send_message(channel_id, content="Hello, world!")

--------------

Requires:
~~~~~~~~~

-  `aiolimiter <https://pypi.org/project/aiolimiter/>`__
-  `aiohttp <https://pypi.org/project/aiohttp/>`__

--------------

Based off of:
~~~~~~~~~~~~~

-  `unbelipy <https://github.com/chrisdewa/unbelipy>`__
-  `discord.py <https://github.com/Rapptz/discord.py>`__
