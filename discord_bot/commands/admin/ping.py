import discord 
import subprocess
from discord_bot.discordlogs import error 
from discord_bot.embeds.embeds import send_embed
from discord_bot.config import get_bot_config

async def ping(client, message, args):
    """
    Discord command to get the ping of the host with google (see latence)
    """

    # This part of the code is now in comment because whatever the arguments of the command, 
    # they are useless so we can execute the command
    #if len(args) != 0:
        #return await error(
            #message.channel,
            #"Invalid argument(s). Use:\n"
            #"ping")
    
    try:
        result = subprocess.run(['ping', '-c', '4', 'google.com'], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return await error(
            message.channel,
            "Ping command timed out. Try again later.")

    if result.returncode == 0:
        ping_output = result.stdout.split('\n')
        ping_stats = ping_output[-2]
        return await send_embed(
            message.channel,
            "📡 Ping to Google",
            f"```{ping_stats}```",
            discord.Color.green()
        )
    else:
        return await error(
            message.channel,
            "Error executing ping command. Please try again."
        )
