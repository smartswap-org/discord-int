def db_setup_smartswap(db):
    """
    Checks if the tables required exist or not.
    If not, the function creates them.

    Parameters:
    - db: An instance of the DatabaseSQL class.
    """
    result = db.execute_query("SHOW TABLES LIKE 'wallets';")
    if not result:
        query_create_table = """
            CREATE TABLE `wallets` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(255),
                network VARCHAR(255),
                wallet_key VARCHAR(255),
                discord_chan_id INT
            );
        """
        db.execute_query(query_create_table)

    result = db.execute_query("SHOW TABLES LIKE 'clients';")
    if not result:
        query_create_table = """
            CREATE TABLE `clients` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name CHAR(255),
                discord_id INT
            );
        """
        db.execute_query(query_create_table)

    result = db.execute_query("SHOW TABLES LIKE 'client_wallets';")
    if not result:
        query_create_table = """
            CREATE TABLE `client_wallets` (
                client_id INT,
                wallet_id INT,
                PRIMARY KEY (client_id, wallet_id),
                FOREIGN KEY (client_id) REFERENCES `clients`(id),
                FOREIGN KEY (wallet_id) REFERENCES `wallets`(id)
            );
        """
        db.execute_query(query_create_table)
