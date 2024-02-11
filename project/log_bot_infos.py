from .config import *
import requests
import subprocess
import socket
import psutil
import platform
from .logs import *
from datetime import datetime
import time

import re

def escape_special_chars(string):
    # Escape underscores, asterisks, and double underscores
    string = re.sub(r'[_*]', r'\\\g<0>', string)
    return string

async def log_bot_info(client):
    try:
        bot_config = get_bot_config()
        guild = client.get_guild(int(bot_config["discordid"]))
        if "logschannelid" not in bot_config:
            return

        channel = guild.get_channel(int(bot_config["logschannelid"]))

        # Host information
        external_ip = get_external_ip()
        local_ip = socket.gethostbyname(socket.gethostname())
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        uptime_str = format_time(uptime_seconds)

        # Get Git information
        git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        git_branch = escape_special_chars(git_branch)
        last_commits = subprocess.check_output(['git', 'log', '-10', '--pretty=format:%H %an %s']).decode().strip().split('\n')

        # Get the repository URL
        repository_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode().strip().replace('.git', '')

        embed_description = (
            f"**🖥️ Host**\n"
            f"**External IP Address:** {external_ip}\n"
            f"**Local IP Address:** {local_ip}\n"
            f"**System Uptime:** {uptime_str}\n"
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
            commit_url = f"{repository_url}/commit/{commit_hash}"
            commit_author = escape_special_chars(commit_author)
            embed_description += f"**{commit_author}** : {commit_message} [🔗]({commit_url})\n"

        await discord_log(client, "🤖 Bot started", embed_description)

    except Exception as e:
        await error(channel, f"Error starting bot with information.\n {e}")

def get_external_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Error fetching external IP"
