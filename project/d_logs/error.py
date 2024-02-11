from ..embeds.embeds import *
from ..config import *

async def error(message, error):
    if not message: return 
    await send_embed(message, "❌ Error", error, discord.Color.brand_red())
