import discord 
from discord_bot.embeds.embeds import send_embed

async def error(message, error):
    if not message: return 
    await send_embed(message, "❌ Error", error, discord.Color.brand_red())
