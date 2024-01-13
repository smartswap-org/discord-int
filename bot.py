import discord
from discord import Activity, ActivityType
from discord.ext import commands, tasks
from project import * # Project includes

bot_config = get_bot_config()

commands = { # All bot commands
    'clear': clear,
    'host': host,
    'restart': restart,
    'tmux': tmux,
    'logschannelid': logschannelid,
    'ping': ping,
}

async def help(client, message, args): # Command !help that print all commands
    """
    Function to send a message in embed 
    with the list of bot commands by printing them 1 per line.
    """
    cmdslist = ""
    for i in commands:
        cmdslist += bot_config["prefix"] + i + "\n"
    await send_embed(message.channel, "📜 Commands list", cmdslist, discord.Color.pink()) 

commands["help"] = help

class MyClient(discord.Client): # Create the client object for the bot
    async def on_ready(self): # When the bot start
        print(f'Logged in as {self.user} (ID: {self.user.id})')
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
        if command in commands: # Verify that the command sent is in commands list
            print("Command: " + bot_config["prefix"] + command + " | Author: " + str(message.author) + "(" + str(message.author.id) + ") | Channel: " + str(message.channel.name))
            if message.channel.name == "smartswap" or str(message.channel.id) == bot_config["logschannelid"]: 
                if message.author.guild_permissions.administrator: # Admin permission security to use the bot
                    await commands[command](self, message, args) 
                else:
                    return await error(message.channel, "You dont have the permission to use the bot.") 
            #else:
                #return await error(message.channel, "You can only use the bot in the smartswap room.")
               
db_smartswap = init_database("smartswap", "db_config.json")
db_smartswap.connect()
client = MyClient(intents=discord.Intents.all()) # Declare the client object
client.run(bot_config["token"]) # Log the client (bot)
