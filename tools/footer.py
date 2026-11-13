"""Generate the strip that closes the profile README (docs/footer.svg, docs/footer-compact.svg).

A slim version of the banner: the same background, a starfield, and the star with its
orbiting body at a third of the size, the same fraction of the way across as the
banner's star so the two line up. The star stands for the Sun, and to its right the
inner solar system runs out to scale (across; the belt's thickness isn't): Earth at
1 au, Mars at 1.52, then the main belt as points whose density follows the catalog's
proper semimajor axes (belt_profile.json), so the Kirkwood gaps open where they really
are. Each point is gold or blue by the share of bright (S-like) and dark (C-like) bodies
with a measured albedo at its distance, so the belt turns from gold to blue outward.
It carries no text; the README's alt text says what it shows.

`footer.svg` is 1200 wide like the banner. At phone widths that leaves a strip about
24px tall, so `footer-compact.svg` is half as wide at the same height, and the README
swaps it in with <picture>, as it does for the tiles.
"""
import json
import random
import sys
from pathlib import Path

import star

H = 84
SCALE = 0.3
OUT = Path(sys.argv[1])

PROFILE = json.loads((Path(__file__).parent / "belt_profile.json").read_text(encoding="utf-8"))
LO, HI, STEP = PROFILE["au"]
EARTH, MARS = 1.0, 1.524        # semimajor axes, au
SMOOTH = 2                      # bins either side when reading the bright share
GOLD, BLUE = (f"#{r:02x}{g:02x}{b:02x}" for r, g, b in (star.S_TYPE, star.C_TYPE))


def bright_share():
    """Per bin, the share of bodies with a measured albedo that are bright, over the bin
    and SMOOTH either side (a lone body shouldn't paint a bin); 0.5 where there are none."""
    b, d = PROFILE["bright"], PROFILE["dark"]
    out = []
    for i in range(len(b)):
        lo, hi = max(0, i - SMOOTH), i + SMOOTH + 1
        n = sum(b[lo:hi]) + sum(d[lo:hi])
        out.append(sum(b[lo:hi]) / n if n else 0.5)
    return out


def mix(t):
    """The colour t of the way from C-type blue (0) to S-type gold (1)."""
    return "#" + "".join(f"{round(c + (s - c) * t):02x}" for s, c in zip(star.S_TYPE, star.C_TYPE))


HAZE_BINS = 3                   # profile bins per stop of the haze


def haze(x0, x1, counts, share):
    """A soft glow under the points from x0 to x1, as bright at each distance as the belt
    is dense there and tinted by its bright share, so the belt reads as one band, gaps
    and all, where the points are too small to see (a phone)."""
    sums = [sum(counts[i:i + HAZE_BINS]) for i in range(0, len(counts), HAZE_BINS)]
    peak, n = max(sums), len(sums)
    stops = "".join(
        f'<stop offset="{(j + 0.5) / n:.3f}" stop-color="{mix(share[min(j * HAZE_BINS + 1, len(share) - 1)])}" '
        f'stop-opacity="{0.4 * s / peak:.3f}"/>' for j, s in enumerate(sums))
    return [
        f'<linearGradient id="haze" x1="{x0:.1f}" x2="{x1:.1f}" gradientUnits="userSpaceOnUse">{stops}</linearGradient>',
        '<filter id="hazeblur" x="-5%" y="-100%" width="110%" height="300%"><feGaussianBlur stdDeviation="1.5 6"/></filter>',
        f'<rect x="{x0:.1f}" y="{H / 2 - 9}" width="{x1 - x0:.1f}" height="18" rx="9" fill="url(#haze)" filter="url(#hazeblur)"/>',
    ]


def belt(w, sun_x, rng):
    """The planets and the belt, to scale across from the Sun at sun_x to HI au at the
    right edge. Points are drawn in proportion to the profile's counts, each placed at
    random within its bin, and spread up and down more the farther out they sit."""
    k = (w - 14 - sun_x) / HI
    mid = H / 2
    counts, share = PROFILE["count"], bright_share()
    picks = rng.choices(range(len(counts)), weights=counts, k=int(w * 0.8))
    groups = {GOLD: [], BLUE: []}
    for i in sorted(picks):
        a = LO + (i + rng.random()) * STEP
        spread = 3 + 7 * (a - LO) / (HI - LO)
        y = min(H - 5, max(5, rng.gauss(mid, spread)))
        colour = GOLD if rng.random() < share[i] else BLUE
        groups[colour].append(f'<circle cx="{sun_x + k * a:.1f}" cy="{y:.1f}" r="{rng.choice([0.5, 0.6, 0.7, 0.8, 1.0])}" '
                              f'opacity="{rng.uniform(0.35, 0.9):.2f}"/>')
    ex, mx = sun_x + k * EARTH, sun_x + k * MARS
    return [
        *haze(sun_x + k * LO, sun_x + k * HI, counts, share),
        f'<circle cx="{ex:.1f}" cy="{mid}" r="7" fill="#5ba3dc" opacity="0.18"/>',
        f'<circle cx="{ex:.1f}" cy="{mid}" r="2.6" fill="#8cc4ff"/>',
        f'<circle cx="{mx:.1f}" cy="{mid}" r="5" fill="#d9744a" opacity="0.15"/>',
        f'<circle cx="{mx:.1f}" cy="{mid}" r="2" fill="#e08a5f"/>',
        *(f'<g fill="{colour}">' + "".join(dots) + "</g>" for colour, dots in groups.items()),
    ]


def render(w, seed):
    rng = random.Random(seed)
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" aria-hidden="true">')
    a(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="0.55" stop-color="#0f1e3d"/>
    <stop offset="1" stop-color="#112650"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.14" cy="0.5" r="0.3">
    <stop offset="0" stop-color="#1d3f74" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#1d3f74" stop-opacity="0"/>
  </radialGradient>
{star.DEFS}
</defs>
<style>
  .tw {{ animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%, 100% {{ opacity: 0.15; }} 50% {{ opacity: 1; }} }}
{star.STYLE}
  @media (prefers-reduced-motion: reduce) {{ .tw, {", ".join(star.ANIMATED)} {{ animation: none; }} }}
</style>""")
    a(f'<clipPath id="round"><rect width="{w}" height="{H}" rx="16"/></clipPath>')
    a('<g clip-path="url(#round)">')
    a(f'<rect width="{w}" height="{H}" fill="url(#bg)"/>')
    a(f'<rect width="{w}" height="{H}" fill="url(#glow)"/>')
    for _ in range(w // 20):
        x, y = rng.uniform(0, w), rng.uniform(0, H)
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.choice([0.6, 0.8, 1.0, 1.2])}" fill="#fff" opacity="{rng.uniform(0.25, 0.8):.2f}"/>')
    for _ in range(w // 120):
        x, y = rng.uniform(0, w), rng.uniform(0, H)
        a(f'<circle class="tw" cx="{x:.1f}" cy="{y:.1f}" r="{rng.choice([1.2, 1.4])}" fill="#dbe7ff" '
          f'style="animation-delay:-{rng.uniform(0, 4):.2f}s;animation-duration:{rng.uniform(3, 6):.2f}s"/>')
    # The banner's star sits at star.CX of its 1200px width; keep the same fraction.
    sun_x = w * star.CX / 1200
    out.extend(belt(w, sun_x, rng))
    out.extend(star.nested(sun_x, H / 2, SCALE))
    a("</g>")
    a("</svg>")
    return "\n".join(out) + "\n"


for name, w in (("footer.svg", 1200), ("footer-compact.svg", 600)):
    (OUT / name).write_text(render(w, 7), encoding="utf-8", newline="\n")
    print(name)
