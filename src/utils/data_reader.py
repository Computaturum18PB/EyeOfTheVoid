import json
from utils.language_settings import lm

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
    
def get_tab_name(path):
    try:
        data = read_file(path)
    except FileNotFoundError:
        print("Файл не существует!")
    
    list_tabs = data[lm.get_current_language()]["tabs"]
    return list_tabs

def get_title_tab_data(path):
    try:
        data = read_file(path)
    except FileNotFoundError:
        print("Файл не существует!")
        
    list_data = data[lm.get_current_language()]["title"]
    return list_data