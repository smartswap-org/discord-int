from ...misc.logs import *
from DEXcryptoLib.Lib.Misc.database import *

async def wallets(client, message, args):
    usage = """Invalid argument(s) number. Use:
    wallets create <address> <private_key> <discord_chanmsglogs_id>
    wallets delete <address>
    wallets search <address>
    """
    if not args or len(args) < 1:
        await error(message.channel, usage)
    else:
        match args[0]:
            case "create":
                if len(args) != 4:
                    await error(message.channel, usage)
                try:
                    address = args[1]
                    existing_user = client.db_smartswap.execute_query(f"SELECT * FROM wallets WHERE address = '{address}'")
                    if existing_user:
                        return await error(message.channel, f"Wallet with address '{address}' already exists.")
                    
                    values_to_insert = {'address': args[1], 'private_key': args[2], 'discord_chanmsglogs_id': args[3]}
                    client.db_smartswap.insert_into_table('wallets', values_to_insert)
                    await send_embed(
                        message.channel,
                        "✅ Success",
                        f"The address: {args[1]} with discord_chan_id: {args[3]} has been inserted into the database.",
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while inserting into the database. \n{e}")
            
            
            case "search":
                if len(args) != 2:
                    await error(message.channel, usage)
                try:
                    query = client.db_smartswap.execute_query(f"SELECT wallets.address FROM wallets WHERE wallets.address = '{args[1]}';")
                    if query:
                        return await send_embed(
                            message.channel, 
                            f"⚙️ Searched by: address",
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
                    wallet_address = args[1]

                    # Check if the wallet address exists in the wallets table
                    query = client.db_smartswap.execute_query(f"DELETE FROM client_wallets WHERE wallet_address = '{wallet_address}';")
                    await send_embed(
                        message.channel, 
                        f"⚙️ Success removed all access to the wallet {wallet_address} for all clients",
                        f"",
                        discord.Color.pink()
                    )
                    
                    # Delete the wallet address from the wallets table
                    try:
                        client.db_smartswap.delete_row_by_column_value('wallets', 'address', wallet_address)
                    except Exception as e:
                        return await error(message.channel, f"Error while deleting '{wallet_address}' from the table: wallets. \n{e}")

                    return await send_embed(
                        message.channel, 
                        f"Wallet {wallet_address} has been deleted from the whole database.",
                        f"{wallet_address}",
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while searching into the database. \n{e}")

            
            case _:
                if message:
                    return await error(message.channel, usage)
