import discord
from ...misc.logs import *
from discord import Activity, ActivityType
import subprocess

async def update(client, message, args):
    config = get_json_content("update_config.json")
    if config == -1:
        write_json("update_config.json", {"projectname":"c://dir"})
        await error(message.channel, "update_config.json has been created.")
        return 
    if len(args) != 1: return await error(message.channel, "Invalid argument. Use `update <project>`")
    if args[0] in config:
        try:
            project_path = config[args[0]]

            # Git pull the main project
            pull_result = subprocess.run(['git', '-C', project_path, 'pull'], capture_output=True, text=True)

            await send_embed(
                message.channel,
                "🖥️ git pull",
                pull_result,
                discord.Color.pink()
            )

            # Git submodule update --remote
            submodule_result = subprocess.run(['git', '-C', project_path, 'submodule', 'update', '--remote'], capture_output=True, text=True)

            await send_embed(
                message.channel,
                "🖥️ git submodule update",
                submodule_result,
                discord.Color.pink()
                )


        except Exception as e:
            await error(message.channel, f"An unexpected error occurred: {e}")

    else:
         return await error(message.channel, "Invalid argument. Use `update <project>` with a project configured in update_config.json")
