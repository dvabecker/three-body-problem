# Three-Body Problem

A small matplotlib animation of three planets orbiting each other under a simplified gravitational force. Each planet is pulled toward the others, the simulation runs frame by frame, and the animation resets with a new random start once the run ends.

## Requirements

- Python 3.14 (the pinned packages in `requirements.txt` ship wheels for it)
- The packages pinned in `requirements.txt` (matplotlib, numpy, Pillow, scipy, and their dependencies)

## Setup on Ubuntu

Ubuntu 26.04 ships Python 3.14 as `python3`, so you only need the venv module and Tk:

```bash
sudo apt install python3-venv python3-tk
cd three-body-problem
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `python3-tk` package provides the Tk window backend that matplotlib uses to show the animation.

If you prefer uv, the same environment can be made with:

```bash
uv venv -p 3.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

The virtual environment directory is ignored by git, so it stays local.

## Running

From the repository root:

```bash
python sim.py
```

A window opens showing the animation on a starfield background.

## How it works

- **Planets:** three `Planet` objects start on a circle of radius 3 at 120° apart, with a random horizontal offset of up to ±1 unit and a tangential initial velocity.
- **Forces:** `gravitational_force` computes the pull between each pair of planets. Each force component is clamped to ±5 to keep the motion stable.
- **Integration:** two integrators are available, `euler_step` and `runge_kutta_step`. The entry point uses Euler; to switch, change `Simulation(method='euler')` in `sim.py` to `Simulation(method='runge_kutta')`.
- **Speed limit:** velocities are capped at 3 units per step, with damping applied when the cap is exceeded.
- **Reset:** a new run starts after 10,000 frames, or when all three planets are outside the ±10 viewport.

## Code layout

```
sim.py                  Entry point: builds the Simulation and shows the window
space.jpg               Background image
requirements.txt        Pinned Python dependencies
three_body/
    __init__.py
    planet.py           Planet class (position, velocity, orbit traces)
    physics.py          Gravity, force and velocity updates
    integrators.py      Euler and Runge-Kutta steps, simulate()
    scenario.py         Creates the starting planets
    animation.py        Simulation class: figure, frame updates, reset logic
```

## Tuning

Constants are spread across the package:

| Setting | Location | Effect |
| --- | --- | --- |
| `DT` | `three_body/animation.py` | Time step per frame |
| `FRAMES_NUM`, `BOUNDS`, `OUT_OF_BOUNDS_LIMIT` | `three_body/animation.py` | Run length, viewport size, out-of-bounds reset threshold |
| `TRAIL_LENGTH`, `TRAIL_TRIM` | `three_body/animation.py` | Orbit trail length and trimmed tail |
| `max_velocity`, `damping_factor` | `three_body/physics.py` (`update_velocity()`) | Speed cap and damping |
| `max_G` | `three_body/physics.py` (`gravitational_force()`) | Force clamp |
| `colors`, `line_colors` | `three_body/scenario.py` | Planet colours |

To add the optional fourth body, uncomment the `earth` lines at the end of `create_new_planets()` in `three_body/scenario.py`.

## Files

| Path | Purpose |
| --- | --- |
| `sim.py` | Entry point |
| `three_body/` | Simulation package (see Code layout) |
| `space.jpg` | Background image |
| `requirements.txt` | Pinned Python dependencies |
| `.gitignore` | Ignores local virtual environments, caches, and editor files |
