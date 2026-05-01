from PySide6.QtWidgets import QApplication
from core.core import CoreWindow

def main():
    app = QApplication([])
    window = CoreWindow()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()