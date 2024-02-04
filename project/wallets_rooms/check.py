from ..misc.logs import *
from ..misc.embeds import *
from ..misc.config import *
from DEXcryptoLib.Lib.Misc.database import *

async def set_clients_permissions(client, channel):
    query = f"""
        SELECT clients.discord_user_id
        FROM clients
        JOIN client_wallets ON client_wallets.client_user = clients.user
        JOIN wallets ON wallets.name = client_wallets.wallet_name
        WHERE client_wallets.wallet_name = '{channel.name}';
        """

    try:
        result = client.db_smartswap.execute_query(query)
        discord_user_ids = [row[0] for row in result]  # tab for all discord_user_id that have access to this channel

        # Remove permissions for users not in discord_user_ids
        for permission_overwrite in channel.overwrites:
            if isinstance(permission_overwrite, discord.Member):
                if str(permission_overwrite.id) not in discord_user_ids:
                    await channel.set_permissions(permission_overwrite, read_messages=False)

        # Add permissions for users in discord_user_ids
        for client_id in discord_user_ids:
            try:
                user = await channel.guild.fetch_member(int(client_id))  # user object
                if user:
                    if not channel.permissions_for(user).read_messages:
                        await channel.set_permissions(user, read_messages=True)
                        await discord_log(client, "Clients Rooms", f"Added read permission for user with ID {client_id} in channel {channel.name}")

            except Exception as e:
                print(f"Error adding read permission: {e}")

    except Exception as e:
        log("db", f"Error during query execution: {e}")
        return False

async def check_wallets_rooms(client, category_id):
    try:
        category = discord.utils.get(client.get_all_channels(), id=category_id)

        if not category or not isinstance(category, discord.CategoryChannel):
            await discord_log(client, "Clients Rooms", f"Category with ID {category_id} not found.")
            return

        wallets = [{'name': wallet[0]} for wallet in client.db_smartswap.execute_query("SELECT * FROM wallets")]

        for wallet in wallets:
            wallet_name = wallet['name'].lower()
            if not discord.utils.get(category.channels, name=wallet_name):
                await discord_log(client, "Clients Rooms", f"Creating channel for wallet '{wallet_name}'.")
                new_wallet_room = await category.create_text_channel(wallet_name)
                await send_embed(new_wallet_room, "New Channel Created", f"The channel {wallet_name} has just been created.", discord.Color.pink())

        for channel in category.channels:
            await set_clients_permissions(client, channel)
            if channel.name.lower() not in [wallet['name'].lower() for wallet in wallets]:
                await discord_log(client, "Clients Rooms", f"Deleting channel '{channel.name}' as it does not correspond to any wallet.")
                await channel.delete()

    except Exception as e:
        await discord_log(client, "Error", f"Error during wallet and room checking: {e}")
