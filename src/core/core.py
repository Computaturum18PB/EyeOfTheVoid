from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Slot
from core.solar_system import SolarSystem
from core.title import Title
from utils.data_reader import get_tab_name
from utils.language_settings import lm

class CoreWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.path_content_tabs = "EyeOfTheVoid/src/data/contants.json"
        self.path_app_icon = "EyeOfTheVoid/src/core/assets/images/icon.ico"
        
        list_tabs = get_tab_name(self.path_content_tabs)
        
        self.showMaximized()
        self.setWindowTitle("Eye of the void")
        self.setWindowIcon(QIcon(QPixmap(self.path_app_icon)))
        
        self.title = Title(self.path_content_tabs)
        self.solar_system = SolarSystem()
        
        self.addTab(self.title, list_tabs[0])
        self.addTab(self.solar_system, list_tabs[1])

        lm.language_changed.connect(self.update_content)
    
    @Slot()
    def update_content(self):
        new_list_tabs = get_tab_name(self.path_content_tabs)
        self.setTabText(0, new_list_tabs[0])
        self.setTabText(1, new_list_tabs[1])

        for i in range(self.count()):
            widget = self.widget(i)
            if hasattr(widget, "update_content"):
                widget.update_content()