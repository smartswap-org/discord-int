from DEXcryptoLib.Lib import *

def get_bot_config():
    """
    Function to get the bot_config.json configuration file
    """
    config = get_json_content("bot_config.json")
    if config == -1: 
        write_json("bot_config.json", {'token': '0x0', 'prefix': '$', 'discordid': '-1'})
        print(f"{'bot_config.json'} has been created.")
        return get_json_content("bot_config.json")
    return config 
    

def get_tmux_config():
    """
    Function to get the tmux_config.json configuration file
    """
    config = get_json_content("tmux_config.json")
    if config == -1: 
        write_json("tmux_config.json", {'example': 'color a'})
        print(f"{'tmux_config.json'} has been created.")
        return get_json_content("tmux_config.json")
    return config 
    
