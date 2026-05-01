from PySide6.QtWidgets import QHBoxLayout, QWidget
import pyqtgraph.opengl as gl

class SolarSystem(QWidget):
    def __init__(self): 
        super().__init__()
        
        layout = QHBoxLayout(self)

        self.view = gl.GLViewWidget()
        
        layout.addWidget(self.view)
        
        sun = gl.GLScatterPlotItem(pos=[0, 0, 0], color=(255, 165, 0, 1), size=100)
        self.view.addItem(sun)
        