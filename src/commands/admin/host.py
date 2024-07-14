import discord
import platform
import psutil
import socket
import os 
from src.discordlogs import error 
from src.embeds.embeds import send_embed

async def host(client, message, args):
    """
    Discord command to informations about the host (the machine where is the bot)
    """
    try:
        # cpu infos
        cpu_info = f"**Processor:** {platform.processor()}\n"
        cpu_info += f"**Physical Cores:** {psutil.cpu_count(logical=False)}\n"
        cpu_info += f"**Total Cores:** {psutil.cpu_count(logical=True)}"

        # disk infos
        disk_info = psutil.disk_usage('/')
        disk_usage_info = f"**Disk Usage:** {disk_info.percent}% used\n"
        disk_usage_info += f"**Total Disk Space:** {round(disk_info.total / (1024 ** 3), 2)} GB\n"
        disk_usage_info += f"**Used Disk Space:** {round(disk_info.used / (1024 ** 3), 2)} GB\n"
        disk_usage_info += f"**Free Disk Space:** {round(disk_info.free / (1024 ** 3), 2)} GB"

        # internet infos
        try:
            host_name = socket.gethostname()
            internet_info = f"**Host Name:** {host_name}\n"
            internet_info += f"**IP Address:** {socket.gethostbyname(host_name)}"

        except socket.error:
            internet_info = "Unable to retrieve Internet information."

        # working directory of the bot (bot path)
        current_working_directory = f"**Current Working Directory:** {os.getcwd()}"

        # Description de l'embed
        embed_description = (
            f"**System:** {platform.system()}\n"
            f"**Node Name:** {platform.node()}\n"
            f"**Release:** {platform.release()}\n"
            f"**Version:** {platform.version()}\n"
            f"**Machine:** {platform.machine()}\n"
            f"{cpu_info}\n"
            f"**Memory Usage:** {psutil.virtual_memory().percent}% used\n"
            f"{disk_usage_info}\n"
            f"{internet_info}\n"
            f"{current_working_directory}"
        )

        await send_embed(
            message.channel,
            "🤖 Host Information",
            embed_description,
            discord.Color.blue()
        )

    except Exception as e:
        await error(message.channel, f"Error retrieving host information.\n {e}")
