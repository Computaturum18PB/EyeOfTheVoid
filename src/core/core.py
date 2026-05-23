from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Slot
from core.solar_system import SolarSystem
from core.title import Title
from utils.data_reader import get_tab_name
from utils.language_settings import lm
from core.environment_variables import ICON_PATH, CONTENT_PATH, PROGRAMM_NAME

class CoreWindow(QTabWidget):
    def __init__(self):
        super().__init__()
                        
        list_tabs = get_tab_name(CONTENT_PATH)
        
        self.showMaximized()
        self.setWindowTitle(PROGRAMM_NAME)
        self.setWindowIcon(QIcon(QPixmap(ICON_PATH)))
        
        self.title = Title(CONTENT_PATH)
        self.solar_system = SolarSystem()
        
        self.addTab(self.title, list_tabs[0])
        self.addTab(self.solar_system, list_tabs[1])

        lm.language_changed.connect(self.update_content)
    
    @Slot()
    def update_content(self):
        new_list_tabs = get_tab_name(CONTENT_PATH)
        self.setTabText(0, new_list_tabs[0])
        self.setTabText(1, new_list_tabs[1])

        for i in range(self.count()):
            widget = self.widget(i)
            if hasattr(widget, "update_content"):
                widget.update_content()