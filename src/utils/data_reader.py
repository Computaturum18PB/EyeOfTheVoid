import json
from utils.language_master import lm

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("The integrity of the software configuration files is compromised!")
    
def get_tab_name(path):
    data = read_file(path)
    list_tabs = data[lm.get_current_language()]["tabs"]
    return list_tabs

def get_title_tab_data(path):
    data = read_file(path)
    list_data = data[lm.get_current_language()]["title"]
    return list_data

def get_menu_section_data(path, section):
    data = read_file(path)
    match section:
        case 1:
            list_data = data[lm.get_current_language()]["menu"]["section_1"]
        case 2:
            list_data = data[lm.get_current_language()]["menu"]["section_2"]
    return list_data

def get_buttons_data(path):
    data = read_file(path)
    list_data = data[lm.get_current_language()]["buttons"]
    return list_data

def get_status(path, type):
    data = read_file(path)
    list_data = data[lm.get_current_language()]["status"][type]
    return list_data

def get_status_temporary(path, type, index):
    data = read_file(path)
    status_and_time = data[lm.get_current_language()]["status"][type][index]
    return status_and_time