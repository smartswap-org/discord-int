from ..logs import *
from .set_permissions import set_clients_permissions
from ..embeds.embeds import *

async def create_missing_wallet_channels(client, category, wallets):
    for wallet in wallets:
        wallet_name = wallet['name'].lower()
        if not discord.utils.get(category.channels, name=wallet_name):
            await discord_log(client, "Clients Rooms", f"Creating channel for wallet '{wallet_name}'.")
            new_wallet_room = await category.create_text_channel(wallet_name)
            await send_embed(new_wallet_room, "New Channel Created", f"The channel {wallet_name} has just been created.", discord.Color.pink())

async def delete_unused_wallet_channels(client, category, wallets):
    for channel in category.channels:
        discord_user_ids = [row[0] for row in client.db_smartswap.execute_query(f"SELECT clients.discord_user_id FROM clients JOIN wallets_access ON wallets_access.client_user = clients.user JOIN wallets ON wallets.name = wallets_access.wallet_name WHERE wallets_access.wallet_name = '{channel.name}'")]
        await set_clients_permissions(client, channel, discord_user_ids)  # Passing discord_user_ids
        if channel.name.lower() not in [wallet['name'].lower() for wallet in wallets]:
            await discord_log(client, "Clients Rooms", f"Deleting channel '{channel.name}' as it does not correspond to any wallet.")
            await channel.delete()