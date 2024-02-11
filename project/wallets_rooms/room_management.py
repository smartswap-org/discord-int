from .room_creation import create_missing_wallet_channels, delete_unused_wallet_channels
from ..logs import *
from ..embeds.embeds import *

async def check_wallets_rooms(client, category_id):
    try:
        category = discord.utils.get(client.get_all_channels(), id=category_id)

        if not category or not isinstance(category, discord.CategoryChannel):
            await discord_log(client, "Clients Rooms", f"Category with ID {category_id} not found.")
            return

        wallets = [{'name': wallet[0]} for wallet in client.db_smartswap.execute_query("SELECT * FROM wallets")]

        await create_missing_wallet_channels(client, category, wallets)
        await delete_unused_wallet_channels(client, category, wallets)

    except Exception as e:
        await discord_log(client, "Error", f"Error during wallet and room checking: {e}")
