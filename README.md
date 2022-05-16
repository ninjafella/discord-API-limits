# discord_limits

### This is a small library that allows you to easily make requests API requests to Discord without having to worry about ratelimits.

<br>

### Currently this library has only been tested on 3.9

---

# Basic usage

```py
import discord_limits
import os

client = discord_limits.DiscordClient(os.environ.get('TOKEN'))

channel_id = 123456789012345678
client.send_message(channel_id, content="Hello, world!")
```

---
### Based off of:
- [unbelipy](https://github.com/chrisdewa/unbelipy)
- [discord.py](https://github.com/Rapptz/discord.py)