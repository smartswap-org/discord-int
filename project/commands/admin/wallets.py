from ...misc.logs import *
from DEXcryptoLib.Lib.Misc.database import *

async def wallets(client, message, args):
    usage = """Invalid argument(s) number. Use:
    wallets create <name> <address> <private_key> <discord_chanmsglogs_id>
    wallets delete <name>
    wallets search <name>
    """
    if not args or len(args) < 1:
        await error(message.channel, usage)
    else:
        match args[0]:
            case "create":
                if len(args) != 5:
                    await error(message.channel, usage)
                try:
                    name = args[1].lower()
                    existing_user = client.db_smartswap.execute_query(f"SELECT * FROM wallets WHERE name = '{name}'")
                    if existing_user:
                        return await error(message.channel, f"Wallet with name '{name}' already exists.")
                    
                    values_to_insert = {'name': name, 'address': args[2], 'private_key': args[3], 'discord_chanmsglogs_id': args[4]}
                    client.db_smartswap.insert_into_table('wallets', values_to_insert)
                    values_to_insert["private_key"] = "*hided*"
                    await send_embed(
                        message.channel,
                        "✅ Success",
                        f": {values_to_insert} has been inserted into the database.",
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while inserting into the database. \n{e}")
            
            
            case "search":
                if len(args) != 2:
                    await error(message.channel, usage)
                try:
                    query = client.db_smartswap.execute_query(f"SELECT wallets.name FROM wallets WHERE wallets.name = '{args[1]}';")
                    if query:
                        return await send_embed(
                            message.channel, 
                            f"⚙️ Searched by: name",
                            f"{query}",
                            discord.Color.green()
                        )
                    return await error(message.channel, f"'{args[1]}' in wallets table of smartswap database has not been found.")
                except Exception as e:
                    print({e})
                    await error(message.channel, f"Error while searching into the database. \n{e}")

            case "delete":
                if len(args) != 2:
                    await error(message.channel, usage)
                try:
                    wallet_name = args[1]

                    # Check if the wallet address exists in the wallets table
                    query = client.db_smartswap.execute_query(f"DELETE FROM wallets_access WHERE wallet_name = '{wallet_name }';")
                    await send_embed(
                        message.channel, 
                        f"⚙️ Success removed all access to the wallet {wallet_name } for all clients",
                        f"",
                        discord.Color.pink()
                    )
                    
                    # Delete the wallet address from the wallets table
                    try:
                        client.db_smartswap.delete_row_by_column_value('wallets', 'name', wallet_name)
                    except Exception as e:
                        return await error(message.channel, f"Error while deleting '{wallet_name}' from the table: wallets. \n{e}")

                    return await send_embed(
                        message.channel, 
                        f"Wallet '{wallet_name}' has been deleted from the whole database.",
                        f"",
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while searching into the database. \n{e}")

            
            case _:
                if message:
                    return await error(message.channel, usage)
