from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon, QPixmap
from core.solar_system import SolarSystem

class CoreWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.showMaximized()
        self.setWindowTitle("Eye of the void")
        self.setWindowIcon(QIcon(QPixmap("EyeOfTheVoid/core/source/images/icon.ico")))
        
        self.solar_system = SolarSystem()
        self.addTab(self.solar_system, "Солнечная система")