import json

def write_json(filerep, content):
    """
    Fonction to write in a json file.

    Tip : If you want to add a line, you need to get the current content then 
    add what you want and write the new content using this fonction.
    """
    with open(filerep, 'w') as file:
        json.dump(content, file, indent=4)