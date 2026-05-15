from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot
from utils.data_reader import get_title_tab_data
from utils.language_settings import lm

class Title(QWidget):
    def __init__(self, path_content_tabs):
        super().__init__()
        self.path_content_tabs = path_content_tabs
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        title_font = QFont("Verdana", 70)
        title_font.setItalic(True)
        
        self.title = QLabel()
        self.title.setFont(title_font)
        self.title.setWordWrap(True)
                  
        self.language_button = QPushButton()
        self.language_button.clicked.connect(self.language_button_clicked)
        
        layout.addWidget(self.title, 1, 0)
        layout.addWidget(self.language_button, 0, 0)

        lm.language_changed.connect(self.update_content)

        self.update_content()
    
    @Slot()
    def language_button_clicked(self):
        lm.change_language()
    
    @Slot()
    def update_content(self):
        self.language_button.setText(lm.get_current_language())

        new_list_data = get_title_tab_data(self.path_content_tabs)
        self.title.setText(new_list_data[0])