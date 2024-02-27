from datetime import datetime
import discord 
import time

# Keep the time of when the bot has been started
bot_start_time = time.time()

def create_embed(title, description, color):
    """
    This function create an embed with 
    title, description, color 
    for discord
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed

async def send_embed(channel, title, description, color):
    """
    This function create using the function create_embed
    then get the timer since when the bot is started using the global variable bot_start_time
    and set this Botuptime in footer.
    """
    # Create embed
    embed = create_embed(title, description, color)

    # Get Bot Uptime
    uptime_seconds = int(time.time() - bot_start_time)
    uptime_str = format_time(uptime_seconds)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Set footer
    embed.set_footer(text=f"Bot uptime: {uptime_str}, date: {date}")

    # Send embed
    await channel.send(embed=embed)

def format_time(seconds):
    """
    this function converts a given duration in seconds 
    into a formatted string representing hours, minutes, and seconds. 

    ex: format_time(3665) will return "1h 1m 5s"
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

