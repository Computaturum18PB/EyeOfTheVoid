import random
from PySide6.QtGui import QFont
from utils.language_master import lm
import json
import pyqtgraph.opengl as gl
import math
import numpy as np
from core.environment_variables import FONT_NAME_NORMAL, FONT_SIZE_NORMAL

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

def get_star(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        match lm.get_current_language():
            case "Русский":
                star = data["Русский"]["Звезда"]
            case "English":
                star = data["English"]["Star"]
        return star
    
def get_star_name(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        match lm.get_current_language():
            case "Русский":
                name = data["Русский"]["Звезда"]["Название"]
            case "English":
                name = data["English"]["Star"]["Name"]
        return name

def get_planets(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        match lm.get_current_language():
            case "English":
                list_planets = data["English"]["Planets"]  
            case "Русский":
                list_planets = data["Русский"]["Планеты"]
        return list_planets

def create_satellite(sat_data, parent_planet_item, view):
    match lm.get_current_language():
        case "Русский":
            name = sat_data["Название"]
            radius = sat_data["Модельный_радиус"]
            orbit_radius = sat_data["Модельный_радиус_орбиты"]
            speed = sat_data["Скорость_км_с"] / 100
            color = sat_data["Модельный_цвет"]
        case "English":
            name = sat_data["Name"]
            radius = sat_data["Model_radius"]
            orbit_radius = sat_data["Model_orbit_radius"]
            speed = sat_data["Speed_kms"] / 100
            color = sat_data["Model_color"]

    sat_item = gl.GLScatterPlotItem(
        pos=[0, 0, 0],
        color=color,
        size=radius
    )
    view.addItem(sat_item)

    orbit_points = []
    segments = 100
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = orbit_radius * math.cos(angle)
        z = orbit_radius * math.sin(angle)
        orbit_points.append([x, 0, z])
    
    orbit_line = gl.GLLinePlotItem(
        pos=np.array(orbit_points),
        color=(0.6, 0.6, 0.6, 0.5),
        width=1
    )
    view.addItem(orbit_line)

    label = gl.GLTextItem(
        text=name,
        pos=np.array([0, 0, 0]),
        font=QFont("Arial", 8),
        color=(0.8, 0.8, 0.8, 1)
    )
    view.addItem(label)
    
    return {
        "name": name,
        "item": sat_item,
        "orbit": orbit_line,
        "label": label,
        "parent": parent_planet_item,
        "orbit_radius": orbit_radius,
        "speed": speed,
        "angle": random.uniform(0, 2 * math.pi),
        "color": color
    }

def create_star(path):
    star_data = get_star(path)
    match lm.get_current_language():
        case "Русский":
            size = star_data["Модельный_радиус"]
            color = star_data["Модельный_цвет"]
        case "English":
            size = star_data["Model_radius"]
            color = star_data["Model_color"]
    return gl.GLScatterPlotItem(pos=[0, 0, 0], color=color, size=size)

def update_text_planet(self):
    for planet_data in self.planets_data:
        old_description = planet_data["description"]
        self.view.removeItem(old_description)

        new_description = gl.GLTextItem(
            text=planet_data.get("name", "Planet"),
            pos=np.array([0, 0, 0]),
            font=QFont("Arial", 10)
        )
        self.view.addItem(new_description)
        planet_data["description"] = new_description

def update_names_planets(path, planets_data):
    planets_list = get_planets(path)
    for i, planet_data in enumerate(planets_data):
        match lm.get_current_language():
            case "English":
                planet_data["name"] = planets_list[i]["Name"]
            case "Русский":
                planet_data["name"] = planets_list[i]["Название"]

def create_planets_objects(path, view):
    planets_list = get_planets(path)
    planets_data = []
    all_satellites = []
        
    for planet in planets_list:
        match lm.get_current_language():
            case "Русский":
                name = planet["Название"]
                orbit_radius = planet["Модельный_радиус_орбиты"]
                size = planet["Модельный_радиус"]
                eccentricity = planet["Эксцентриситет_орбиты"]
                inclination = math.radians(planet["Наклон_орбиты_градусов"])
                speed = planet["Модельная_скорость"]
                color = planet["Модельный_цвет"]
                satellites_data = planet.get("Спутники", [])
            case "English":
                name = planet["Name"]
                orbit_radius = planet["Model_orbit_radius"]
                size = planet["Model_radius"]
                eccentricity = planet["Orbit_eccentricity"]
                inclination = math.radians(planet["Orbit_inclination_degrees"])
                speed = planet["Model_speed"]
                color = planet["Model_color"]
                satellites_data = planet.get("Satellites", [])

        angle = random.uniform(0, 2 * math.pi)

        r = orbit_radius * (1 - eccentricity**2) / (1 + eccentricity * math.cos(angle))
        x = r * math.cos(angle)
        z = r * math.sin(angle) * math.cos(inclination)
        y = x * math.sin(inclination)

        planet_item = gl.GLScatterPlotItem(
            pos=[x, y, z],
            color=color,
            size=size
        )
        view.addItem(planet_item)
        
        description_item = gl.GLTextItem(
            text=name,
            pos=np.array([x+7, y+7, z+7]),
            font=QFont(FONT_NAME_NORMAL, FONT_SIZE_NORMAL)
        )
        view.addItem(description_item)
        
        planet_obj = {
            "name": name,
            "item": planet_item,
            "description": description_item,
            "orbit_radius": orbit_radius,
            "eccentricity": eccentricity,
            "inclination": inclination,
            "speed": speed,
            "angle": angle,
            "color": color,
            "size": size,
            "satellites": [],
            "x": x,
            "y": y,
            "z": z
        }

        for sat_data in satellites_data:
            satellite = create_satellite(sat_data, planet_item, view)
            planet_obj["satellites"].append(satellite)
            all_satellites.append(satellite)
        
        planets_data.append(planet_obj)

    return planets_data, all_satellites

def update_satellites(satellites, planets_data):
    for sat in satellites:
        sat["angle"] += sat["speed"]
        
        parent = None
        for planet in planets_data:
            if planet["item"] is sat["parent"]:
                parent = planet
                break
            
        parent_x = parent["x"]
        parent_y = parent["y"]
        parent_z = parent["z"]

        sat_x = parent_x + sat["orbit_radius"] * math.cos(sat["angle"])
        sat_z = parent_z + sat["orbit_radius"] * math.sin(sat["angle"])

        sat["item"].setData(pos=[sat_x, parent_y, sat_z])
        
        orbit_points = []
        segments = 100
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = parent_x + sat["orbit_radius"] * math.cos(angle)
            z = parent_z + sat["orbit_radius"] * math.sin(angle)
            orbit_points.append([x, parent_y, z])

        sat["orbit"].setData(pos=np.array(orbit_points))

        sat["label"].setData(pos=np.array([sat_x, parent_y, sat_z]))

def create_planet_orbit(planet_data):
    a = planet_data["orbit_radius"]
    e = planet_data["eccentricity"]
    inclination = planet_data["inclination"]
    
    orbit_points = []
    segments = 360
    
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        
        r = a * (1 - e**2) / (1 + e * math.cos(angle))

        x_orbit = r * math.cos(angle)
        z_orbit = r * math.sin(angle)

        y = x_orbit * math.sin(inclination)
        z = z_orbit * math.cos(inclination)
        x = x_orbit
        
        orbit_points.append([x, y, z])
    
    return np.array(orbit_points)

def create_all_orbits(planets_data):
    orbits = []
    for planet_data in planets_data:
        orbit_points = create_planet_orbit(planet_data)
        orbit_line = gl.GLLinePlotItem(
            pos=orbit_points,
            color=(0.5, 0.5, 0.5, 0.7),
            width=1
        )
        orbits.append(orbit_line)
    return orbits