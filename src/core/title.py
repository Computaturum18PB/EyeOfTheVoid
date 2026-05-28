from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Slot
from utils.data_reader import get_title_tab_data
from utils.language_settings import lm
from core.environment_variables import FONT_NAME_H1, FONT_SIZE_H1, FONT_NAME_NORMAL, FONT_SIZE_NORMAL

class Title(QWidget):
    def __init__(self, path_content_tabs):
        super().__init__()
        self.path_content_tabs = path_content_tabs
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        title_font = QFont(FONT_NAME_H1, FONT_SIZE_H1)
        title_font.setItalic(True)
        
        normal_font = QFont(FONT_NAME_NORMAL, FONT_SIZE_NORMAL)
        
        self.title = QLabel()
        self.title.setFont(title_font)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignTop)
        
        self.description = QLabel()
        self.description.setFont(normal_font)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignTop)
        
        layout.addWidget(self.title, 0, 0)
        layout.addWidget(self.description, 0, 1)

        lm.language_changed.connect(self.update_content)

        self.update_content()
    
    @Slot()
    def update_content(self):
        new_list_data = get_title_tab_data(self.path_content_tabs)
        self.title.setText(new_list_data[0])
        self.description.setText(new_list_data[1])