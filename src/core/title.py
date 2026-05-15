from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot
from utils.data_reader import get_title_tab_data
from utils.language_settings import lm

class Title(QWidget):
    def __init__(self):
        super().__init__()
        
        list_data = get_title_tab_data("EyeOfTheVoid/src/data/contants.json")
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        title_font = QFont("Verdana", 70)
        title_font.setItalic(True)
        
        self.title = QLabel(list_data[0])
        self.title.setFont(title_font)
        self.title.setWordWrap(True)
                  
        self.language_button = QPushButton(lm.get_current_language())
        self.language_button.clicked.connect(self.update_content)
        
        layout.addWidget(self.title, 1, 0)
        layout.addWidget(self.language_button, 0, 0)   
    
    @Slot()
    def update_content(self):
        lm.set_current_language()
        self.language_button.setText(lm.get_current_language())