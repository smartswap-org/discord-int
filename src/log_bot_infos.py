import datetime
import requests
import subprocess
import socket
import psutil
import platform
import re
from src.config import get_bot_config
from src.discordlogs import discord_log, error

def escape_special_chars(string):
    """
    Escapes special characters in a string by prefixing them with a backslash.

    # From somewhere on the web

    Exemple:
    string:          This_is_an_example_with*special_chars_and__double_underscores
    returned string: This\_is\_an\_example\_with\*special\_chars\_and\_\_double\_underscores
    """

    string = re.sub(r'([\\*_])', r'\\\1', string)
    return string

async def log_bot_infos(client):
    try:
        bot_config = get_bot_config()                          # Get bot config
        guild = client.get_guild(int(bot_config["discordid"])) # Get object of the current Discord configured
        if "logschannelid" not in bot_config: return           # Dont sent a message in the log channel if not configured
            
        channel = guild.get_channel(
            int(bot_config["logschannelid"])
            )

        external_ip = get_external_ip() # Get my public ip address 

        # Get my local ip address: 192.168.1.X
        local_ip = socket.gethostbyname(
            socket.gethostname()
            ) 

        # Get the current branch that we work on 
        git_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
            ).decode().strip() 
        git_branch = escape_special_chars(git_branch) 
        
        # Get the 10 last commits of made on the branch
        # and split them line by line using \n
        last_commits = subprocess.check_output(
            ['git', 'log', '-10', '--pretty=format:%H %an %s']
            ).decode().strip().split('\n') 

        # Get repository url
        repository_url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url']
            ).decode().strip().replace('.git', '') 

        # Uptime of the machine
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

        embed_description = (
            f"\n"
            f"**🖥️ Host**\n"
            f"**External IP Address:** {external_ip}\n"
            f"**Local IP Address:** {local_ip}\n"
            f"**System Uptime:** {uptime}\n"
            f"**System Type:** {platform.system()}\n"
            f"\n"
            f"**🤖 Git**\n"
            f"**Git Branch:** {git_branch}\n"
            f"**Last 10 Commits:**\n"
        )

        for commit in last_commits:
            commit_parts = commit.split(' ', 2)
            commit_hash = commit_parts[0]
            commit_author = commit_parts[1]
            commit_message = commit_parts[2]
            commit_url = f"[{commit_message}]({repository_url}/commit/{commit_hash})"
            commit_message = escape_special_chars(commit_message)
            embed_description += f"**{commit_author}**  :  {commit_url}\n"

        await discord_log(client, "🤖 Bot started", embed_description)

    except Exception as e:
        await error(channel, f"Error starting bot with information.\n {e}")

def get_external_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Error fetching external IP"