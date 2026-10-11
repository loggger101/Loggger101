"""Generate the diagram of how the asteroid repos feed each other (docs/pipeline*.svg).

`pipeline.svg` runs left to right for desktop widths. `pipeline-compact.svg` runs top to
bottom with larger text, for phones, where the wide version shrinks to about 350px; the
README swaps it in with <picture>, as it does for the stat tiles.

Solid arrows carry data (a pinned release or an installed package); dashed arrows are
citations. Check an edge against the two repos' READMEs before adding or moving it.
"""
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

# key: (title, line 1, line 2, kind). "repo" cards are repositories, "out" cards are what they produce.
NODES = {
    "gr": ("General_Research", "the sources the", "other repos cite", "repo"),
    "ac": ("AsteroidCatalog", "1.57M asteroids,", "frozen releases", "repo"),
    "sc": ("spacecost", "cited cost and mass", "tables, pip package", "repo"),
    "abg": ("asteroid-belt-gradient", "S/C gradient across", "161,659 asteroids", "repo"),
    "es": ("economicspace", "prices minerals, costs", "transport, sums profit", "repo"),
    "paper": ("Paper", "AASTeX, rebuilt from", "two public inputs", "out"),
    "targets": ("Mining targets", "ranked by net", "mission profit", "out"),
}
# (from, to, dashed)
EDGES = [
    ("gr", "ac", True),
    ("gr", "sc", True),
    ("ac", "abg", False),
    ("ac", "es", False),
    ("sc", "es", False),
    ("abg", "paper", False),
    ("es", "targets", False),
]
ALT = (
    "How the repos connect: General_Research holds the sources that AsteroidCatalog and "
    "spacecost cite. AsteroidCatalog releases feed asteroid-belt-gradient, which builds the "
    "paper, and economicspace, which also installs spacecost and ranks mining targets by profit."
)


def background(w, h, seed):
    rng = random.Random(seed)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, w - 8):.1f}" cy="{rng.uniform(8, h - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(int(w * h / 4500))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{ALT}">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#1e1640"/></linearGradient>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#5ba3dc"/></marker>
<marker id="arrow-dim" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#7d8fb3"/></marker>
</defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#g)" stroke="#2a3b63"/>
{stars}
"""


def card(key, x, y, w, h, title_size, line_size):
    title, l1, l2, kind = NODES[key]
    if kind == "repo":
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#13213f" stroke="#2f4a7a" stroke-width="1.5"/>'
        colour = "#5ba3dc"
    else:
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#1b2a4f" fill-opacity="0.5" stroke="#5ba3dc" stroke-width="1.5" stroke-dasharray="6 5"/>'
        colour = "#dbe3f5"
    gap = line_size * 1.3
    top = y + (h - title_size - 2 * gap) / 2 + title_size * 0.85
    return f"""{box}
<text x="{x + 16}" y="{top:.1f}" font-size="{title_size}" font-weight="700" fill="{colour}">{title}</text>
<text x="{x + 16}" y="{top + gap + 4:.1f}" font-size="{line_size}" fill="#b9c6e4">{l1}</text>
<text x="{x + 16}" y="{top + 2 * gap + 4:.1f}" font-size="{line_size}" fill="#b9c6e4">{l2}</text>"""


def edge(a, b, dashed, horizontal):
    """Arrow from box a to box b; boxes are (x, y, w, h). Curves when they are not in line."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    if horizontal:
        x1, y1, x2, y2 = ax + aw, ay + ah / 2, bx - 3, by + bh / 2
        mid = (x1 + x2) / 2
        d = f"M{x1:.1f} {y1:.1f} C{mid:.1f} {y1:.1f} {mid:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
    else:
        x1, y1, x2, y2 = ax + aw / 2, ay + ah, bx + bw / 2, by - 3
        mid = (y1 + y2) / 2
        d = f"M{x1:.1f} {y1:.1f} C{x1:.1f} {mid:.1f} {x2:.1f} {mid:.1f} {x2:.1f} {y2:.1f}"
    if dashed:
        return f'<path d="{d}" fill="none" stroke="#7d8fb3" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arrow-dim)"/>'
    return f'<path d="{d}" fill="none" stroke="#5ba3dc" stroke-width="2.5" marker-end="url(#arrow)"/>'


def legend(x, y, size):
    return f"""<g font-size="{size}" fill="#b9c6e4">
<line x1="{x}" y1="{y - size * 0.35:.1f}" x2="{x + 34}" y2="{y - size * 0.35:.1f}" stroke="#5ba3dc" stroke-width="2.5"/>
<text x="{x + 44}" y="{y}">data: a pinned release or package</text>
<line x1="{x + size * 21}" y1="{y - size * 0.35:.1f}" x2="{x + size * 21 + 34}" y2="{y - size * 0.35:.1f}" stroke="#7d8fb3" stroke-width="2" stroke-dasharray="5 5"/>
<text x="{x + size * 21 + 44}" y="{y}">cites</text>
</g>"""


def render(w, h, boxes, horizontal, title_size, line_size, legend_at, seed):
    parts = [background(w, h, seed), f'<g font-family="{FONT}">']
    parts += [edge(boxes[a], boxes[b], dashed, horizontal) for a, b, dashed in EDGES]
    parts += [card(k, *boxes[k], title_size, line_size) for k in NODES]
    parts.append(legend(*legend_at, line_size - 1))
    parts.append("</g>\n</svg>\n")
    return "\n".join(parts)


# Desktop: four columns, left to right.
CW = {1: 250, 2: 220, 3: 270, 4: 226}
CX = {1: 24, 2: 336, 3: 618, 4: 950}
TOP, BOT, CH = 34, 180, 104
wide = {
    "gr": (CX[1], (TOP + BOT) / 2, CW[1], CH),
    "ac": (CX[2], TOP, CW[2], CH),
    "sc": (CX[2], BOT, CW[2], CH),
    "abg": (CX[3], TOP, CW[3], CH),
    "es": (CX[3], BOT, CW[3], CH),
    "paper": (CX[4], TOP, CW[4], CH),
    "targets": (CX[4], BOT, CW[4], CH),
}
# Phones: four rows, top to bottom, two cards a row; General_Research sits centred on its own.
PW, PH, ROW = 300, 118, 168
left, right = 14, 326
tall = {
    "gr": ((640 - PW) / 2, 20, PW, PH),
    "ac": (left, 20 + ROW, PW, PH),
    "sc": (right, 20 + ROW, PW, PH),
    "abg": (left, 20 + 2 * ROW, PW, PH),
    "es": (right, 20 + 2 * ROW, PW, PH),
    "paper": (left, 20 + 3 * ROW, PW, PH),
    "targets": (right, 20 + 3 * ROW, PW, PH),
}

files = {
    "pipeline.svg": render(1200, 336, wide, True, 22, 17, (CX[1], 320), 7),
    "pipeline-compact.svg": render(640, 20 + 3 * ROW + PH + 64, tall, False, 25, 21, (left + 4, 20 + 3 * ROW + PH + 42), 8),
}
for name, svg in files.items():
    (OUT / name).write_text(svg, encoding="utf-8", newline="\n")
    print(name)
