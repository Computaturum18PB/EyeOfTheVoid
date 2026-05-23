from PySide6.QtWidgets import QHBoxLayout, QWidget, QTextEdit
from PySide6.QtCore import QTimer
import numpy as np
import math
import pyqtgraph.opengl as gl
from utils.solar_system import create_star, create_planets_objects, create_all_orbits, get_planets
from core.environment_variables import SOLAR_SYSTEM_PATH

class SolarSystem(QWidget):
    def __init__(self): 
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = gl.GLViewWidget()
        layout.addWidget(self.view)

        sun = create_star(SOLAR_SYSTEM_PATH)
        self.view.addItem(sun)

        self.planets_list = get_planets(SOLAR_SYSTEM_PATH)
        self.planets_data = create_planets_objects(SOLAR_SYSTEM_PATH, self.view)
             
        self.description = QTextEdit()
        self.description.setFixedWidth(300)
        self.description.setReadOnly(True)
        layout.addWidget(self.description)
        
        self.create_description(0)

        orbits = create_all_orbits(self.planets_data)
        for orbit in orbits:
            self.view.addItem(orbit)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_planets)
        self.timer.start(16)
    
    def get_planet_position(self, planet_data, angle):
        a = planet_data["orbit_radius"]
        e = planet_data["eccentricity"]
        inclination = planet_data["inclination"]

        r = a * (1 - e**2) / (1 + e * math.cos(angle))

        x_orbit = r * math.cos(angle)
        z_orbit = r * math.sin(angle)

        y = x_orbit * math.sin(inclination)
        z = z_orbit * math.cos(inclination)
        x = x_orbit
        
        return [x, y, z]
    
    def update_planets(self):
        for planet_data in self.planets_data:
            planet_data["angle"] += planet_data["speed"]
            
            x, y, z = self.get_planet_position(planet_data, planet_data["angle"])

            planet_data["item"].setData(pos=[x, y, z])
            
    def create_description(self, index):
        russian_block_list = ["Модельный", "Модельное", "Модельная", "Модельные"]
        english_block_list = ["Model"]
        planet = self.planets_list[index]
        description_lines = []
        
        for key, value in planet.items():
            formatted_key = key.replace("_", " ")
            if not(any(block in formatted_key for block in russian_block_list) | any(block in formatted_key for block in english_block_list)):
                match value:
                    case str() | int() | float():
                        description_lines.append(f"{formatted_key}: {value}")
                    case list():
                        description_lines.append(f"{formatted_key}:")
                        for item in value:
                            description_lines.append(f"     {item}")
                    case dict():
                        description_lines.append(f"{formatted_key}:")
                        for sub_key, sub_value in value.items():
                            description_lines.append(f"     {sub_key}: {sub_value}")
                    case _:
                        description_lines.append("{UNKNOWN TYPE}")
        text = "\n".join(description_lines)
        
        self.description.append(text)