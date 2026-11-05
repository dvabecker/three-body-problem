class Planet:
    """A body with position, velocity, and a separate orbit trace per integrator."""

    def __init__(self, x, y, radius, color, line_color, mass, vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.line_color = line_color
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.orbit_euler = [(x, y)]  # Separate orbits for Euler and Runge-Kutta methods
        self.orbit_rk = [(x, y)]
