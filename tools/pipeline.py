"""Generate the diagram of how the space-economics repos feed each other (docs/pipeline*.svg).

`pipeline.svg` runs left to right for desktop widths. `pipeline-compact.svg` runs top to
bottom with larger text, for phones, where the wide version shrinks to about 350px; the
README swaps it in with <picture>, as it does for the stat tiles.

Solid arrows carry data (a pinned release or an installed package); dashed arrows are
citations. Check an edge against the two repos' READMEs before adding or moving it.
Packages economicspace installs side by side share one line into it (a bus): the others
join it as branches without heads of their own (`wide_branches`, `tall_branches`).

Card widths are set so the longest title, "asteroid-belt-gradient", fits even in a font as
wide as Verdana, which stands in for DejaVu Sans on Linux machines without Arial.

It moves the way the banner does: points of light run along the data arrows in the
direction the data goes, the citations' dashes creep toward what cites them, and a few
stars twinkle. With reduced motion it stands still, and the points of light, which only
show while they move, are gone.
"""
import json
import sys
from pathlib import Path

import panel
from refresh_counts import millions

# The catalog's size, which refresh_counts.py keeps current.
COUNTS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))
CATALOG_ROWS = COUNTS["catalog_rows"]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

# key: (title, line 1, line 2, kind). "repo" cards are repositories, "out" cards are what they produce.
NODES = {
    "gr": ("General_Research", "the sources the", "other repos cite", "repo"),
    "ac": ("AsteroidCatalog", f"{millions(CATALOG_ROWS)}M asteroids,", "frozen releases", "repo"),
    "sc": ("spacecost", "cited cost and mass", "tables, pip package", "repo"),
    "sv": ("spacevalue", "mineral prices at", "eight destinations", "repo"),
    "abg": ("asteroid-belt-gradient", "S/C gradient across", f"{COUNTS['belt']['classified']:,} asteroids", "repo"),
    "es": ("economicspace", "rocket equation, cost", "cascade, sums profit", "repo"),
    "paper": ("Paper", "AASTeX, rebuilt from", "two public inputs", "out"),
    "targets": ("Mining targets", "ranked by net", "mission profit", "out"),
    "ql": ("quietlaunch", "windowless dashboard", "launcher, pip package", "repo"),
    "sr": ("starred-repos", "the pipeline audited", "against 211 starred", "repo"),
    "qq": ("quietqueue", "the campaign's job", "runner, pip package", "repo"),
    "sb": ("samebytes", "bit-identity checks", "for releases, pip package", "repo"),
}
# (from, to, dashed)
EDGES = [
    ("gr", "ac", True),
    ("gr", "sc", True),
    ("gr", "sv", True),
    ("gr", "es", True),
    ("ac", "abg", False),
    ("ac", "es", False),
    ("sc", "sv", False),   # spacevalue installs the pinned package for its launch prices
    ("sv", "es", False),   # economicspace pins a spacevalue release as its Stage 2
    ("sc", "es", False),
    ("abg", "paper", False),
    ("es", "targets", False),
    ("ql", "es", False),   # economicspace's launcher installs the pinned package
    ("sr", "es", True),    # economicspace cites the audit's orbit-quality measurement
    ("qq", "es", False),   # economicspace's campaign installs the pinned package
    ("sb", "es", False),   # economicspace's verify scripts install the pinned package
]
ALT = (
    "How the repos connect: General_Research holds the sources that AsteroidCatalog, "
    "spacecost, spacevalue and economicspace cite. AsteroidCatalog releases feed asteroid-belt-gradient, which builds the "
    "paper, and economicspace. spacevalue installs spacecost and prices minerals at each destination, and its releases "
    "feed economicspace too, which also installs spacecost, quietlaunch, quietqueue and samebytes, cites the starred-repos audit, "
    "and ranks mining targets by profit."
)


# The arrowheads: bright for data, dim for citations.
MARKERS = tuple(
    f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    f'<path d="M0 0 L10 5 L0 10 z" fill="{colour}"/></marker>'
    for name, colour in (("arrow", "#5ba3dc"), ("arrow-dim", "#7d8fb3")))


def background(w, h, seed):
    return panel.background(w, h, seed, ALT, defs=MARKERS, rules=(
        f".flow {{ opacity: 0; animation: flow {FLOW_SECONDS}s linear infinite; }}",
        f"@keyframes flow {{ from {{ stroke-dashoffset: {FLOW_GAP}; opacity: 0.9; }} to {{ stroke-dashoffset: 0; opacity: 0.9; }} }}",
        ".cite { animation: cite 1.2s linear infinite; }",
        "@keyframes cite { from { stroke-dashoffset: 10; } to { stroke-dashoffset: 0; } }",
    ), animated=("flow", "cite"))


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


FLOW_GAP = 48          # px between the points of light on a data arrow
FLOW_SECONDS = 1.4     # time for each to travel FLOW_GAP


def arrow(d, dashed, head=True):
    """The path d as a citation (dashed, its dashes creeping forward) or as a data arrow
    with points of light running along it. A dash offset falling to 0 moves the pattern
    toward the end of the path. Each point of light is a wide faint dot under a small bright
    one; the group's dash offset, which both inherit, moves them together. Without a head,
    it is a branch that joins another arrow's line."""
    if dashed:
        return f'<path class="cite" d="{d}" fill="none" stroke="#7d8fb3" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arrow-dim)"/>'
    dots = f'fill="none" stroke-linecap="round" stroke-dasharray="0.01 {FLOW_GAP - 0.01}"'
    marker = ' marker-end="url(#arrow)"' if head else ""
    return (f'<path d="{d}" fill="none" stroke="#5ba3dc" stroke-width="2.5"{marker}/>'
            f'<g class="flow"><path d="{d}" {dots} stroke="#5ba3dc" stroke-opacity="0.45" stroke-width="13"/>'
            f'<path d="{d}" {dots} stroke="#ffffff" stroke-width="6"/></g>')


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
    return arrow(d, dashed)


def elbow(points, dashed, head=True, r=8):
    """An arrow along straight runs through points, with each corner rounded."""
    d = f"M{points[0][0]:.1f} {points[0][1]:.1f}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(points, points[1:], points[2:]):
        # Stop r short of the corner, then curve round it to r past it.
        ux, uy = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)
        vx, vy = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
        d += f" L{x1 - ux * r:.1f} {y1 - uy * r:.1f} Q{x1:.1f} {y1:.1f} {x1 + vx * r:.1f} {y1 + vy * r:.1f}"
    d += f" L{points[-1][0]:.1f} {points[-1][1]:.1f}"
    return arrow(d, dashed, head)


def route(a, b, dashed, boxes, horizontal, lanes, branches):
    """The arrow for edge a -> b. An edge in branches has no head of its own: its lane ends
    on another arrow's line (the trunk), which carries it the rest of the way, so packages
    economicspace installs side by side arrive as one line instead of a bundle of them."""
    if (a, b) in lanes:
        return elbow(lanes[a, b](boxes), dashed, (a, b) not in branches)
    return edge(boxes[a], boxes[b], dashed, horizontal)


def legend(x, y, size):
    return f"""<g font-size="{size}" fill="#b9c6e4">
<line x1="{x}" y1="{y - size * 0.35:.1f}" x2="{x + 34}" y2="{y - size * 0.35:.1f}" stroke="#5ba3dc" stroke-width="2.5"/>
<text x="{x + 44}" y="{y}">data: a pinned release or package</text>
<line x1="{x + size * 21}" y1="{y - size * 0.35:.1f}" x2="{x + size * 21 + 34}" y2="{y - size * 0.35:.1f}" stroke="#7d8fb3" stroke-width="2" stroke-dasharray="5 5"/>
<text x="{x + size * 21 + 44}" y="{y}">cites</text>
</g>"""


def render(w, h, boxes, horizontal, title_size, line_size, legend_at, seed, lanes, branches):
    parts = [background(w, h, seed), f'<g font-family="{FONT}">']
    parts += [route(a, b, dashed, boxes, horizontal, lanes, branches) for a, b, dashed in EDGES]
    parts += [card(k, *boxes[k], title_size, line_size) for k in NODES]
    parts.append(legend(*legend_at, line_size - 1))
    parts.append("</g>\n</svg>\n")
    return panel.keep_clear("\n".join(parts))


# Edges a plain curve can't take, as the corners of a path of straight runs, given the boxes.
def at(box, fx, fy):
    x, y, w, h = box
    return x + w * fx, y + h * fy


# Desktop: four columns, left to right. The top row runs from the sources to the paper, the
# second from spacecost to the mining targets, and the cards in the third row feed
# economicspace from below. Citations from General_Research run along a lane between the top
# two rows, and the data AsteroidCatalog sends economicspace along a lane above that.
# The third column is the widest so "asteroid-belt-gradient" fits even in a font as wide as
# Verdana (DejaVu Sans, on Linux machines without Arial); the gaps hold an arrow and its head.
CW = {1: 250, 2: 224, 3: 300, 4: 216}
GAP = 54
CX = {1: 24}
for col in (2, 3, 4):
    CX[col] = CX[col - 1] + CW[col - 1] + GAP
TOP, MID, CH = 34, 200, 104
wide = {
    "gr": (CX[1], TOP, CW[1], CH),
    "sc": (CX[1], MID, CW[1], CH),
    "ac": (CX[2], TOP, CW[2], CH),
    "sv": (CX[2], MID, CW[2], CH),
    "abg": (CX[3], TOP, CW[3], CH),
    "es": (CX[3], MID, CW[3], CH),
    "paper": (CX[4], TOP, CW[4], CH),
    "targets": (CX[4], MID, CW[4], CH),
}
CITE_LANE, DATA_LANE = TOP + CH + 44, TOP + CH + 22
# Under the second row, one bus carries the four packages economicspace installs: spacecost
# drops into it, the trunk, and samebytes, quietlaunch and quietqueue climb into it from the
# third row. It rises into economicspace's bottom at TRUNK_X, straight over quietqueue. The
# audit's citation runs at the same height to the right of it, where the bus has ended.
BUS = MID + CH + 26
R3 = BUS + 26
wide.update({
    "sb": (CX[1], R3, CW[1], CH),
    "ql": (CX[2], R3, CW[2], CH),
    "qq": (CX[3], R3, CW[3], CH),
    "sr": (CX[4], R3, CW[4], CH),
})
TRUNK_X = CX[3] + CW[3] * 0.45


def onto_bus(b, key, fx):
    """Up out of key's top, fx along it, to the bus."""
    x = at(b[key], fx, 0)[0]
    return [(x, R3), (x, BUS)]


wide_branches = {("sb", "es"), ("ql", "es"), ("qq", "es")}
wide_lanes = {
    ("gr", "sc"): lambda b: [at(b["gr"], 0.5, 1), (at(b["sc"], 0.5, 0)[0], b["sc"][1] - 3)],
    ("gr", "sv"): lambda b: [at(b["gr"], 0.8, 1), (at(b["gr"], 0.8, 1)[0], CITE_LANE),
                             (at(b["sv"], 0.3, 0)[0], CITE_LANE), (at(b["sv"], 0.3, 0)[0], MID - 3)],
    ("gr", "es"): lambda b: [at(b["gr"], 0.8, 1), (at(b["gr"], 0.8, 1)[0], CITE_LANE),
                             (at(b["es"], 0.25, 0)[0], CITE_LANE), (at(b["es"], 0.25, 0)[0], MID - 3)],
    # Down the gutter between AsteroidCatalog and the paper's repo, then over the citations.
    ("ac", "es"): lambda b: [at(b["ac"], 1, 0.75), ((CX[2] + CW[2] + CX[3]) / 2, at(b["ac"], 1, 0.75)[1]),
                             ((CX[2] + CW[2] + CX[3]) / 2, DATA_LANE), (at(b["es"], 0.6, 0)[0], DATA_LANE),
                             (at(b["es"], 0.6, 0)[0], MID - 3)],
    # The bus's trunk: down out of spacecost, under spacevalue, and up into economicspace.
    ("sc", "es"): lambda b: [at(b["sc"], 0.3, 1), (at(b["sc"], 0.3, 1)[0], BUS),
                             (TRUNK_X, BUS), (TRUNK_X, MID + CH + 3)],
    ("sb", "es"): lambda b: onto_bus(b, "sb", 0.7),
    ("ql", "es"): lambda b: onto_bus(b, "ql", 0.5),
    # Straight up into the trunk's climb, past its corner, so the two read as one line.
    ("qq", "es"): lambda b: [(TRUNK_X, R3), (TRUNK_X, BUS - 8)],
    # Up out of the audit and over to economicspace's lower right, under the mining targets.
    ("sr", "es"): lambda b: [at(b["sr"], 0.15, 0), (at(b["sr"], 0.15, 0)[0], BUS),
                             (at(b["es"], 0.85, 1)[0], BUS), (at(b["es"], 0.85, 1)[0], MID + CH + 3)],
}
# Phones: six rows, top to bottom, two cards a row, starred-repos beside General_Research.
# The citations leave General_Research's right side and come down the middle of the gap
# between the columns, AsteroidCatalog's data left of them, and quietlaunch and quietqueue
# climb a lane right of them to economicspace's lower left. On the right edge spacecost's
# data runs down past spacevalue, the audit's citation down the outside of it, and
# samebytes's climbs from under the mining targets, each in its own stretch. The left
# column is wider (LW) so "asteroid-belt-gradient" fits in a font as wide as Verdana.
PW, LW, PH, ROW = 300, 324, 118, 168
PWIDTH, left = 760, 12
right = left + LW + 80
tall = {
    "gr": (left, 20, LW, PH),
    "sr": (right, 20, PW, PH),
    "ac": (left, 20 + ROW, LW, PH),
    "sc": (right, 20 + ROW, PW, PH),
    "abg": (left, 20 + 2 * ROW, LW, PH),
    "sv": (right, 20 + 2 * ROW, PW, PH),
    "paper": (left, 20 + 3 * ROW, LW, PH),
    "es": (right, 20 + 3 * ROW, PW, PH),
    "ql": (left, 20 + 4 * ROW, LW, PH),
    "targets": (right, 20 + 4 * ROW, PW, PH),
    "qq": (left, 20 + 5 * ROW, LW, PH),
    "sb": (right, 20 + 5 * ROW, PW, PH),
}
GAP_X = (left + LW + right) / 2
EDGE_IN, EDGE_OUT = right + PW + 15, right + PW + 28
PKG_LANE = right - 26


def cite_from_gr(b, key, fy):
    """Out of General_Research's right side, down the gap, into key's left side fy down."""
    y = at(b[key], 0, fy)[1]
    return [at(b["gr"], 1, 0.5), (GAP_X, at(b["gr"], 1, 0.5)[1]), (GAP_X, y), (right - 3, y)]


tall_lanes = {
    ("gr", "sc"): lambda b: cite_from_gr(b, "sc", 0.5),
    ("gr", "sv"): lambda b: cite_from_gr(b, "sv", 0.3),
    ("gr", "es"): lambda b: cite_from_gr(b, "es", 0.2),
    ("ac", "es"): lambda b: [at(b["ac"], 1, 0.75), (left + LW + 14, at(b["ac"], 1, 0.75)[1]),
                             (left + LW + 14, at(b["es"], 0, 0.45)[1]), (right - 3, at(b["es"], 0, 0.45)[1])],
    ("sc", "es"): lambda b: [at(b["sc"], 1, 0.75), (EDGE_IN, at(b["sc"], 1, 0.75)[1]),
                             (EDGE_IN, at(b["es"], 1, 0.3)[1]), (right + PW + 3, at(b["es"], 1, 0.3)[1])],
    ("sr", "es"): lambda b: [at(b["sr"], 1, 0.5), (EDGE_OUT, at(b["sr"], 1, 0.5)[1]),
                             (EDGE_OUT, at(b["es"], 1, 0.6)[1]), (right + PW + 3, at(b["es"], 1, 0.6)[1])],
    ("sb", "es"): lambda b: [at(b["sb"], 1, 0.5), (EDGE_IN, at(b["sb"], 1, 0.5)[1]),
                             (EDGE_IN, at(b["es"], 1, 0.85)[1]), (right + PW + 3, at(b["es"], 1, 0.85)[1])],
    # quietqueue's climb is the trunk into economicspace's lower left; quietlaunch joins it.
    ("qq", "es"): lambda b: [at(b["qq"], 1, 0.5), (PKG_LANE, at(b["qq"], 1, 0.5)[1]),
                             (PKG_LANE, at(b["es"], 0, 0.72)[1]), (right - 3, at(b["es"], 0, 0.72)[1])],
    ("ql", "es"): lambda b: [at(b["ql"], 1, 0.5), (PKG_LANE, at(b["ql"], 1, 0.5)[1])],
}
tall_branches = {("ql", "es")}

files = {
    "pipeline.svg": render(1200, R3 + CH + 56, wide, True, 22, 17, (CX[1], R3 + CH + 40), 7,
                           wide_lanes, wide_branches),
    "pipeline-compact.svg": render(PWIDTH, 20 + 5 * ROW + PH + 64, tall, False, 24, 22,
                                   (left + 4, 20 + 5 * ROW + PH + 42), 8, tall_lanes, tall_branches),
}
for name, svg in files.items():
    (OUT / name).write_text(svg, encoding="utf-8", newline="\n")
    print(name)
