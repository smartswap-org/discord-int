from datetime import datetime
import discord
import time

bot_start_time = time.time()

def create_embed(title, description, color):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed

async def send_embed(channel, title, description, color):
    embed = create_embed(title, description, color)
    uptime_seconds = int(time.time() - bot_start_time)
    uptime_str = format_time(uptime_seconds)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    embed.set_footer(text=f"Bot uptime: {uptime_str}, date: {date}")
    await channel.send(embed=embed)

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

