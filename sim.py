import math
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

class Planet:
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

def update_position(planet, dt):
    planet.x += planet.vx * dt
    planet.y += planet.vy * dt

def update_velocity(planet, force, dt):
    ax = force[0] / planet.mass
    ay = force[1] / planet.mass
    planet.vx += ax * dt
    planet.vy += ay * dt
    
    # Set maximum velocity and damping factor
    max_velocity = 3
    damping_factor = 0.99  # Adjust this value to control how quickly velocity decreases (0 < damping_factor < 1)

    # Calculate the current velocity magnitude
    velocity_magnitude = math.sqrt(planet.vx**2 + planet.vy**2)

    # Check if the velocity exceeds the maximum allowed velocity
    if velocity_magnitude > max_velocity:
        # Apply damping to reduce the velocity gradually
        planet.vx *= damping_factor
        planet.vy *= damping_factor

        # Limit the velocity to the maximum value
        scaling_factor = max_velocity / velocity_magnitude
        planet.vx *= scaling_factor
        planet.vy *= scaling_factor

def gravitational_force(planet1, planet2):

    if planet2.color == 'gainsboro':
        return (0, 0)

    max_G = 5
    min_G = -max_G
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    distance_squared = dx**2 + dy**2
    distance = math.sqrt(distance_squared)
    if distance == 0:
        return (0, 0)
    if (distance > 12):
        G = 0.3*distance
    else:
        G = 1.2
    force_magnitude = G * planet1.mass * planet2.mass / distance_squared
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance

    return (max(min(max_G, force_x), min_G), max(min(max_G, force_y), min_G))
    
def euler_step(planet, dt, planets):
    for planet in planets:
        net_force = [0, 0]
        for other_planet in planets:
            if planet != other_planet:
                force = gravitational_force(planet, other_planet)
                net_force[0] += force[0]
                net_force[1] += force[1]

        update_velocity(planet, net_force, dt)
    for planet in planets:
        update_position(planet, dt)
        planet.orbit_euler.append((planet.x, planet.y))
    

def runge_kutta_step(planet, dt, planets):
    # Backup the original velocities and positions
    vx_backup, vy_backup = planet.vx, planet.vy
    x_backup, y_backup = planet.x, planet.y

    # Calculate forces at the initial position
    initial_force = calculate_total_force(planet, planets)

    # Update velocity using Runge-Kutta method
    k1x, k1y = initial_force[0] / planet.mass, initial_force[1] / planet.mass
    planet.vx = vx_backup + k1x * dt / 2
    planet.vy = vy_backup + k1y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    second = calculate_total_force(planet, planets)
    k2x, k2y = second[0] / planet.mass, second[1] / planet.mass
    planet.vx = vx_backup + k2x * dt / 2
    planet.vy = vy_backup + k2y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    third = calculate_total_force(planet, planets)
    k3x, k3y = third[0] / planet.mass, third[1] / planet.mass
    planet.vx = vx_backup + k3x * dt / 2
    planet.vy = vy_backup + k3y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    last = calculate_total_force(planet, planets)
    k4x, k4y = last[0] / planet.mass, last[1] / planet.mass

    planet.vx = vx_backup + (k1x + 2 * k2x + 2 * k3x + k4x) * dt / 6
    planet.vy = vy_backup + (k1y + 2 * k2y + 2 * k3y + k4y) * dt / 6

    # Update position
    update_position(planet, dt)

    # Append the updated position to the orbit
    planet.orbit_rk.append((planet.x, planet.y))

def calculate_total_force(planet, planets):
    total_force = [0, 0]
    for other_planet in planets:
        if planet != other_planet:
            force_component = gravitational_force(planet, other_planet)
            total_force[0] += force_component[0]
            total_force[1] += force_component[1]
    return total_force

def simulate(planets, dt, method):
    if method == 'euler':
        for planet in planets:
            euler_step(planet, dt, planets)
    elif method == 'runge_kutta':
        for planet in planets:
            runge_kutta_step(planet, dt, planets)

def animate(frame, planets, ax, method, scatter_points, orbit_lines):

    if (frame == FRAMES_NUM):
        print("Max frames reached. Resetting...")
        planets.clear()
        ani.event_source.stop()
        new_planets = create_new_planets()
        planets.extend(new_planets)
        start_animation()

    dt = 0.05
    oob = 0
    simulate(planets, dt, method)
    
    for scatter in scatter_points:
        scatter.remove()  # This clears previous scatter points
    for line in orbit_lines:
        line.remove()  # This clears previous orbit lines
        
    scatter_points.clear()
    orbit_lines.clear()
    
    for planet in planets:                
        if (planet.color != 'gainsboro' and (planet.x > 10 or planet.x < -10 or planet.y > 10 or planet.y < -10)):
            oob += 1
        orbit = planet.orbit_euler if method == 'euler' else planet.orbit_rk
        scatter = ax.scatter(planet.x, planet.y, color=planet.color, s=planet.radius, zorder=2)
        scatter_points.append(scatter)
        updated_points = list(zip(*orbit))
        if (planet.color == 'gainsboro'):
            fade_length = max(0, len(updated_points[0])-200)
        else:
            fade_length = max(0, len(updated_points[0])-800)
        orbit_line, = ax.plot(updated_points[0][fade_length:-18], updated_points[1][fade_length:-18], color=planet.line_color, linewidth=1, zorder=1, alpha=0.2)
        orbit_lines.append(orbit_line)
    
    if (oob == 3):
        print("All planets are out of bounds. Resetting...")
        planets.clear()
        ani.event_source.stop()
        new_planets = create_new_planets()
        planets.extend(new_planets)
        start_animation()

def create_new_planets():
    # Create instances of Planet with initial coordinates and velocities
    # Circle parameters
    circle_radius = 3
    num_planets = 3
    theta = 2 * math.pi / num_planets  # Angle between planets (120 degrees for 3 planets)
    colors = ["indianred", "powderblue", "greenyellow"]
    line_colors = ["lightcoral", "paleturquoise", "palegreen"]

    # Create instances of Planet with initial coordinates and velocities
    planets = []
    for i in range(num_planets):
        angle = i * theta
        x = circle_radius * math.cos(angle)
        y = circle_radius * math.sin(angle)
        
        # Initial velocities directed tangentially
        vx = -math.sin(angle)  # Tangential velocity (in the negative y direction)
        vy = math.cos(angle)   # Tangential velocity (in the positive x direction)

        planet = Planet(x + random.randint(-100,100)/100, y, 100, colors[i], line_colors[i], 1, vx*0.4, vy*0.4)
        planets.append(planet)
        
        #earth = Planet(0, 0, 20, 'gainsboro', 'whitesmoke', 0.5, 0, 0.4)
        #planets.append(earth)
    return planets

# Set up the animation
fig, ax = plt.subplots(figsize=(4,9))
ax.set_facecolor('black')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
img = mpimg.imread('space.jpg')  # Replace with your image file
ax.imshow(img, extent=[-10, 10, -10, 10], aspect='auto')

planets = create_new_planets()
# select 'euler' or 'runge_kutta'
# Create a reference to the animation object so we can restart it later if needed
ani = None
scatter_points = []
orbit_lines = []
FRAMES_NUM = 10000

def start_animation():
    global ani
    ani = FuncAnimation(fig, animate, frames=FRAMES_NUM+1, fargs=(planets, ax, 'euler', scatter_points, orbit_lines), interval=10, repeat=False)

# Start the animation for the first time
start_animation()

# Show the animation
plt.show()