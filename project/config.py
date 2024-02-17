from DEXcryptoLib.Lib import *

def get_config(file_path, default_config):
    config = get_json_content(file_path)
    if config == -1:
        write_json(file_path, default_config)
        print(f"{file_path} has been created.")
        return default_config
    return config

def get_bot_config():
    return get_config("configs/bot_config.json", {'token': '0x0', 'prefix': '$', 'discordid': '-1', 'logschannelid': '-1', 'roomscategid': '-1'})

def get_git_config():
    return get_config("configs/git_config.json", {})

def get_tmux_config():
    return get_config("configs/tmux_config.json", {'example': 'color a'})
