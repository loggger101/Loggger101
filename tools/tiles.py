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
"""
import json
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 270, 120
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
# Advance widths in Segoe UI Bold, in ems (measured with Pillow; its digits are all one width).
ADVANCE = {**dict.fromkeys("0123456789", 0.575), ",": 0.271, ".": 0.271, "M": 0.957}
ROLL = 1.8              # seconds a digit column spins

# The catalog and belt numbers are fixed by the releases they come from. The two that grow
# are in counts.json, which refresh_counts.py keeps current.
COUNTS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))

# name: (number, label, short label for the compact tile, repo)
TILES = {
    "catalog": ("1.57M", "asteroids cataloged", "asteroids", "AsteroidCatalog"),
    "belt": ("161,659", "asteroids analyzed", "analyzed", "asteroid-belt-gradient"),
    "sources": (f"{COUNTS['sources']:,}", "research sources", "sources", "General_Research"),
    "skills": (f"{COUNTS['skills']:,}", "agent skills", "agent skills", "Hermes_Skills"),
}


def frame(i, label):
    rng = random.Random(100 + i)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, W - 8):.1f}" cy="{rng.uniform(8, H - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(14)
    )
    # Three stars twinkle, as in the banner; drawn after the still ones, so those stay put.
    twinkles = "".join(
        f'<circle class="tw" cx="{rng.uniform(8, W - 8):.1f}" cy="{rng.uniform(8, H - 8):.1f}" r="1.2" fill="#dbe7ff" '
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
  @media (prefers-reduced-motion: reduce) {{ .tw, .roll {{ animation: none; }} }}
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


for i, (name, (num, label, short, repo)) in enumerate(TILES.items()):
    full = frame(i, f"{num} {label}, {repo}") + f"""<g font-family="{FONT}">
{odometer(num, 20, 62, 44)}
<text x="20" y="96" font-size="20" fill="#dbe3f5">{label}</text>
</g>
</svg>
"""
    compact = frame(i, f"{num} {short}") + f"""<g font-family="{FONT}" text-anchor="middle">
{odometer(num, W / 2, 70, 62, centred=True)}
<text x="{W / 2}" y="106" font-size="30" fill="#dbe3f5">{short}</text>
</g>
</svg>
"""
    (OUT / f"{name}.svg").write_text(full, encoding="utf-8", newline="\n")
    (OUT / f"{name}-compact.svg").write_text(compact, encoding="utf-8", newline="\n")
    print(name)
