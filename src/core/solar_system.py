from PySide6.QtWidgets import QHBoxLayout, QWidget, QTextEdit
from PySide6.QtCore import QTimer
import numpy as np
import math
import pyqtgraph.opengl as gl
from utils.solar_system import create_star, create_planets_objects, create_all_orbits, get_planets
from core.environment_variables import SOLAR_SYSTEM_PATH, RUSSIAN_BLOCK_LIST, ENGLISH_BLOCK_LIST, UNKNOWN_TYPE

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
            
    def format_value(self, value, indent=0):
        lines = []
        spaces = " " * indent
        
        match value:
            case str() | int() | float():
                lines.append(f"{spaces}{value}")    
            case list():
                for item in value:
                    lines.extend(self.format_value(item, indent + 4))
            case dict():
                for k, v in value.items():
                    formatted_k = k.replace("_", " ")
                    if isinstance(v, (str, int, float)):
                        lines.append(f"{spaces}{formatted_k}: {v}")
                    else:
                        lines.append(f"{spaces}{formatted_k}:")
                        lines.extend(self.format_value(v, indent + 4))        
            case _:
                lines.append(f"{spaces}{UNKNOWN_TYPE}")
        return lines

    def create_description(self, index):
        planet = self.planets_list[index]
        description_lines = []
        
        for key, value in planet.items():
            formatted_key = key.replace("_", " ")

            if any(block in formatted_key for block in RUSSIAN_BLOCK_LIST) or \
            any(block in formatted_key for block in ENGLISH_BLOCK_LIST):
                continue
            
            if isinstance(value, (str, int, float)):
                description_lines.append(f"{formatted_key}: {value}")
            else:
                description_lines.append(f"{formatted_key}:")
                description_lines.extend(self.format_value(value, 4))
        
        text = "\n".join(description_lines)
        self.description.append(text)