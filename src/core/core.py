from PySide6.QtWidgets import QTabWidget, QMenuBar, QMainWindow
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Slot
from core.solar_system import SolarSystem
from core.title import Title
from utils.data_reader import get_tab_name, get_menu_section_data
from utils.language_settings import lm
from core.environment_variables import ICON_PATH, CONTENT_PATH, PROGRAMM_NAME

class CoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.showMaximized()
        self.setWindowTitle(PROGRAMM_NAME)
        self.setWindowIcon(QIcon(QPixmap(ICON_PATH)))
        
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        
        list_section_1 = get_menu_section_data(CONTENT_PATH, 1)
        
        self.language_menu = self.menu.addMenu(list_section_1[0])
        
        self.set_language = self.language_menu.addAction(list_section_1[1])
        self.set_language.triggered.connect(lm.change_language)
        
        list_tabs = get_tab_name(CONTENT_PATH)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)   
        
        self.title = Title(CONTENT_PATH)
        self.solar_system = SolarSystem()
        
        self.tabs.addTab(self.title, list_tabs[0])
        self.tabs.addTab(self.solar_system, list_tabs[1])

        lm.language_changed.connect(self.update_content)
        
        self.update_content()
    
    @Slot()
    def update_content(self):
        new_list_tabs = get_tab_name(CONTENT_PATH)
        self.tabs.setTabText(0, new_list_tabs[0])
        self.tabs.setTabText(1, new_list_tabs[1])
        
        new_list_section_1 = get_menu_section_data(CONTENT_PATH, 1)
        self.language_menu.setTitle(new_list_section_1[0])
        self.set_language.setText(new_list_section_1[1])

        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, "update_content"):
                widget.update_content()        