from PySide6.QtWidgets import QApplication
from core.core import CoreWindow
from core.load import LoadWindow
from core.protector import ProtectorWindow

def main():
    app = QApplication([])
    
    load_first = LoadWindow()
    load_first.show()
    app.processEvents()
    
    protector = ProtectorWindow()
    if not protector.exec():
        load_first.close()
        return 
    
    load_first.close()

    load_second = LoadWindow()
    load_second.show()
    app.processEvents()

    window = CoreWindow()
    
    load_second.close()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()