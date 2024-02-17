import discord
import platform
import psutil
import socket
import os 
from discord_bot.discordlogs import error 
from discord_bot.embeds.embeds import send_embed

async def host(client, message, args):
    try:
        # Informations système
        system_info = platform.system()
        node_name = platform.node()
        release_info = platform.release()
        version_info = platform.version()
        machine_info = platform.machine()
        processor_info = platform.processor()

        # Informations CPU
        cpu_info = f"**Processor:** {processor_info}\n"
        cpu_info += f"**Physical Cores:** {psutil.cpu_count(logical=False)}\n"
        cpu_info += f"**Total Cores:** {psutil.cpu_count(logical=True)}"

        # Informations mémoire
        memory_info = psutil.virtual_memory()

        # Informations disque
        disk_info = psutil.disk_usage('/')
        disk_usage_info = f"**Disk Usage:** {disk_info.percent}% used\n"
        disk_usage_info += f"**Total Disk Space:** {round(disk_info.total / (1024 ** 3), 2)} GB\n"
        disk_usage_info += f"**Used Disk Space:** {round(disk_info.used / (1024 ** 3), 2)} GB\n"
        disk_usage_info += f"**Free Disk Space:** {round(disk_info.free / (1024 ** 3), 2)} GB"

        # Informations sur la connexion Internet
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            internet_info = f"**Host Name:** {host_name}\n"
            internet_info += f"**IP Address:** {host_ip}"
        except socket.error:
            internet_info = "Unable to retrieve Internet information."

        # Répertoire de travail du bot
        current_working_directory = f"**Current Working Directory:** {os.getcwd()}"

        # Description de l'embed
        embed_description = (
            f"**System:** {system_info}\n"
            f"**Node Name:** {node_name}\n"
            f"**Release:** {release_info}\n"
            f"**Version:** {version_info}\n"
            f"**Machine:** {machine_info}\n"
            f"{cpu_info}\n"
            f"**Memory Usage:** {memory_info.percent}% used\n"
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
