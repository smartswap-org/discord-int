import discord
from ...logs.error import *

async def clear(client, message, args):
    try:
        await message.channel.purge(limit=None) # Delete all the messages of the channel
        await send_embed(
            message.channel,
            "✅ Success",
            "All messages have been deleted.",
            discord.Color.green()
        )
    except Exception as e:
        print(f"Error during message deletion: {e}")
        await error(message.channel, f"Error during message deletion.\n {e}")
