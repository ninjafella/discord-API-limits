[![Documentation Status](https://readthedocs.org/projects/discord-limits/badge/?version=latest)](https://discord-limits.readthedocs.io/en/latest/?badge=latest)
[![Version](https://img.shields.io/badge/Version-v1.1.2-blue)](https://img.shields.io/badge/Version-v1.1.2-blue)

# discord_limits

### A simple library to asynchronously make API requests to Discord without having to worry about ratelimits.

<br>

### Currently this library has only been tested on Python 3.9

---

# Basic usage

```py
import discord_limits
import os
import asyncio

limitsClient = discord_limits.DiscordClient(os.environ.get('TOKEN'))

async def main():
    await limitsClient.create_message(123456789012345678, content='Hello World!')


asyncio.get_event_loop().run_until_complete(main())
```

---
### Requires:
- [aiolimiter](https://pypi.org/project/aiolimiter/)
- [aiohttp](https://pypi.org/project/aiohttp/)

---
### Based off of:
- [unbelipy](https://github.com/chrisdewa/unbelipy)
- [discord.py](https://github.com/Rapptz/discord.py)
