from PySide6.QtCore import Slot, QObject, Signal

class Language_master(QObject):
    language_changed = Signal()
    __current_language = "Русский"
    
    @staticmethod
    def get_current_language():
        return Language_master.__current_language

    @staticmethod
    def set_current_language():
        match Language_master.__current_language:
            case "Русский":
                Language_master.__current_language = "English"
            case "English":
                Language_master.__current_language = "Русский"
    
    @Slot()
    def change_language(self):
        self.set_current_language()
        self.language_changed.emit()
        
lm = Language_master()