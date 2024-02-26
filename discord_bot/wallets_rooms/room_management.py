import discord 
from discord_bot.discordlogs.discord_log import discord_log
from .room_creation import create_missing_wallet_channels, delete_unused_wallet_channels

async def check_wallets_rooms(client, category_id):
    """
    Check the Rooms Category for each wallets from the database.
    Create/Delete, grant or remove access to clients
    """
    try:
        # Get all channels from the configured category_id (configs/bot_config.json | roomscategid)
        category = discord.utils.get(client.get_all_channels(), id=category_id) 

        if not category or not isinstance(category, discord.CategoryChannel): 
            # The category doesnt exist and the code cant perform his job
            await discord_log(client, "Clients Rooms", f"Category with ID {category_id} not found.")
            return

        # Get all wallets from the table wallets from the database smartswap
        wallets = [{'name': wallet[0]} for wallet in client.db_smartswap.execute_query("SELECT * FROM wallets")]

        await create_missing_wallet_channels(client, category, wallets)
        await delete_unused_wallet_channels(client, category, wallets)

    except Exception as e:
        await discord_log(client, "Error", f"Error during wallet and room checking: {e}")
