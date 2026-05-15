from PySide6.QtCore import Slot

class Language_master:
    __current_language = "ru"
        
    @staticmethod
    def get_current_language():
        return Language_master.__current_language

    @staticmethod
    def set_current_language():
        match Language_master.__current_language:
            case "ru":
                Language_master.__current_language = "en"
            case "en":
                Language_master.__current_language = "ru"               
          
lm = Language_master