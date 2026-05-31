from PySide6.QtWidgets import QLabel, QMenu, QTabWidget, QWidget, QMenuBar, QStatusBar, QMainWindow
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtCore import Slot
from core.solar_system import SolarSystem
from core.title import Title
from core.music_player import MediaPlayer
from utils.data_reader import get_tab_name, get_menu_section_data, get_status, get_status_temporary
from utils.language_master import lm
from utils.speed_master import sp
from core.environment_variables import ICON_PATH, CONTENT_PATH, PROGRAMM_NAME

class CoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle(PROGRAMM_NAME)
        self.setWindowIcon(QIcon(QPixmap(ICON_PATH)))
        
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        self.app_status = QLabel()
        self.status.addPermanentWidget(self.app_status)
        
        self.version = QLabel()
        self.status.addPermanentWidget(self.version)
        
        start_status = get_status_temporary(CONTENT_PATH, "start", 0)
        self.status.showMessage(start_status[0], start_status[1])
        
        list_menu_section_1 = get_menu_section_data(CONTENT_PATH, 1)
        
        self.language_menu = self.menu.addMenu(list_menu_section_1[0])
        
        self.set_language = self.language_menu.addAction(list_menu_section_1[1])
        self.set_language.triggered.connect(lm.change_language)
        
        list_menu_section_2 = get_menu_section_data(CONTENT_PATH, 2)
        
        self.solar_system_menu = QMenu(list_menu_section_2[0], self)
        self.menu.addMenu(self.solar_system_menu)
        self.solar_system_menu.setEnabled(False)
        
        self.increase_speed = QAction(list_menu_section_2[2], self)
        self.decrease_speed = QAction(list_menu_section_2[3], self)
        
        self.increase_speed.triggered.connect(sp.fast_speed)
        self.decrease_speed.triggered.connect(sp.real_speed)
        
        self.solar_system_menu.addActions([self.increase_speed, self.decrease_speed])
        
        list_tabs = get_tab_name(CONTENT_PATH)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)   
        
        self.title = Title(CONTENT_PATH)
        self.solar_system = SolarSystem()
        self.music_player = MediaPlayer()
        
        self.tabs.addTab(self.title, list_tabs[0])
        self.tabs.addTab(self.solar_system, list_tabs[1])
        self.tabs.addTab(self.music_player, list_tabs[2])

        lm.language_changed.connect(self.update_content)
        self.tabs.currentChanged.connect(self.solar_system_active)
        
        self.increase_speed.triggered.connect(self.solar_system.change_speed)
        self.decrease_speed.triggered.connect(self.solar_system.change_speed)
        
        self.update_content()
        self.showMaximized()
        
    def solar_system_active(self, index):
        self.solar_system_menu.setEnabled(index == 1)
    
    @Slot()
    def update_content(self):
        new_list_tabs = get_tab_name(CONTENT_PATH)
        self.tabs.setTabText(0, new_list_tabs[0])
        self.tabs.setTabText(1, new_list_tabs[1])
        self.tabs.setTabText(2, new_list_tabs[2])
        
        new_list_section_1 = get_menu_section_data(CONTENT_PATH, 1)
        self.language_menu.setTitle(new_list_section_1[0])
        self.set_language.setText(new_list_section_1[1])
        
        new_list_section_2 = get_menu_section_data(CONTENT_PATH, 2)
        self.solar_system_menu.setTitle(new_list_section_2[0])
        self.increase_speed.setText(new_list_section_2[2])
        self.decrease_speed.setText(new_list_section_2[3])

        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, "update_content"):
                widget.update_content()
                
        app_status = get_status(CONTENT_PATH, "statuses")[0]
        self.app_status.setText(app_status)
        
        version = get_status(CONTENT_PATH, "parameters")[0]
        self.version.setText(version)
        
        localizate = get_status_temporary(CONTENT_PATH, "actions", 0)
        self.status.showMessage(localizate[0], localizate[1])