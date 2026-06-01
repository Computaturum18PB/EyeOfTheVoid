from PySide6.QtWidgets import QApplication
from core.core import CoreWindow
from core.environment_variables import STYLES_PATH
from core.load import LoadWindow
from core.protector import ProtectorWindow

def load_stylesheet(app):
    try:
        with open(STYLES_PATH, "r", encoding="utf-8") as file:
            style = file.read()
            app.setStyleSheet(style)
    except Exception:
        print("Ошибка загрузки стилей!")

def main():
    app = QApplication([])
    
    load_stylesheet(app)

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