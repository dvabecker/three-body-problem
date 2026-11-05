# Three-Body Problem

A small matplotlib animation of three planets orbiting each other under a simplified gravitational force. Each planet is pulled toward the others, the simulation runs frame by frame, and the animation resets with a new random start once the run ends.

## Requirements

- Python 3.10 (the original environment was built with 3.10.11)
- The packages pinned in `requirements.txt` (matplotlib, numpy, Pillow, and their dependencies)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The virtual environment directory is ignored by git, so it stays local.

## Running

Run the script from the repository root, because it loads `space.jpg` by a relative path:

```bash
python sim.py
```

A window opens showing the animation on a starfield background.

## How it works

- **Planets:** three `Planet` objects start on a circle of radius 3 at 120° apart, with a small random offset and a tangential initial velocity.
- **Forces:** `gravitational_force` computes the pull between each pair of planets. Each force component is clamped to ±5 to keep the motion stable.
- **Integration:** `sim.py` contains two integrators, `euler_step` and `runge_kutta_step`. The animation currently uses `'euler'`; change the `fargs` in `start_animation()` to `'runge_kutta'` to switch.
- **Speed limit:** velocities are capped at 3 units per step, with damping applied when the cap is exceeded.
- **Reset:** a new run starts after 10,000 frames, or when all three planets are outside the ±10 viewport.

## Tuning

Most behaviour is set by constants inside `sim.py`:

| Setting | Location | Effect |
| --- | --- | --- |
| `dt` | `animate()` | Time step per frame |
| `max_velocity`, `damping_factor` | `update_velocity()` | Speed cap and damping |
| `max_G` | `gravitational_force()` | Force clamp |
| `FRAMES_NUM` | module level | Frames before reset |
| `colors`, `line_colors` | `create_new_planets()` | Planet colours |

An optional fourth body (the commented-out `earth` planet) is available in `create_new_planets()`.

## Files

| Path | Purpose |
| --- | --- |
| `sim.py` | Simulation and animation |
| `space.jpg` | Background image |
| `requirements.txt` | Pinned Python dependencies |
| `.gitignore` | Ignores local virtual environments, caches, and editor files |
