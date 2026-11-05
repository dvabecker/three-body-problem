import math
import random

from .planet import Planet


def create_new_planets():
    """Return three planets on a circle with tangential starting velocities."""
    circle_radius = 3
    num_planets = 3
    theta = 2 * math.pi / num_planets  # Angle between planets (120 degrees for 3 planets)
    colors = ["indianred", "powderblue", "greenyellow"]
    line_colors = ["lightcoral", "paleturquoise", "palegreen"]

    planets = []
    for i in range(num_planets):
        angle = i * theta
        x = circle_radius * math.cos(angle)
        y = circle_radius * math.sin(angle)

        # Initial velocities directed tangentially
        vx = -math.sin(angle)
        vy = math.cos(angle)

        planet = Planet(x + random.randint(-100, 100) / 100, y, 100, colors[i], line_colors[i], 1, vx * 0.4, vy * 0.4)
        planets.append(planet)

        # Optional fourth body (fixed "earth" that exerts no force on others):
        # earth = Planet(0, 0, 20, 'gainsboro', 'whitesmoke', 0.5, 0, 0.4)
        # planets.append(earth)
    return planets
