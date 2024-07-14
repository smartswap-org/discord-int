import discord
import subprocess
from src.discordlogs import error 
from src.embeds.embeds import send_embed
from discord import Activity, ActivityType

async def restart(client, message, args):
    """
    Discord command to restart the host or the bot.
    NB: - the bot restart only work if u use start_bot.sh to start the bot (because it use a while)
        - the host restart command may not working depending ur OS  
    """
    if len(args) == 1:
        if args[0] == "host":
            await client.change_presence(activity=Activity(type=ActivityType.custom, name=" ", details=" ", state="⚠️ Host is restarting"))
            await send_embed(
                message.channel,
                "🖥️ Host",
                "Host will restart",
                discord.Color.red()
            )
            subprocess.run(["sudo", "reboot"]) # Send command to reboot the host (only works on Linux)
        elif args[0] == "bot":
            await client.change_presence(activity=Activity(type=ActivityType.custom, name=" ", details=" ", state="⚠️ Bot is restarting"))
            await send_embed(
                message.channel,
                "🤖 Bot",
                "Bot will restart",
                discord.Color.red()
            )
            exit() # Exit the bot, but the script.sh of the bot will restart the bot.
        else:
            await error(message.channel, "Invalid argument. Use `restart <bot/host>`")
    else:
       await error(message.channel, "Invalid argument(s) number. Use `restart <bot/host>`")
