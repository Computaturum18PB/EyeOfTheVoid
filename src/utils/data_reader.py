import json

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
    
def get_tab_name(path, current_language):
    try:
        data = read_file(path)
    except FileExistsError:
        print("Файл не существует!")
    
    list_tabs = data[current_language]["tabs"]
    return list_tabs

def get_title_tab_data(path, current_language):
    try:
        data = read_file(path)
    except FileExistsError:
        print("Файл не существует!")
        
    list_data = data[current_language]["title"]
    return list_data