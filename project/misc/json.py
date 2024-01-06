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

def write_json(filerep, content):
    """
    Fonction to write in a json file.

    Tip : If you want to add a line, you need to get the current content then 
    add what you want and write the new content using this fonction.
    """
    with open(filerep, 'w') as file:
        json.dump(content, file, indent=4)

