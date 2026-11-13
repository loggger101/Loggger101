"""Generate the 'by the numbers' stat tiles (docs/stats/*.svg) in the banner's style.

Each tile comes in two versions. `<name>.svg` is the full tile for desktop widths.
`<name>-compact.svg` has a larger number and a one- or two-word label, for phones, where
four tiles in a row leave each one about 70px wide; the README swaps it in with <picture>.
Neither shows the repo name: the tile links to the repo and its alt text names it, and at
laptop widths (tiles about 140px) a third line of text is too small to read.

The number rolls up like an odometer when the tile loads: each digit is a column of digits
that spins once round and stops on its own. Every character is placed by itself, so the
columns line up; ADVANCE has Segoe UI Bold's widths (Arial Bold's are within a few
percent, so the number only spaces a little looser there). With reduced motion the number
just stands there, as does a still render: the columns rest on the real digits.

Under the label each desktop tile draws a thin strip of its own data, which grows in
from the left as the number rolls: the belt's density across it from the catalog, with the
Kirkwood gaps (belt_profile.json); the paper's turn from S-type gold to C-type blue, its
corrected midpoint and the snow line; the sources' four tiers of authority, coloured as in
the sources chart; and one segment for each category of skills. Phones get no strip: at
about 70px a tile has no room for one.
"""
import json
import random
import sys
from pathlib import Path

import panel
from refresh_counts import millions

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 270, 120
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
# Advance widths in Segoe UI Bold, in ems (measured with Pillow; its digits are all one width).
ADVANCE = {**dict.fromkeys("0123456789", 0.575), ",": 0.271, ".": 0.271, "M": 0.957}
ROLL = 1.8              # seconds a digit column spins

# The numbers are in counts.json, which refresh_counts.py keeps current: the belt's from the
# paper's results, the catalog's size from its latest release, and the two that grow.
COUNTS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))

PROFILE = json.loads((Path(__file__).parent / "belt_profile.json").read_text(encoding="utf-8"))

# name: (number, label, short label for the compact tile, repo)
TILES = {
    "catalog": (f"{millions(COUNTS['catalog_rows'])}M", "asteroids cataloged", "asteroids", "AsteroidCatalog"),
    "belt": (f"{COUNTS['belt']['classified']:,}", "asteroids analyzed", "analyzed", "asteroid-belt-gradient"),
    "sources": (f"{COUNTS['sources']:,}", "research sources", "sources", "General_Research"),
    "skills": (f"{COUNTS['skills']:,}", "agent skills", "agent skills", "Hermes_Skills"),
}


def frame(i, label, body):
    """The tile's opening, its stars kept off what body draws: each star is drawn until it
    lands clear, so a tile that is mostly number has as many as one that isn't."""
    rng = random.Random(100 + i)
    boxes = panel.clear_boxes(body)

    def spot():
        while True:
            x, y = rng.uniform(8, W - 8), rng.uniform(8, H - 8)
            if panel.is_clear(boxes, x, y):
                return f'cx="{x:.1f}" cy="{y:.1f}"'
    stars = "".join(
        f'<circle {spot()} r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(14)
    )
    # Three stars twinkle, as in the banner; drawn after the still ones, so those stay put.
    twinkles = "".join(
        f'<circle class="tw" {spot()} r="1.2" fill="#dbe7ff" '
        f'style="animation-delay:-{rng.uniform(0, 4):.2f}s;animation-duration:{rng.uniform(3, 6):.2f}s"/>'
        for _ in range(3)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#112650"/></linearGradient></defs>
<style>
  .tw {{ animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%, 100% {{ opacity: 0.15; }} 50% {{ opacity: 1; }} }}
  .roll {{ animation: roll {ROLL}s cubic-bezier(0.15, 0.85, 0.25, 1) both; }}
  @keyframes roll {{ from {{ transform: translateY(var(--from)); }} }}
  {panel.GROW[0]}
  {panel.GROW[1]}
  @media (prefers-reduced-motion: reduce) {{ .tw, .roll, .grow {{ animation: none; }} }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="url(#g)" stroke="#2a3b63"/>
{stars}
{twinkles}
"""


def odometer(num, x, y, size, centred=False):
    """num in bold blue at baseline y, from x (or centred on x), each digit a column that
    rolls up through one full turn to land on it. The columns show through a window one
    line tall; the line pitch is taller than the window, so only one digit shows."""
    width = sum(ADVANCE[c] for c in num) * size
    left = x - width / 2 if centred else x
    pitch = size * 1.3
    window = f'<clipPath id="window"><rect x="{left - 2:.1f}" y="{y - size * 0.95:.1f}" width="{width + 4:.1f}" height="{size * 1.2:.1f}"/></clipPath>'
    # text-anchor="start": each character sits at its own x, whatever the tile's anchor.
    out = [window, f'<g clip-path="url(#window)" text-anchor="start" font-weight="700" fill="#5ba3dc" font-size="{size}">']
    at, k = left, 0
    for c in num:
        if c.isdigit():
            d = int(c)
            # 0 up to 9, then 0 up to d: the column ends on d, at the baseline.
            strip = list(range(10)) + list(range(d + 1))
            cells = "".join(f'<text x="{at:.1f}" y="{y - (len(strip) - 1 - j) * pitch:.1f}">{v}</text>'
                            for j, v in enumerate(strip))
            # Columns to the right start a moment later, as a counter's last digits do.
            out.append(f'<g class="roll" style="--from:{(len(strip) - 1) * pitch:.1f}px;'
                       f'animation-delay:{0.15 + 0.08 * k:.2f}s">{cells}</g>')
            k += 1
        else:
            out.append(f'<text x="{at:.1f}" y="{y}">{c}</text>')
        at += ADVANCE[c] * size
    out.append("</g>")
    return "\n".join(out)


# The data strip under the label on desktop tiles.
SX, SY, SW, SH = 20, 103, W - 40, 5
BLUE, DIM, TRACK = "#5ba3dc", "#7d8fb3", "#1b2a4f"
# sources.py's tier colours, T1 to T3; T4 (grey sources) is hollow, as there.
TIER_FILL = ("#d2e9fb", "#6aaee6", "#3474b8", None)
GOLD = "#e8c27a"            # crossover.py's S-type gold; its C-type blue is BLUE
BELT_AU = (1.6, 3.6)        # the span of the paper's strip, au


def gradient(stops):
    """A left-to-right gradient across the strip, from (offset, colour, opacity) stops."""
    return (f'<linearGradient id="strip" x1="{SX}" x2="{SX + SW}" gradientUnits="userSpaceOnUse">'
            + "".join(f'<stop offset="{o:.3f}" stop-color="{c}" stop-opacity="{a:.3f}"/>' for o, c, a in stops)
            + "</linearGradient>")


def catalog_strip():
    """The belt's density across 1.75 to 3.5 au from the catalog's proper orbits, two
    bins to a stop, on a square-root scale so the thin inner and outer edges still show
    and the Kirkwood gaps break it."""
    counts = PROFILE["count"]
    sums = [sum(counts[i:i + 2]) for i in range(0, len(counts), 2)]
    peak, n = max(sums), len(sums)
    stops = [((j + 0.5) / n, BLUE, (c / peak) ** 0.5) for j, c in enumerate(sums)]
    return [gradient(stops), f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="{SH / 2}" fill="url(#strip)"/>']


def belt_strip():
    """The paper's finding across 1.6 to 3.6 au: gold turning to blue over the corrected
    samples' mean 10-90% width, a white dot at their mean midpoint, and the snow line."""
    corrected = [c for c in COUNTS["belt"]["crossover"] if c["sample"] != "raw"]
    a50 = sum(c["a50"] for c in corrected) / len(corrected)
    width = sum(c["width"] for c in corrected) / len(corrected)
    lo, hi = BELT_AU
    frac = lambda a: (a - lo) / (hi - lo)
    x = lambda a: SX + SW * frac(a)
    snow = COUNTS["belt"]["snow_line_au"]
    return [gradient([(max(frac(a50 - width / 2), 0), GOLD, 0.9), (min(frac(a50 + width / 2), 1), BLUE, 0.9)]),
            f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="{SH / 2}" fill="url(#strip)"/>',
            f'<line x1="{x(snow):.1f}" y1="{SY - 3}" x2="{x(snow):.1f}" y2="{SY + SH + 3}" stroke="#e8c27a" stroke-width="1.2"/>',
            f'<circle cx="{x(a50):.1f}" cy="{SY + SH / 2}" r="3.4" fill="#eef4ff" stroke="#0f1e3d" stroke-width="1"/>']


def segments(widths, fills):
    """Segments of the given widths along the strip, 2px apart; a None fill is hollow."""
    parts, at = [], SX
    for w, fill in zip(widths, fills):
        drawn = max(w - 2, 1.5)
        if fill:
            parts.append(f'<rect x="{at:.1f}" y="{SY}" width="{drawn:.1f}" height="{SH}" rx="1.5" fill="{fill}"/>')
        else:
            parts.append(f'<rect x="{at + 0.6:.1f}" y="{SY + 0.6}" width="{max(drawn - 1.2, 0.5):.1f}" height="{SH - 1.2:.1f}" '
                         f'rx="1.5" fill="{DIM}" fill-opacity="0.15" stroke="{DIM}" stroke-width="1.2"/>')
        at += w
    return parts


def sources_strip():
    """All the sources split by tier, T1 to T4, as the sources chart splits each domain."""
    tiers = [sum(r["tiers"][t] for r in COUNTS["research"]) for t in range(4)]
    total = sum(tiers)
    return segments([SW * n / total for n in tiers if n], [f for n, f in zip(tiers, TIER_FILL) if n])


def skills_strip():
    """One segment for each category of skills (the library says how many, not their sizes)."""
    n = COUNTS["skill_categories"]
    return segments([SW / n] * n, [BLUE] * n)


STRIPS = {"catalog": catalog_strip, "belt": belt_strip, "sources": sources_strip, "skills": skills_strip}


def strip(name):
    """The strip for tile name over a faint track, growing in from the left as the number
    rolls (the snow line and midpoint grow with it)."""
    return "\n".join([f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="{SH / 2}" fill="{TRACK}" opacity="0.7"/>',
                      '<g class="grow" style="animation-delay:0.3s">', *STRIPS[name](), "</g>"])


for i, (name, (num, label, short, repo)) in enumerate(TILES.items()):
    body = f"""<g font-family="{FONT}">
{odometer(num, 20, 58, 44)}
<text x="20" y="90" font-size="20" fill="#dbe3f5">{label}</text>
</g>
{strip(name)}
</svg>
"""
    full = frame(i, f"{num} {label}, {repo}", body) + body
    body = f"""<g font-family="{FONT}" text-anchor="middle">
{odometer(num, W / 2, 66, 62, centred=True)}
<text x="{W / 2}" y="107" font-size="34" fill="#dbe3f5">{short}</text>
</g>
</svg>
"""
    compact = frame(i, f"{num} {short}", body) + body
    (OUT / f"{name}.svg").write_text(full, encoding="utf-8", newline="\n")
    (OUT / f"{name}-compact.svg").write_text(compact, encoding="utf-8", newline="\n")
    print(name)
