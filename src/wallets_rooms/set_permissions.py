import discord 
from src.discordlogs.discord_log import discord_log
from DEXcryptoLib.Lib.Misc.logs import log

async def set_clients_permissions(client, channel, discord_user_ids):
    """
    This function checks the permissions of every user on a channel within the Room Category (config/bot_config.json | roomscategid). 
    It removes access for users who don't have access in the database table clients_wallets, 
    and grants access for those who have access but haven't been granted it yet.
    """
    try:
        # Remove permissions for users not in discord_user_ids (users that dont have access from the database table clients_wallets)
        for permission_overwrite in channel.overwrites:
            if isinstance(permission_overwrite, discord.Member):
                if str(permission_overwrite.id) not in discord_user_ids:
                    await channel.set_permissions(permission_overwrite, read_messages=False)

        # Add permissions for users in discord_user_ids (users that have access to this wallet from database table clients_wallets)
        for client_id in discord_user_ids:
            try:
                user = await channel.guild.fetch_member(int(client_id))  # user object
                if user:
                    if not channel.permissions_for(user).read_messages: # if he dont have the permission to read the channel  
                        await channel.set_permissions(user, read_messages=True) # grant the permission to see messages (supposed see channel too)
                        await discord_log(client, "Clients Rooms", f"Added read permission for user with ID {client_id} in channel {channel.name}")

            except Exception as e:
                print(f"Error adding read permission: {e}")

    except Exception as e:
        log("db", f"Error during query execution: {e}")
        return False
