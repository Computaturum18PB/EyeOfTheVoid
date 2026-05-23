from PySide6.QtWidgets import QApplication
from core.core import CoreWindow
from core.load import LoadWindow
import time

def main():
    app = QApplication([])
    
    load = LoadWindow()
    load.show()
    app.processEvents()

    window = CoreWindow()
    
    load.close()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()