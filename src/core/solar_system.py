from PySide6.QtWidgets import QHBoxLayout, QWidget, QTextEdit
from PySide6.QtCore import QTimer
import numpy as np
import math
import pyqtgraph.opengl as gl
from utils.solar_system import create_star, create_planets_objects, create_all_orbits, get_planets

class SolarSystem(QWidget):
    def __init__(self): 
        super().__init__()
        self.path = "EyeOfTheVoid/src/data/solar_system.json"
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = gl.GLViewWidget()
        layout.addWidget(self.view)

        sun = create_star(self.path)
        self.view.addItem(sun)

        self.planets_list = get_planets(self.path)
        self.planets_data = create_planets_objects(self.path, self.view)
             
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
        planet = self.planets_list[index]
        for key in planet:
            self.description.append(f"{key}: {planet[key]}")