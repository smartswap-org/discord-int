import discord
from discord import Activity, ActivityType
from discord.ext import tasks
from discord_bot import * # Project includes

#To make: a script to install all the dependicies with pip
    #dependicies:
    #web3
    #discord
    #pmysql-connector-python
    #psutil

bot_config = get_bot_config() # Get the config configs/bot_config.json

client_commands = {
    # No commands yet for clients
}

admin_commands = { # Admin commands: discord_bot/commands/admin/*
    'clear': clear,
    'host': host,
    'restart': restart,
    'tmux': tmux,
    'logschannelid': logschannelid,
    'ping': ping,
    'clients': clients,
    'wallets': wallets,
    'git': git
}

async def help(client, message, args): # Command !help that print all commands
    """
    Function to send a message in embed 
    with the list of bot commands by printing them 1 per line.
    """
    cmdslist = "- **client_commands**:\n"
    for i in client_commands:
        cmdslist += bot_config["prefix"] + i + "\n"
    if message.author.guild_permissions.administrator:
        cmdslist += "\n- **admin_commands**:\n"
        for i in admin_commands:
            cmdslist += bot_config["prefix"] + i + "\n"
    await send_embed(message.channel, "📜 Commands list", cmdslist, discord.Color.pink()) 

client_commands["help"] = help

class MyClient(discord.Client):
    async def on_ready(self): 
        """
        Toggeled at every start of the bot
        """
        subprocess.run(["bash", "scripts/create_config_files.sh"]) # Create config scripts if they dont exists
        print(f'Logged in as {self.user} (ID: {self.user.id})') 
        self.db_smartswap = init_database("smartswap", "configs/db_config.json") # Get config of the database smartswap from configs/db_config.json
        self.db_smartswap.connect() # Connected to the database smartswap
        await self.change_presence(activity=Activity(type=ActivityType.custom, name=" ", details=" ", state="➡️ " + bot_config["prefix"] +"help")) # Rich presence
        self.tmux_task.start()                # A loop cheeckup of tmux_task fonction
        self.check_wallets_rooms_task.start() # A loop cheeckup of check_wallets_rooms_task fonction
        await log_bot_infos(client)   

    @tasks.loop(seconds=5)
    async def tmux_task(self):
        """
        Execute tmux checkup every 5 seconds, if a tmux configured session 
        in configs/tmux_config.json is not on tmux list-session (not running) and
        start it if needed.
        """
        await tmux(self, None, ['checkup'])

    @tasks.loop(seconds=5)
    async def check_wallets_rooms_task(self): 
        """
        Checks that the rooms in the roomscategid category configured in configs/bot_config exist for each wallet 
        in the table wallets in database smartswap and assigns permissions to each user with clients_wallets 
        and for each client from the clients table (userdiscordid).
        """
        await check_wallets_rooms(self, int(bot_config["roomscategid"]))

    async def on_message(self, message): 
        """
        Toggled at every message sent
        """
        if message.author.id == self.user.id: return  # No respond to itself
        
        # Imperative security that make the bot interract only on the configured discord channel (usage and logs channels)
        if str(message.guild.id) != bot_config["discordid"]: return  

        content = message.content[len(bot_config["prefix"]):].split() # Separate command and arguments
        if not content: return # Security if there is no command and only prefix

        if message.content[:len(bot_config["prefix"])] != bot_config["prefix"]: return # Not good prefix command

        command = content[0] 
        args = content[1:]

        if command in admin_commands: # Verify that the command sent is in commands list
            if message.author.guild_permissions.administrator: # Admin permission security to use the bot
                #if message.channel.name == "smartswap" or str(message.channel.id) == bot_config["logschannelid"] : # channel must be smartswap or the log channel
                print("admin-Command: " + bot_config["prefix"] + command + " | Author: " + str(message.author) + "(" + str(message.author.id) + ") | Channel: " + str(message.channel.name))
                await admin_commands[command](self, message, args) 
            else:
                    return await error(message.channel, "You dont have the permission to use this command (Admin permission).") 
        elif command in client_commands:
            await client_commands[command](self, message, args) 


client = MyClient(intents=discord.Intents.all()) # Declare the client object
client.run(bot_config["token"]) # Log the client (bot)
