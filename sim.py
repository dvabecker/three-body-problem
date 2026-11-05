"""Entry point: run the three-body animation with `python sim.py`."""
import matplotlib.pyplot as plt

from three_body.animation import Simulation


def main():
    sim = Simulation(method='euler')  # or 'runge_kutta'
    sim.start()
    plt.show()


if __name__ == '__main__':
    main()
