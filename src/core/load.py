from PySide6.QtWidgets import QProgressBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from core.environment_variables import DIALOG_LOADING

class LoadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DIALOG_LOADING)
        self.setFixedSize(500, 300)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedWidth(300)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.progress)
        
        self.setLayout(layout)
        