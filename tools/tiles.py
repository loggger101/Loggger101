"""Generate the 'by the numbers' stat tiles (docs/stats/*.svg) in the banner's style.

Each tile comes in two versions. `<name>.svg` is the full tile for desktop widths.
`<name>-compact.svg` has a larger number and a short label, for phones, where four
tiles in a row leave each one about 80px wide; the README swaps it in with <picture>.
"""
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 270, 120
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

# name: (number, label, short label for the compact tile, repo)
TILES = {
    "catalog": ("1.57M", "asteroids cataloged", "asteroids cataloged", "AsteroidCatalog"),
    "belt": ("161,659", "classified asteroids analyzed", "asteroids analyzed", "asteroid-belt-gradient"),
    "star": ("84.3%", "spectral letter, top-1", "spectral letter", "star-spectral-classifier"),
    "drone": ("91.2%", "valid/invalid accuracy", "valid/invalid", "drone-target-id"),
}


def frame(i, label):
    rng = random.Random(100 + i)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, W - 8):.1f}" cy="{rng.uniform(8, H - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(14)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#1e1640"/></linearGradient></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="url(#g)" stroke="#2a3b63"/>
{stars}
"""


for i, (name, (num, label, short, repo)) in enumerate(TILES.items()):
    full = frame(i, f"{num} {label}, {repo}") + f"""<g font-family="{FONT}">
<text x="20" y="54" font-size="36" font-weight="700" fill="#5ba3dc">{num}</text>
<text x="20" y="80" font-size="17" fill="#dbe3f5">{label}</text>
<text x="20" y="103" font-size="13" fill="#93a0c4">{repo}</text>
</g>
</svg>
"""
    compact = frame(i, f"{num} {short}") + f"""<g font-family="{FONT}" text-anchor="middle">
<text x="{W / 2}" y="66" font-size="56" font-weight="700" fill="#5ba3dc">{num}</text>
<text x="{W / 2}" y="102" font-size="26" fill="#dbe3f5">{short}</text>
</g>
</svg>
"""
    (OUT / f"{name}.svg").write_text(full, encoding="utf-8", newline="\n")
    (OUT / f"{name}-compact.svg").write_text(compact, encoding="utf-8", newline="\n")
    print(name)
