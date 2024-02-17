import discord 
from discord_bot.discordlogs import error 
from discord_bot.embeds.embeds import send_embed
from DEXcryptoLib.Lib.Misc.database import *

async def clients(client, message, args):
    usage = """Invalid argument(s) number. Use:
    clients create <user> <discord_user_id>
    clients delete <user/discord_user_id>
    clients search <user/discord_user_id>
    clients access_set <clients_user> <wallet_name>
    clients access_revoke <clients_user> <wallet_name>
    """
    
    if not args or len(args) < 2:
        return await error(message.channel, usage)

    action = args[0].lower()

    match action:
        case "create":
            await create_user(client, message, args, usage)

        case "search":
            await search_user(client, message, args, usage)

        case "delete":
            await delete_user(client, message, args, usage)

        case "access_set":
            await access_set(client, message, args, usage)

        case "access_revoke":
            await access_revoke(client, message, args, usage)

        case _:
            await error(message.channel, usage)

async def create_user(client, message, args, usage):
    try:
        if len(args) != 3:
            return await error(message.channel, usage)

        user, discord_user_id = args[1].lower(), args[2]

        existing_user = client.db_smartswap.execute_query(f"SELECT * FROM clients WHERE user = '{user}'")
        if existing_user:
            return await error(message.channel, f"User with username '{user}' already exists.")

        values_to_insert = {'user': user, 'discord_user_id': discord_user_id}
        client.db_smartswap.insert_into_table('clients', values_to_insert)

        await send_embed(
            message.channel,
            "✅ Success",
            f"User '{user}' with Discord User ID '{discord_user_id}' has been inserted into the database.",
            discord.Color.green()
        )

    except Exception as e:
        await error(message.channel, f"Error while inserting into the database. \n{e}")

async def search_user(client, message, args, usage):
    try:
        if len(args) != 2:
            return await error(message.channel, usage)

        search_term = args[1]

        columns = client.db_smartswap.execute_query("SHOW COLUMNS FROM clients")
        for column in [column[0] for column in columns]:
            query = client.db_smartswap.execute_query(f"SELECT user, discord_user_id FROM clients WHERE {column} = '{search_term}'")
            if query:
                return await send_embed(
                    message.channel,
                    f"⚙️ Searched by: {column}",
                    f"{query}",
                    discord.Color.green()
                )

        await error(message.channel, f"'{search_term}' not found in clients table of smartswap database.")

    except Exception as e:
        await error(message.channel, f"Error while searching into the database. \n{e}")

async def delete_user(client, message, args, usage):
    try:
        if len(args) != 2:
            return await error(message.channel, usage)

        delete_term = args[1]

        columns = client.db_smartswap.execute_query("SHOW COLUMNS FROM clients")
        for column in [column[0] for column in columns]:
            query = client.db_smartswap.execute_query(f"SELECT user, discord_user_id FROM clients WHERE {column} = '{delete_term}'")
            if query:
                try:
                    client.db_smartswap.delete_row_by_column_value('clients', column, delete_term)
                except Exception as e:
                    return await error(message.channel, f"Error while deleting '{delete_term}' from the clients table. \n{e}")

                return await send_embed(
                    message.channel,
                    f"⚙️ Success removed from the table (clients) by: {column}",
                    f"{delete_term}",
                    discord.Color.green()
                )

        await error(message.channel, f"'{delete_term}' not found in clients table of smartswap database.")

    except Exception as e:
        await error(message.channel, f"Error while searching into the database. \n{e}")

async def access_set(client, message, args, usage):
    try:
        if len(args) != 3:
            return await error(message.channel, usage)

        user, name = args[1].lower(), args[2].lower()

        existing_user = client.db_smartswap.execute_query(f"SELECT * FROM clients WHERE user = '{user}'")
        if not existing_user:
            return await error(message.channel, f"User with username '{user}' does not exist. Please create the user first.")

        existing_name = client.db_smartswap.execute_query(f"SELECT * FROM wallets WHERE name = '{name}'")
        if not existing_name:
            return await error(message.channel, f"Wallet with name '{name}' does not exist. Please make sure the name is correct.")

        existing_access = client.db_smartswap.execute_query(f"SELECT * FROM wallets_access WHERE client_user = '{user}' AND wallet_name = '{name}'")
        if existing_access:
            return await error(message.channel, f"Access for user: '{user}' on wallet '{name}' already exists.")

        client.db_smartswap.insert_into_table('wallets_access', {'client_user': user, 'wallet_name': name})
        await send_embed(
            message.channel,
            "✅ Success",
            f"Access for user '{user}' on wallet '{name}' has been added to the database.",
            discord.Color.green()
        )

    except Exception as e:
        await error(message.channel, f"Error while inserting into the database. \n{e}")

async def access_revoke(client, message, args, usage):
    try:
        if len(args) != 3:
            return await error(message.channel, usage)

        user, name = args[1].lower(), args[2].lower()

        existing_access = client.db_smartswap.execute_query(f"SELECT * FROM wallets_access WHERE client_user = '{user}' AND wallet_name = '{name}'")
        if not existing_access:
            return await error(message.channel, f"Access for user: '{user}' on wallet '{name}' does not exist.")

        client.db_smartswap.delete_row_by_column_values('wallets_access', {'client_user': user, 'wallet_name': name})
        await send_embed(
            message.channel,
            "✅ Success",
            f"Access for user '{user}' on wallet '{name}' has been revoked and removed from the database.",
            discord.Color.green()
        )

    except Exception as e:
        await error(message.channel, f"Error while revoking access from the database. \n{e}")
