from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .integrators import simulate
from .scenario import create_new_planets

IMAGE_PATH = Path(__file__).resolve().parent.parent / 'space.jpg'
DT = 0.05
FRAMES_NUM = 10000        # Frames before the run resets
BOUNDS = 10               # Viewport half-width; planets beyond this count as out of bounds
OUT_OF_BOUNDS_LIMIT = 3   # Reset once this many planets are out of bounds
TRAIL_LENGTH = 800        # Orbit points kept for planets (gainsboro uses 200)
TRAIL_TRIM = 18           # Newest points hidden from each orbit trail


class Simulation:
    """Owns the figure, the planets, and the FuncAnimation that drives them."""

    def __init__(self, method='euler'):
        self.method = method
        self.fig, self.ax = plt.subplots(figsize=(4, 9))
        self.ax.set_facecolor('black')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-BOUNDS, BOUNDS)
        self.ax.set_ylim(-BOUNDS, BOUNDS)
        img = mpimg.imread(IMAGE_PATH)
        self.ax.imshow(img, extent=[-BOUNDS, BOUNDS, -BOUNDS, BOUNDS], aspect='auto')

        self.planets = create_new_planets()
        self.scatter_points = []
        self.orbit_lines = []
        self.ani = None

    def start(self):
        self.ani = FuncAnimation(
            self.fig, self.animate, frames=FRAMES_NUM + 1,
            interval=10, repeat=False,
        )

    def reset(self):
        self.planets.clear()
        self.ani.event_source.stop()
        self.planets.extend(create_new_planets())
        self.start()

    def animate(self, frame):
        if frame == FRAMES_NUM:
            print("Max frames reached. Resetting...")
            self.reset()

        simulate(self.planets, DT, self.method)

        for scatter in self.scatter_points:
            scatter.remove()  # This clears previous scatter points
        for line in self.orbit_lines:
            line.remove()  # This clears previous orbit lines
        self.scatter_points.clear()
        self.orbit_lines.clear()

        oob = 0
        for planet in self.planets:
            if planet.color != 'gainsboro' and (
                planet.x > BOUNDS or planet.x < -BOUNDS or planet.y > BOUNDS or planet.y < -BOUNDS
            ):
                oob += 1
            orbit = planet.orbit_euler if self.method == 'euler' else planet.orbit_rk
            scatter = self.ax.scatter(planet.x, planet.y, color=planet.color, s=planet.radius, zorder=2)
            self.scatter_points.append(scatter)
            xs, ys = (list(c) for c in zip(*orbit))
            if planet.color == 'gainsboro':
                fade_length = max(0, len(xs) - 200)
            else:
                fade_length = max(0, len(xs) - TRAIL_LENGTH)
            orbit_line, = self.ax.plot(
                xs[fade_length:-TRAIL_TRIM], ys[fade_length:-TRAIL_TRIM],
                color=planet.line_color, linewidth=1, zorder=1, alpha=0.2,
            )
            self.orbit_lines.append(orbit_line)

        if oob == OUT_OF_BOUNDS_LIMIT:
            print("All planets are out of bounds. Resetting...")
            self.reset()
