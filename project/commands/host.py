import discord
import platform
import psutil
from ..misc.logs import *

async def host(client, message, args):
    try:
        system_info = platform.system()
        node_name = platform.node()
        release_info = platform.release()
        version_info = platform.version()
        machine_info = platform.machine()
        processor_info = platform.processor()
        cpu_info = platform.processor()

        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        embed_description = (
            f"**System:** {system_info}\n"
            f"**Node Name:** {node_name}\n"
            f"**Release:** {release_info}\n"
            f"**Version:** {version_info}\n"
            f"**Machine:** {machine_info}\n"
            f"**Processor:** {processor_info}\n"
            f"**CPU:** {cpu_info}\n"
            f"**Memory Usage:** {memory_info.percent}% used\n"
            f"**Disk Usage:** {disk_info.percent}% used"
        )

        await send_embed(
            message.channel,
            "🤖 Host Information",
            embed_description,
            discord.Color.blue()
        )

    except Exception as e:
        await error(message.channel, f"Error retrieving host information. {e}")
