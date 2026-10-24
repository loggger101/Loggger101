"""Record a clip of Satellite-Space-Flight for its animated gallery card (gallery.py runs it).

Drives the simulator the way its own tools/make_screenshots.py does: headless (SDL's
dummy video driver), its default scenario, the simulation advanced and then drawn with
the clock stopped, so the clip comes out the same every time. Between frames the clock
moves on by an equal step; the whole clip spans one orbit of the ISS, so the ISS ends
where it began and the loop barely shows.

    python tools/sim_clip.py OUT_DIR FRAMES

Writes OUT_DIR/000.png, 001.png, ... Needs the simulator's clone beside this repo and its
requirements (pygame, numpy). Run in its own process: pygame keeps global state.
"""
import os
import sys
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"          # before pygame is imported
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

SIM = Path(__file__).resolve().parents[2] / "Satellite Space Flight"
sys.path.insert(0, str(SIM))

import pygame  # noqa: E402

from satflight.elements import period_of, rv2coe  # noqa: E402
from satflight.ui.app import App  # noqa: E402

START = 45 * 60         # seconds into the scenario: the overview card's own moment
SIZE = (1600, 900)      # the size the simulator's README pictures are drawn at


def main():
    out, frames = Path(sys.argv[1]), int(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    app = App(SIM / "scenarios" / "default.json", size=SIZE)
    app.sim.advance(START)
    app.toasts.clear()                  # no "Loaded ..." banner over the scene
    for _ in range(10):                 # a fresh App's first frames draw a coarser Earth
        app.update(0.0)
        app.draw()
    # The ISS's period from its osculating elements, by the simulator's own functions.
    r_v = app.sim.y[app.sim.index_of("ISS")]
    step = float(period_of(rv2coe(r_v[:3], r_v[3:]).a)) / frames
    for k in range(frames):
        app.update(0.0)
        app.draw()
        pygame.image.save(app.screen, str(out / f"{k:03d}.png"))
        app.sim.advance(step)
    pygame.quit()
    print(f"{frames} frames, {step:.1f} s apart")


if __name__ == "__main__":
    main()
