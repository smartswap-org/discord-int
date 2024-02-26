import discord 
from discord_bot.discordlogs.discord_log import discord_log
from discord_bot.embeds.embeds import send_embed
from .set_permissions import set_clients_permissions

# In this code, we use 
# wallet_name = wallet['name'].lower() 
# to avoid any confusion and error when inserting/content in/from database.

async def create_missing_wallet_channels(client, category, wallets):
    """
    client : discord obj of the discord bot
    category : category obj of "Wallets Rooms"
    wallets : tab with every wallets (found in the table wallets on smartswap database)
    """
    for wallet in wallets: # Check for every wallet
        wallet_name = wallet['name'].lower() 
        if not discord.utils.get(category.channels, name=wallet_name): # Check if the category has the a channel with this wallet name 
            # The category on the discord dont have a channel with this wallet name
            await discord_log(client, "Clients Rooms", f"Creating channel for wallet '{wallet_name}'.") 
            
            # Create the channel in the category with the wallet name
            new_wallet_room = await category.create_text_channel(wallet_name)
            await send_embed(new_wallet_room, "New Channel Created", f"The channel {wallet_name} has just been created.", discord.Color.pink())

async def delete_unused_wallet_channels(client, category, wallets):
    """
    client : discord obj of the discord bot
    category : category obj of "Wallets Rooms"
    wallets : tab with every wallets (found in the table wallets on smartswap database)
    """
    for channel in category.channels: # Check all rooms in the category
        discord_user_ids = [
            row[0] for row in client.db_smartswap.execute_query(
                            f"""
                            SELECT clients.discord_user_id 
                            FROM clients 
                            JOIN wallets_access ON wallets_access.client_user = clients.user 
                            JOIN wallets ON wallets.name = wallets_access.wallet_name 
                            WHERE wallets_access.wallet_name = '{channel.name}'
                            """) # This request get all the clients that have access to this wallet name
                            ]
        # Checking permissions of every clients on this channel and check if they are allowed with the result of the database request
        # NB: If you use !client revoke_access <wallet_name>, it will edit the table clients_wallets and this function will remove permission and/or add permission to the userdiscordid
        await set_clients_permissions(client, channel, discord_user_ids)  

        # If this channel name(supposed this wallet) is not in the wallets list from database
        #   -> Delete the channel
        if channel.name.lower() not in [wallet['name'].lower() for wallet in wallets]:
            await discord_log(client, "Clients Rooms", f"Deleting channel '{channel.name}' as it does not correspond to any wallet.")
            await channel.delete()