"""The banner's star and its orbiting body, shared by banner.py and footer.py, and the
asteroid belt the banner draws round them.

The system is drawn in its own 340 x 300 coordinate box centred on (170, 150), the
banner's layout. The animations scale about that fixed point (CSS transform-origin),
so a page that wants the system somewhere else, or smaller, places it with a nested
<svg> viewport (see `nested`) rather than a transform, which would move the origin.
"""

import json
import math
import random
from pathlib import Path

CX, CY = 170, 150
BOX_W, BOX_H = 340, 300

# The belt, drawn from the catalog (belt_profile.json, which belt_profile.py writes): its
# lanes are the real belt's stretches between the Kirkwood gaps, from 2.1 au to the 2:1
# resonance, laid from just outside the body's orbit (rx 125) at RADII. Each lane holds
# rocks in proportion to the bodies in its stretch, each rock at a distance drawn as the
# catalog's are and gold or blue-grey by the share of bright and dark bodies with a
# measured albedo there, so the belt turns from S-type gold to C-type blue outward as the
# real one does. Seen at the orbit's tilt, so flattened to its 42/125. Inner lanes turn
# faster (Kepler's third law: period goes as radius^1.5).
TILT, FLAT = -18, 42 / 125
PROFILE = json.loads((Path(__file__).parent / "belt_profile.json").read_text(encoding="utf-8"))
# The lanes' edges, au: the belt's inner edge, then the 3:1, 5:2, 7:3 and 2:1 resonances.
EDGES = (2.1, 2.502, 2.825, 2.958, 3.279)
RADII = (138, 168)                    # where 2.1 au and 3.279 au fall
GAP_PX = 1.2                          # each lane stops this short of a gap, so the gaps show
ROCKS = 120
LANE_PERIOD = 90                                             # seconds per turn for the first lane
S_TYPE, C_TYPE = (0xe8, 0xc2, 0x7a), (0x8f, 0xa8, 0xc8)


def radius(a):
    """The banner radius of a distance a (au) from the Sun."""
    return RADII[0] + (RADII[1] - RADII[0]) * (a - EDGES[0]) / (EDGES[-1] - EDGES[0])


def lanes():
    """(inner radius, outer radius, [(bin index, weight)]) for each stretch between gaps."""
    lo, _, step = PROFILE["au"]
    out = []
    for a0, a1 in zip(EDGES, EDGES[1:]):
        bins = [(i, n) for i, n in enumerate(PROFILE["count"]) if a0 <= lo + (i + 0.5) * step < a1 and n]
        out.append((radius(a0) + (GAP_PX if a0 != EDGES[0] else 0), radius(a1) - GAP_PX, bins))
    return out


def bright_share(i, spread=2):
    """The share of bright bodies among those with a measured albedo, over bin i and spread
    either side; 0.5 where there are none."""
    b, d = PROFILE["bright"][max(0, i - spread):i + spread + 1], PROFILE["dark"][max(0, i - spread):i + spread + 1]
    return sum(b) / (sum(b) + sum(d)) if sum(b) + sum(d) else 0.5

DEFS = """  <radialGradient id="corona" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/>
    <stop offset="0.07" stop-color="#e6f2ff" stop-opacity="0.75"/>
    <stop offset="0.2" stop-color="#9ccaf2" stop-opacity="0.5"/>
    <stop offset="0.45" stop-color="#5ba3dc" stop-opacity="0.2"/>
    <stop offset="1" stop-color="#5ba3dc" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset="0.45" stop-color="#ffffff"/>
    <stop offset="0.7" stop-color="#dcefff" stop-opacity="0.85"/>
    <stop offset="1" stop-color="#a9d3f7" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="spike" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#5ba3dc" stop-opacity="0"/>
    <stop offset="0.3" stop-color="#8fc2ee" stop-opacity="0.45"/>
    <stop offset="0.5" stop-color="#ffffff"/>
    <stop offset="0.7" stop-color="#8fc2ee" stop-opacity="0.45"/>
    <stop offset="1" stop-color="#5ba3dc" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="body" cx="0.35" cy="0.35" r="0.65">
    <stop offset="0" stop-color="#fff4d8"/>
    <stop offset="0.45" stop-color="#e8c27a"/>
    <stop offset="1" stop-color="#7a5a26"/>
  </radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="0.7"/></filter>
  <filter id="bloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>"""

STYLE = f"""  .breathe {{ animation: breathe 6s ease-in-out infinite; transform-origin: {CX}px {CY}px; }}
  @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.85; }} 50% {{ transform: scale(1.08); opacity: 1; }} }}
  .rays {{ animation: rays 6s ease-in-out infinite; transform-origin: {CX}px {CY}px; }}
  @keyframes rays {{ 0%, 100% {{ transform: scale(0.94); opacity: 0.8; }} 50% {{ transform: scale(1.04); opacity: 1; }} }}
  .rays2 {{ animation: rays2 4.5s ease-in-out infinite; transform-origin: {CX}px {CY}px; }}
  @keyframes rays2 {{ 0%, 100% {{ opacity: 0.55; }} 50% {{ opacity: 0.9; }} }}
  .lane {{ animation: lane var(--t) linear var(--d) infinite; transform-origin: 0 0; }}
  .lane ellipse {{ animation: unlane var(--t) linear var(--d) infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes lane {{ to {{ transform: rotate(360deg); }} }}
  @keyframes unlane {{ to {{ transform: rotate(-360deg); }} }}"""

# Class names the page's reduced-motion rule must stop.
ANIMATED = (".breathe", ".rays", ".rays2", ".lane", ".lane ellipse")


def spike(length, width, angle):
    """A long thin diamond through the centre, white in the middle and clear at both tips."""
    return (f'<polygon points="{CX - length},{CY} {CX},{CY - width} {CX + length},{CY} {CX},{CY + width}" '
            f'fill="url(#spike)" transform="rotate({angle} {CX} {CY})"/>')


def belt():
    """The belt's lanes, each turning about the star. A lane is drawn as a circle of rocks in
    a group squashed to the orbit's tilt, so one rotation turns it along its ellipse. Each
    rock is drawn tall by the same factor and turns back as fast as its lane turns, so it
    stays upright and the squash leaves it round. Rocks are ellipses, not circles, so
    panel.keep_clear, which reads circles at their untransformed place, leaves them be."""
    rng = random.Random(7)
    parts = [f'<g transform="translate({CX} {CY}) rotate({TILT}) scale(1 {FLAT:.4f})">']
    ls = lanes()
    total = sum(n for *_, bins in ls for _, n in bins)
    lo, _, step = PROFILE["au"]
    first = (ls[0][0] + ls[0][1]) / 2
    gold, blue = ("#" + "".join(f"{c:02x}" for c in rgb) for rgb in (S_TYPE, C_TYPE))
    for r0, r1, bins in ls:
        period = LANE_PERIOD * (((r0 + r1) / 2) / first) ** 1.5
        parts.append(f'<g class="lane" style="--t:{period:.1f}s;--d:-{rng.uniform(0, period):.1f}s">')
        n = round(ROCKS * sum(w for _, w in bins) / total)
        for i in rng.choices([i for i, _ in bins], weights=[w for _, w in bins], k=n):
            # Where in its bin, then onto the lane (kept inside its edges).
            r = min(max(radius(lo + (i + rng.random()) * step), r0), r1)
            a = rng.uniform(0, 2 * math.pi)
            colour = gold if rng.random() < bright_share(i) else blue
            size = rng.choice((0.9, 1.1, 1.3, 1.6))
            parts.append(f'<ellipse cx="{r * math.cos(a):.1f}" cy="{r * math.sin(a):.1f}" rx="{size}" ry="{size / FLAT:.2f}" '
                         f'fill="{colour}" opacity="{rng.uniform(0.45, 0.9):.2f}"/>')
        parts.append("</g>")
    parts.append("</g>")
    return parts


def system(with_belt=False):
    """The belt if asked for, the orbit's far half, the star, then the near half, so the
    body passes in front."""
    cx, cy = CX, CY
    path = f"M {cx + 125} {cy} A 125 42 0 1 1 {cx - 125} {cy} A 125 42 0 1 1 {cx + 125} {cy}"
    main = "".join(spike(126, 3.2, ang) for ang in (0, 90))
    diag = "".join(spike(80, 2.2, ang) for ang in (45, 135))
    return [
        *(belt() if with_belt else []),
        # Orbit around the star, tilted ellipse
        f'<g transform="rotate(-18 {cx} {cy})">',
        f'<ellipse cx="{cx}" cy="{cy}" rx="125" ry="42" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>',
        f'<circle r="5" fill="url(#body)"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/></circle>',
        "</g>",
        # The star, drawn as light: a corona, diffraction spikes and a white-hot core.
        f'<circle class="breathe" cx="{cx}" cy="{cy}" r="135" fill="url(#corona)"/>',
        f'<g class="rays"><g filter="url(#bloom)" opacity="0.55">{main}</g><g filter="url(#soft)">{main}</g></g>',
        f'<g class="rays2" filter="url(#soft)">{diag}</g>',
        f'<circle class="breathe" cx="{cx}" cy="{cy}" r="24" fill="url(#core)"/>',
        f'<circle cx="{cx}" cy="{cy}" r="6" fill="#ffffff"/>',
        # Near half of the orbit, redrawn over the star. The path runs clockwise from the
        # right end, so its first half is the near (lower) arc.
        f'<g transform="rotate(-18 {cx} {cy})">',
        f'<path d="M {cx + 125} {cy} A 125 42 0 0 1 {cx - 125} {cy}" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>',
        f'<circle r="5" fill="url(#body)"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/>'
        '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" calcMode="discrete" values="1;0" keyTimes="0;0.5"/></circle>',
        "</g>",
    ]


def nested(x_centre, y_centre, scale, with_belt=False):
    """The system centred at (x_centre, y_centre) and scaled, in its own viewport."""
    w, h = BOX_W * scale, BOX_H * scale
    return ([f'<svg x="{x_centre - w / 2:g}" y="{y_centre - h / 2:g}" width="{w:g}" height="{h:g}" '
             f'viewBox="0 0 {BOX_W} {BOX_H}" overflow="visible">']
            + system(with_belt) + ["</svg>"])
