from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from PySide6.QtGui import QFont

class Title(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        title_font = QFont("Verdana", 70)
        title_font.setItalic(True)
        
        self.title = QLabel("Приветствуем, ученые!")
        self.title.setFont(title_font)
        self.title.setWordWrap(True)
        
        layout.addWidget(self.title)