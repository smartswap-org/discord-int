from ..embeds.embeds import *
from ..config import *

async def discord_log(client, title, log):
    bot_config = get_bot_config()
    guild = client.get_guild(int(bot_config["discordid"]))
    if "logschannelid" not in bot_config.keys(): return
         
    channel = guild.get_channel(int(bot_config["logschannelid"]))
    highest_role = max(guild.get_member(client.user.id).roles, key=lambda r: r.position)
    color = highest_role.color if highest_role else discord.Color.green()

    await send_embed(channel, title, log, color)
