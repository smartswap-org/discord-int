from ...misc.logs import *
from DEXcryptoLib.Lib.Misc.database import *

async def wallets(client, message, args):
    usage = """Invalid argument(s) number. Use:
    wallets create <address> <private_key> <discord_chan_id>
    wallets delete <address/discord_chan_id>
    wallets search <address/discord_chan_id>
    """
    if not args or len(args) < 1:
        await error(message.channel, usage)
    else:
        match args[0]:
            case "create":
                if len(args) != 4:
                    await error(message.channel, usage)
                try:
                    discord_chan_id = args[3]
                    existing_user = client.db_smartswap.execute_query(f"SELECT * FROM wallets WHERE discord_chan_id = '{discord_chan_id}'")
                    if existing_user:
                        return await error(message.channel, f"User with discord_chan_id '{discord_chan_id}' already exists.")
                    
                    values_to_insert = {'address': args[1], 'private_key': args[2], 'discord_chan_id': discord_chan_id}
                    client.db_smartswap.insert_into_table('wallets', values_to_insert)
                    await send_embed(
                        message.channel,
                        "✅ Success",
                        f"The address: {args[1]} with discord_chan_id: {discord_chan_id} has been inserted into the database.",
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while inserting into the database. \n{e}")
            
            
            case "search":
                if len(args) != 2:
                    await error(message.channel, usage)
                try:
                    columns = client.db_smartswap.execute_query(f"SHOW COLUMNS FROM wallets")
                    for i in [column[0] for column in columns]:
                        query = client.db_smartswap.execute_query(f"SELECT wallets.address, wallets.discord_chan_id FROM wallets WHERE wallets.{i} = '{args[1]}';")
                        if query:
                            return await send_embed(
                                message.channel, 
                                f"⚙️ Searched by: {i}",
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
                    columns = client.db_smartswap.execute_query(f"SHOW COLUMNS FROM wallets")
                    for i in [column[0] for column in columns]:
                        query = client.db_smartswap.execute_query(f"SELECT wallets.address, wallets.discord_chan_id FROM wallets WHERE wallets.{i} = '{args[1]}';")
                        if query:
                            try:
                                client.db_smartswap.delete_row_by_column_value('wallets', i, args[1])
                            except Exception as e:
                                return await error(message.channel, f"Error while deleting {args[1]} from the table: wallets. \n{e}")
                            return await send_embed(
                                message.channel, 
                                f"⚙️ Success removed from the table (wallets) by: {i}",
                                f"{args[1]}",
                                discord.Color.green()
                            )
                    return await error(message.channel, f"'{args[1]}' in wallets table of smartswap database has not been found.")
                except Exception as e:
                    await error(message.channel, f"Error while searching into the database. \n{e}")
            
            case _:
                if message:
                    return await error(message.channel, usage)
