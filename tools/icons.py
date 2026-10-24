"""Generate the icons beside the README's section headings (docs/icons/*.svg).

Each is a glyph from glyphs.py on a small tile with the link buttons' fill and border, so
it reads the same on GitHub's light and dark themes, like the rest of the profile's dark
pieces. They are decorative (the heading says what the section is), so the README gives
them empty alt text.
"""
import sys
from pathlib import Path

from glyphs import EDGE, ICONS, TILE

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
S, GLYPH = 28, 18          # tile size, and the glyph box drawn inside it

# file: glyph
SECTIONS = {
    "economics": "asteroid",
    "planetary": "belt",
    "learning": "network",
    "simulation": "orbit",
    "rare-disease": "heart",
    "elsewhere": "external",
    "activity": "rings",
    "languages": "code",
    "contact": "mail",
}

for name, glyph in SECTIONS.items():
    pad = (S - GLYPH) / 2
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" aria-hidden="true">
<rect x="0.75" y="0.75" width="{S - 1.5}" height="{S - 1.5}" rx="7" fill="{TILE}" stroke="{EDGE}" stroke-width="1.5"/>
<g transform="translate({pad} {pad})">{ICONS[glyph]}</g>
</svg>
"""
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8", newline="\n")
    print(name)
