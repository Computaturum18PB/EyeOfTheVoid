import random

from utils.language_settings import lm
import json
import pyqtgraph.opengl as gl
import math
import numpy as np

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

def get_planets(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        match lm.get_current_language():
            case "English":
                list_planets = data["English"]["Planets"]  
            case "Русский":
                list_planets = data["Русский"]["Планеты"]
        return list_planets
    
def get_satellites(path):
    list_planets = get_planets(path)
    list_satellites = []
    match lm.get_current_language():
        case "Русский":
            for planet in list_planets:
                list_satellites.append(planet["Спутники"])
        case "English":
            for planet in list_planets:
                list_satellites.append(planet["Satellites"])
    return list_satellites

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

def create_planets_objects(path, view):
    planets_list = get_planets(path)
    planets_data = []
    
    for planet in planets_list:
        match lm.get_current_language():
            case "Русский":
                name = planet["Название"]
                orbit_radius = planet["Модельный_радиус_орбиты"]
                size = planet["Модельный_радиус"]
                eccentricity = planet["Эксцентриситет_орбиты"]
                inclination = math.radians(planet["Наклон_орбиты_градусов"])
                speed = planet["Модельная_скорость"]
                color = planet.get("Модельный_цвет", (0.3, 0.6, 1.0, 1.0))
            case "English":
                name = planet["Name"]
                orbit_radius = planet["Model_orbit_radius"]
                size = planet["Model_radius"]
                eccentricity = planet["Orbit_eccentricity"]
                inclination = math.radians(planet["Orbit_inclination_degrees"])
                speed = planet["Model_speed"]
                color = planet.get("Model_color", (0.3, 0.6, 1.0, 1.0))

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
        
        planets_data.append({
            "name": name,
            "item": planet_item,
            "orbit_radius": orbit_radius,
            "eccentricity": eccentricity,
            "inclination": inclination,
            "speed": speed,
            "angle": angle,
            "color": color,
            "size": size
        })
    
    return planets_data

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