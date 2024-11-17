import json

def get_json_content(filerep):
    """
    Fonction to get json file content in a dic
    """
    try:
        with open(filerep, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return -1
    except json.JSONDecodeError:
        return -2 