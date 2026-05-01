from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon, QPixmap
from core.solar_system import SolarSystem
from core.title import Title
from utils.data_reader import get_tab_name

class CoreWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.current_language = "ru"
        
        list_tabs = get_tab_name("EyeOfTheVoid/src/data/contatnts.json", self.current_language)
        
        self.showMaximized()
        self.setWindowTitle("Eye of the void")
        self.setWindowIcon(QIcon(QPixmap("EyeOfTheVoid/src/core/assets/images/icon.ico")))
        
        self.title = Title()
        self.solar_system = SolarSystem()
        
        self.addTab(self.title, list_tabs[0])
        self.addTab(self.solar_system, list_tabs[1])
        