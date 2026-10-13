"""Draw the badge logos shields.io has no icon for (Astropy, pygame) and print their badge URLs.

Each logo is a white glyph on a 24x24 grid, written to docs/logos/<name>.svg for reference
and embedded in its badge as a base64 data URI (shields' custom-logo form), because a
badge can't load an image from this repo. After changing a glyph, rerun this and paste the
printed URL over the badge's src in the README.
"""
import base64
import sys
import urllib.parse
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# Ends of the ring's major axis (rx 11.2, tilted 22 degrees about the centre). Sweep flag 0
# runs left to right under the planet, 1 over it.
RING_FRONT = "M1.62 16.2A11.2 4 -22 0 0 22.38 7.8"
RING_BACK = "M1.62 16.2A11.2 4 -22 0 1 22.38 7.8"

LOGOS = {
    # A ringed planet, ring tilted 22 degrees. The front (lower) arc crosses the disc with a
    # gap cut around it; the back (upper) arc is hidden where the planet covers it.
    "astropy": f"""<mask id="d"><rect width="24" height="24" fill="#fff"/><path d="{RING_FRONT}" fill="none" stroke="#000" stroke-width="3.8"/></mask>
<mask id="b"><rect width="24" height="24" fill="#fff"/><circle cx="12" cy="12" r="7.6" fill="#000"/></mask>
<circle cx="12" cy="12" r="6.4" fill="#fff" mask="url(#d)"/>
<path d="{RING_FRONT}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
<path d="{RING_BACK}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" mask="url(#b)"/>""",
    # A gamepad with the d-pad and two buttons cut through it.
    "pygame": """<path fill="#fff" fill-rule="evenodd" d="M7 6h10a6 6 0 0 1 5.9 4.9l.9 5.2a3.3 3.3 0 0 1-5.6 2.8L15.6 16.4H8.4l-2.6 2.5a3.3 3.3 0 0 1-5.6-2.8l.9-5.2A6 6 0 0 1 7 6Z
M6 8.6v1.9H4.1v2.2H6v1.9h2.2v-1.9h1.9v-2.2H8.2V8.6Z
M15.05 10.2a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0-2.7 0Z
M17.45 12.6a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0-2.7 0Z"/>""",
}

for name, body in LOGOS.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{body}</svg>'
    (OUT / f"{name}.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    label = {"astropy": "Astropy", "pygame": "pygame"}[name]
    print(f"https://img.shields.io/badge/{label}-1f3354?style=flat-square&logo={urllib.parse.quote(uri, safe='')}")
