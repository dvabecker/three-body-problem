import math


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
    if distance > 12:
        G = 0.3 * distance
    else:
        G = 1.2
    force_magnitude = G * planet1.mass * planet2.mass / distance_squared
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance

    return (max(min(max_G, force_x), min_G), max(min(max_G, force_y), min_G))


def calculate_total_force(planet, planets):
    total_force = [0, 0]
    for other_planet in planets:
        if planet != other_planet:
            force_component = gravitational_force(planet, other_planet)
            total_force[0] += force_component[0]
            total_force[1] += force_component[1]
    return total_force
