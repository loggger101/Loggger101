"""Bin the main belt for the footer (tools/belt_profile.json), from the AsteroidCatalog
release asteroid-belt-gradient pins for its paper.

The footer draws the inner solar system to scale and fills the belt with points whose
density across follows this profile, so the Kirkwood gaps open where the catalog has them.
Each bin holds every body with a proper semimajor axis in it, and of those with a measured
albedo, how many are bright (p_V at least 0.10, mostly S-types) and how many dark (mostly
C-types), the split asteroid-belt-gradient's albedo.py uses. The footer colours the points
by that share, gold for bright and blue for dark.

Run by hand, like gallery.py: it needs the release on disk and pyarrow, which CI hasn't
got, so footer.py reads the JSON this writes instead.

    python tools/belt_profile.py
"""
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

GH = Path(__file__).resolve().parents[2]
RELEASE = "asteroid_catalog_data-2026-09-29c"
CATALOG = GH / f"asteroid-belt-gradient/data/{RELEASE}.parquet"
OUT = Path(__file__).parent / "belt_profile.json"
LO, HI, STEP = 1.75, 3.50, 0.01      # au
DARK_BELOW = 0.10                    # p_V, as in asteroid-belt-gradient's albedo.py

# A measured albedo is any the catalog holds, as in albedo.py's with_measured_albedo().
t = pq.read_table(CATALOG, columns=["proper_semi_major_axis_au", "albedo"])
a = t.column(0).to_numpy(zero_copy_only=False).astype(float)
pv = t.column(1).to_numpy(zero_copy_only=False).astype(float)
edges = np.round(np.arange(LO, HI + STEP / 2, STEP), 4)
inside = np.isfinite(a) & (a >= LO) & (a < HI)
measured = inside & np.isfinite(pv)
count = np.histogram(a[inside], edges)[0]
bright = np.histogram(a[measured & (pv >= DARK_BELOW)], edges)[0]
dark = np.histogram(a[measured & (pv < DARK_BELOW)], edges)[0]

OUT.write_text(json.dumps({
    "release": RELEASE,
    "au": [LO, HI, STEP],
    "bodies": int(count.sum()),
    "count": count.tolist(),
    "bright": bright.tolist(),
    "dark": dark.tolist(),
}, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
print(f"{OUT.name}: {int(count.sum()):,} bodies, {int(bright.sum() + dark.sum()):,} with a measured albedo")
