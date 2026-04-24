from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon, QPixmap

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Eye of the void")
        self.setWindowIcon(QIcon(QPixmap("EyeOfTheVoid/app/images/icon.ico")))

app = QApplication([])
window = Window()
window.show()
app.exec()