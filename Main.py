from PySide6.QtWidgets import QMainWindow, QApplication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("Eye of the void")     

app = QApplication([])
window = Window()
window.show()
app.exec()