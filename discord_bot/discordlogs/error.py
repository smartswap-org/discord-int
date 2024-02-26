import discord 
from discord_bot.embeds.embeds import send_embed
from .discord_log import discord_log

async def error(message, error):
    """
    Sends an error embed in the channel.
    """
    # Check if message is None to avoid errors when called internally
    if not message:
        return

    # Send the error embed
    await send_embed(message, "❌ Error", error, discord.Color.brand_red())
