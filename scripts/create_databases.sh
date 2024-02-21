# MySQL credentials
MYSQL_USER="root"
MYSQL_PASS="your_password"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"

# Database names
DB_NAMES=("smartswap" "smartswap_positions" "smartswap_data")

# Tables creation
WALLETS_TABLE_QUERY="
CREATE TABLE IF NOT EXISTS wallets (
    name VARCHAR(255) PRIMARY KEY,
    address VARCHAR(255),
    private_key VARCHAR(255),
    discord_chanmsglogs_id VARCHAR(255)
);"

CLIENTS_TABLE_QUERY="
CREATE TABLE IF NOT EXISTS clients (
    user CHAR(255) PRIMARY KEY,
    discord_user_id VARCHAR(255),
    password VARCHAR(32)
);"

WALLETS_ACCESS_TABLE_QUERY="
CREATE TABLE IF NOT EXISTS wallets_access (
    client_user CHAR(255),
    wallet_name VARCHAR(255),
    PRIMARY KEY (client_user, wallet_name),
    FOREIGN KEY (client_user) REFERENCES clients(user),
    FOREIGN KEY (wallet_name) REFERENCES wallets(name)
);"

# Create databases and grant privileges
for DB_NAME in "${DB_NAMES[@]}"; do
    mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
    mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO 'smartswap'@'$MYSQL_HOST';"
done

# Create tables
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" -e "USE smartswap; $WALLETS_TABLE_QUERY $CLIENTS_TABLE_QUERY $WALLETS_ACCESS_TABLE_QUERY"

echo "Databases and tables have been created successfully."
