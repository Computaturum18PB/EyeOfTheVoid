from PySide6.QtCore import Slot

class language_master:
    current_language = "ru"
        
    @staticmethod
    def get_current_language():
        return language_master.current_language

    @staticmethod
    @Slot()
    def set_current_language():
        match language_master.current_language:
            case "ru":
                language_master.current_language = "en"
            case "en":
                language_master.current_language = "ru"
        print(language_master.current_language)                