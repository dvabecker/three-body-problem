from .physics import calculate_total_force, update_position, update_velocity, gravitational_force


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


def simulate(planets, dt, method):
    if method == 'euler':
        for planet in planets:
            euler_step(planet, dt, planets)
    elif method == 'runge_kutta':
        for planet in planets:
            runge_kutta_step(planet, dt, planets)
