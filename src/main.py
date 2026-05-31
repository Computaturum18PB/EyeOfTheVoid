from PySide6.QtWidgets import QApplication
from core.core import CoreWindow
from core.load import LoadWindow
from core.protector import ProtectorWindow

def main():
    app = QApplication([])

    protector = ProtectorWindow()
    if not protector.exec():
        return 

    load = LoadWindow()
    load.show()
    app.processEvents()

    window = CoreWindow()
    
    load.close()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()