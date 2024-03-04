import discord
import subprocess
from discord_bot.discordlogs import error, discord_log
from discord_bot.embeds.embeds import send_embed
from discord_bot.config import get_tmux_config
from DEXcryptoLib.Lib.Misc.json import *

async def tmux(client, message, args):
    usage = """Invalid argument(s) number. Use:
    tmux list-sessions
    tmux config
    tmux checkup (internal usage)
    tmux new <name> <command>
    tmux remove <name>
    """

    if not args or len(args) < 1:
        await error(message.channel, usage)
    else:
        tmux_config = get_tmux_config()
        match args[0]:
            case "list-sessions":
                try:
                    result = subprocess.run(['sudo', 'tmux', 'list-sessions'], capture_output=True, text=True)
                    if result.returncode == 0: 
                        output = result.stdout
                    else:
                        output = "0 tmux on tmux" #result.stderr
                    await send_embed(
                        message.channel,
                        "🖥️ tmux (list-sessions)",
                        output,
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error during command ['tmux', 'list-sessions'].\n {e}")
            case "config":
                embed_desc = "**Name | Config**\n\n"
                match tmux_config:
                    case -1:
                        return await tmux(client, message, args)
                    case -2:
                        embed_desc = "Error when reading file."
                    case _:
                        for i in tmux_config.keys():
                            embed_desc = embed_desc + i + " | " + tmux_config[i] + "\n"
                await send_embed(
                    message.channel,
                    "🖥️ tmux (config)",
                    embed_desc,
                    discord.Color.yellow()
                )
            case "checkup":
                match tmux_config:
                    case -1, -2:
                        return await discord_log(client, "Error", "Error while reading tmux config.", discord.Color.red()) 
                tmuxlist = subprocess.run(['sudo', 'tmux', 'list-sessions'], capture_output=True, text=True)
                tmuxoutput = tmuxlist.stdout
                for key in tmux_config.keys():
                    if not key in tmuxoutput:
                        argline = tmux_config[key].split(" ", 1)
                        command_os = ['sudo', 'tmux', 'new-session', '-d', '-s', key] + '"' + argline + '"'
                        print("tmux", command_os)
                        subprocess.run(command_os) 
                        await discord_log(client, 
                                          ("🖥️ tmux (start)", "tmux:" + str(key)), 
                                          discord.Color.green())     
            case "new":
                if len(args) < 3: return await error(message.channel, usage)
                if not tmux_config: tmux_config = {}
                tmux_config[args[1]] = ' '.join(args[2:])
                write_json("tmux_config.json", tmux_config)
                await send_embed(
                    message.channel, 
                    "🖥️ tmux (new)",
                    "New tmux:\nname: " + args[1] + "\ncommand: "+ tmux_config[args[1]],
                    discord.Color.green()
                    )
            case "remove":
                if len(args) != 2: return await error(message.channel, usage) 
                if args[1] in tmux_config.keys():
                    del tmux_config[args[1]]
                    write_json("tmux_config.json", tmux_config)
                    await send_embed(
                        message.channel,
                        "🖥️ tmux (remove)",
                        "tmux: " + args[1] + " has been deleted.",
                        discord.Color.green()
                    )
                else:
                    await send_embed(
                        message.channel,
                        "🖥️ tmux (remove)",
                        "tmux: " + args[1] + " doesn't exist.",
                        discord.Color.red()
                    )
            case _:
                if message:
                    return await error(message.channel, usage)