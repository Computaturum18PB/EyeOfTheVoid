from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from PySide6.QtGui import QFont
from utils.data_reader import get_title_tab_data

class Title(QWidget):
    def __init__(self, current_language):
        super().__init__()
        
        list_data = get_title_tab_data("EyeOfTheVoid/src/data/contants.json", current_language)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        title_font = QFont("Verdana", 70)
        title_font.setItalic(True)
        
        self.title = QLabel(list_data[0])
        self.title.setFont(title_font)
        self.title.setWordWrap(True)
        
        layout.addWidget(self.title)