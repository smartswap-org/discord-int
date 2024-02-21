# create_config_files dir
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# path were configs files are 
CONFIGS_DIR="$SCRIPT_DIR/../configs"

# create configs directory if he doesnt exist
mkdir -p "$CONFIGS_DIR"

# overwrite files if needed (usefull to create the config files)
create_or_overwrite_file() {
    local file=$1
    local content=$2
    if [ ! -f "$file" ]; then
        echo "$content" > "$file"
    else
        echo "$file already exists. Skipping creation."
    fi
}

# bot_config.json
bot_config_content='{
    "token": "your_token_id",
    "prefix": "!",
    "discordid": "123", 
    "logschannelid": "123",
    "roomscategid": "123"
}'
create_or_overwrite_file "$CONFIGS_DIR/bot_config.json" "$bot_config_content"

# db_config.json
db_config_content='{
    "host": "192.168.1.1",
    "user":"youruser",
    "pass":"yourpass"
}'
create_or_overwrite_file "$CONFIGS_DIR/db_config.json" "$db_config_content"

# git_config.json
create_or_overwrite_file "$CONFIGS_DIR/git_config.json" "{}"

# tmux_config.json
create_or_overwrite_file "$CONFIGS_DIR/tmux_config.json" "{}"
