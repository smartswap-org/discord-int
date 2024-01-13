from .embeds import *
from .config import *


async def discord_log(client, title, log, color=discord.Color.dark_blue()):
    bot_config = get_bot_config()
    guild = client.get_guild(int(bot_config["discordid"]))
    if not "logschannelid" in bot_config.keys(): return 
    channel = guild.get_channel(int(bot_config["logschannelid"]))
    await send_embed(channel, title, log, color)

async def error(message, error):
    if not message: return 
    await send_embed(message, "❌ Error", error, discord.Color.red())
