import discord
from discord import Activity, ActivityType
from discord.ext import tasks
from project import * # Project includes

bot_config = get_bot_config()

client_commands = {

}

admin_commands = { # All bot commands
    'clear': clear,
    'host': host,
    'restart': restart,
    'tmux': tmux,
    'logschannelid': logschannelid,
    'ping': ping,
    'clients': clients
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

class MyClient(discord.Client): # Create the client object for the bot
    async def on_ready(self): # When the bot start
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.db_smartswap = init_database("smartswap", "db_config.json")
        self.db_smartswap.connect()
        await self.change_presence(activity=Activity(type=ActivityType.custom, name=" ", details=" ", state="➡️ " + bot_config["prefix"] +"help")) # Rich presence
        self.tmux_task.start() # // While
        await discord_log(client, "Bot", "🤖 Bot started")   

    @tasks.loop(seconds=5)
    async def tmux_task(self): # Execute tmux checkup every 5 seconds
        await tmux(self, None, ['checkup'])

    async def on_message(self, message): # When a message is sent
        if message.author.id == self.user.id: return  # No respond to itself
        # Imperative security that make the bot interract only on the configured discord channel (usage and logs channels)
        if str(message.guild.id) != bot_config["discordid"]: return  # Security to only use bot in a room
        content = message.content[len(bot_config["prefix"]):].split() # Separate command and arguments
        if not content: return # Security if there is no command and only prefix
        if message.content[:len(bot_config["prefix"])] != bot_config["prefix"]: return # Not good prefix command
        command = content[0] 
        args = content[1:]
        if command in admin_commands: # Verify that the command sent is in commands list
            if message.author.guild_permissions.administrator: # Admin permission security to use the bot
                if message.channel.name == "smartswap": # To use the bot in log channel: str(message.channel.id) == bot_config["logschannelid"] 
                    print("admin-Command: " + bot_config["prefix"] + command + " | Author: " + str(message.author) + "(" + str(message.author.id) + ") | Channel: " + str(message.channel.name))
                    await admin_commands[command](self, message, args) 
            else:
                    return await error(message.channel, "You dont have the permission to use this command (Admin permission).") 
        elif command in client_commands:
            await client_commands[command](self, message, args) 

client = MyClient(intents=discord.Intents.all()) # Declare the client object
client.run(bot_config["token"]) # Log the client (bot)
