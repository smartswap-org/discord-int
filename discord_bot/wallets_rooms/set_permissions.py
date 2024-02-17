from ..d_logs import *


async def set_clients_permissions(client, channel, discord_user_ids):
    try:
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
