from ...config import *
from ...logs.error import *
import subprocess

async def ping(client, message, args):
    if len(args) != 0:
        return await error(
            message.channel,
            "Invalid argument(s). Use:\n"
            "ping")
    
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
