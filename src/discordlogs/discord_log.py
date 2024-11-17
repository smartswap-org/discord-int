import discord 
from src.config import get_bot_config
from src.embeds.embeds import send_embed

async def discord_log(client, title, log):
    """
    Function used to log in the log channel configured in configs/bot_config.json | logschannelid
    """

    bot_config = get_bot_config()
    guild = client.get_guild(int(bot_config["discordid"]))

    # The logschannelid is not configured in the bot_config.json yet
    if "logschannelid" not in bot_config.keys(): return 
    
    # Get the channel object using the discord channel id     
    channel = guild.get_channel(int(bot_config["logschannelid"]))

    # Set the color of the embed with the color of the HIGHTEST role that the BOT has on him
    highest_role = max(
        guild.get_member(client.user.id).roles, 
        key=lambda r: r.position) # Position highter
    
    # Set the color by default has green if we didnt found the hightest color
    color = highest_role.color if highest_role else discord.Color.green() 

    # Send the embed (the log on the discord)
    await send_embed(channel, title, log, color)
