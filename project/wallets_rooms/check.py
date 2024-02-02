from ..misc.logs import *
from ..misc.embeds import *
from ..misc.config import *
from DEXcryptoLib.Lib.Misc.database import *


async def check_wallets_rooms(client, category_id):
    try:
        category = discord.utils.get(client.get_all_channels(), id=category_id)

        if not category or not isinstance(category, discord.CategoryChannel):
            await discord_log(client, "Error", f"Category with ID {category_id} not found.")
            return

        wallets = [{'address': wallet[0]} for wallet in client.db_smartswap.execute_query("SELECT * FROM wallets")]

        for channel in category.channels:
            if channel.name not in [wallet['address'] for wallet in wallets]:
                await discord_log(client, "Channel Deletion", f"Deleting channel '{channel.name}' as it does not correspond to any wallet.")
                await channel.delete()

        for wallet in wallets:
            wallet_address = wallet['address']
            if not discord.utils.get(category.channels, name=wallet_address):
                await discord_log(client, "Channel Creation", f"Creating channel for wallet '{wallet_address}'.")
                await category.create_text_channel(wallet_address)


    except Exception as e:
        await discord_log(client, "Error", f"Error during wallet and room checking: {e}")

async def check_channel_access(client, channel, member):
    try:
        access = channel.permissions_for(member).read_messages and channel.permissions_for(member).send_messages
        if not access:
            await discord_log(client, "Channel Access Error", f"User {member.display_name} does not have access to channel {channel.name}")
        return access
    except Exception as e:
        discord_log(client, "Error", f"Error checking channel access: {e}")
        return False