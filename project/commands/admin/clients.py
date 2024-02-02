from ...misc.logs import *
from DEXcryptoLib.Lib.Misc.database import *

async def clients(client, message, args):
    usage = """Invalid argument(s) number. Use:
    clients create <user> <discord_user_id>
    clients delete <user/discord_user_id>
    clients search <user/discord_user_id>
    """
    if not args or len(args) < 1:
        await error(message.channel, usage)
    else:
        match args[0]:
            case "create":
                if len(args) != 3:
                    await error(message.channel, usage)
                try:
                    values_to_insert = {
                        'user': args[1],
                        'discord_user_id': args[2]
                    }
                    client.db_smartswap.insert_into_table('clients', values_to_insert)
                    await send_embed(
                        message.channel,
                        "✅ Success",
                        f"""
                            The user: {args[1]} 
                            with discord_user_id: {args[2]} 
                            has been inserted into the database.\n
                        """,
                        discord.Color.green()
                    )
                except Exception as e:
                    await error(message.channel, f"Error while inserting into the database. \n{e}")
            
            case "search":
                if len(args) !=2: await error(message.channel, usage)
                try:
                    columns = client.db_smartswap.execute_query(f"SHOW COLUMNS FROM clients")
                    for i in [column[0] for column in columns]:
                        query = client.db_smartswap.execute_query(f"SELECT clients.user, clients.discord_user_id FROM clients WHERE clients.{i} = '{args[1]}';")
                        if query:
                            return await send_embed(
                            message.channel, 
                            f"⚙️ Searched by: {i}",
                            f"""{query}""",
                            discord.Color.green()
                            )
                    return await error(message.channel, f"'{args[1]}' in clients table of smartswap database has not been found.")
                except Exception as e:
                    print({e})
                    await error(message.channel, f"Error while searching into the database. \n{e}")


            
            case "delete":
                if len(args) != 2:
                    await error(message.channel, usage)
                try:
                    columns = client.db_smartswap.execute_query(f"SHOW COLUMNS FROM clients")
                    for i in [column[0] for column in columns]:
                        query = client.db_smartswap.execute_query(f"SELECT clients.user, clients.discord_user_id FROM clients WHERE clients.{i} = '{args[1]}';")
                        if query:
                            try:
                                # Use the correct method for deletion
                                client.db_smartswap.delete_row_by_column_value('clients', i, args[1])
                            except Exception as e:
                                return await error(message.channel, f"Error while deleting {args[1]} from the table: clients. \n{e}")
                            return await send_embed(
                                message.channel, 
                                f"⚙️ Success removed from the table (clients) by: {i}",
                                f"""{args[1]}""",
                                discord.Color.green()
                            )
                    return await error(message.channel, f"'{args[1]}' in clients table of smartswap database has not been found.")
                except Exception as e:
                    await error(message.channel, f"Error while searching into the database. \n{e}")
            
            case _:
                if message:
                    return await error(message.channel, usage)
