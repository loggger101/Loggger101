"""Generate the animated profile banner: a star drawn as light, an orbiting body, and the name.

`banner.svg` is the wide banner. `banner-compact.svg` is for phones, where the wide one
shrinks to about 350px and its two smaller lines fall under 8px: the star is smaller, and
the lines under the name are split so each can be twice the size. The README swaps it in
with <picture>, as it does for the panels.

    python tools/banner.py docs
"""
import random
import sys
from pathlib import Path

import panel
import star

H = 300
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
ALT = "Logan M Edwards, Astronomy and Astrophysics, Planetary Science"

# A shooting star crosses the empty top right, clear of the name and the star, once per
# cycle. It is invisible unless it is moving, so with reduced motion it never shows.
METEOR_START = (880, 18)           # where its tail starts
METEOR_TRAIL = (110, 40)           # tail to head, along its path
METEOR_RUN = (230, 84)             # how far it travels (same direction as the trail)
METEOR_CYCLE = 14                  # seconds between appearances
METEOR_SHARE = 0.08                # share of the cycle it is visible (about 1.1 s)


def render(w, glow_x, system, lines, meteor):
    """A w x H banner: the backdrop with its glow at glow_x (a share of w), the starfield,
    the shooting star if meteor, the star system (star.py's parts), then lines of text,
    each (x, y, size, bold, colour, text)."""
    rng = random.Random(42)
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" role="img" aria-label="{ALT}">')
    a(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="0.55" stop-color="#0f1e3d"/>
    <stop offset="1" stop-color="#112650"/>
  </linearGradient>
  <radialGradient id="glow" cx="{glow_x}" cy="0.35" r="0.5">
    <stop offset="0" stop-color="#1d3f74" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#1d3f74" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="0.85" cy="0.95" r="0.45">
    <stop offset="0" stop-color="#1d3f74" stop-opacity="0.5"/>
    <stop offset="1" stop-color="#1d3f74" stop-opacity="0"/>
  </radialGradient>
{star.DEFS}
</defs>
<style>
  .tw {{ animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%, 100% {{ opacity: 0.15; }} 50% {{ opacity: 1; }} }}
{star.STYLE}
  .t {{ font-family: {FONT}; }}
  .meteor {{ opacity: 0; animation: meteor {METEOR_CYCLE}s linear infinite; animation-delay: 3s; }}
  @keyframes meteor {{
    0% {{ transform: translate(0, 0); opacity: 0; }}
    1% {{ opacity: 0.9; }}
    {METEOR_SHARE * 100 * 0.7:.1f}% {{ opacity: 0.9; }}
    {METEOR_SHARE * 100:.1f}%, 100% {{ transform: translate({METEOR_RUN[0]}px, {METEOR_RUN[1]}px); opacity: 0; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ .tw, .meteor, {", ".join(star.ANIMATED)} {{ animation: none; }} }}
</style>""")
    # Rounded corners, to match the stat tiles
    a(f'<clipPath id="round"><rect width="{w}" height="{H}" rx="16"/></clipPath>')
    a('<g clip-path="url(#round)">')
    a(f'<rect width="{w}" height="{H}" fill="url(#bg)"/>')
    a(f'<rect width="{w}" height="{H}" fill="url(#glow)"/>')
    a(f'<rect width="{w}" height="{H}" fill="url(#glow2)"/>')

    # Static starfield, as dense as the wide banner's
    for _ in range(round(170 * w / 1200)):
        x, y = rng.uniform(0, w), rng.uniform(0, H)
        r = rng.choice([0.6, 0.7, 0.8, 0.9, 1.1, 1.3])
        op = rng.uniform(0.25, 0.8)
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{op:.2f}"/>')
    # Twinkling stars
    for _ in range(round(28 * w / 1200)):
        x, y = rng.uniform(0, w), rng.uniform(0, H)
        r = rng.choice([1.2, 1.4, 1.6])
        d = rng.uniform(0, 4)
        dur = rng.uniform(3, 6)
        a(f'<circle class="tw" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dbe7ff" style="animation-delay:-{d:.2f}s;animation-duration:{dur:.2f}s"/>')

    if meteor:
        # The shooting star. Its gradient is in user space: a line's bounding box has no
        # height, and a bounding-box gradient on it would not draw.
        tx, ty = METEOR_TRAIL
        a(f'<g transform="translate({METEOR_START[0]} {METEOR_START[1]})"><g class="meteor">'
          f'<linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{tx}" y2="{ty}">'
          f'<stop offset="0" stop-color="#9ccaf2" stop-opacity="0"/><stop offset="1" stop-color="#ffffff"/></linearGradient>'
          f'<line x1="0" y1="0" x2="{tx}" y2="{ty}" stroke="url(#trail)" stroke-width="1.6" stroke-linecap="round"/>'
          f'<circle cx="{tx}" cy="{ty}" r="1.8" fill="#ffffff"/></g></g>')

    out.extend(system)
    a("</g>")

    # Text, outside the clip so keep_clear sees it
    for x, y, size, bold, colour, text in lines:
        weight = ' font-weight="700"' if bold else ""
        a(f'<text class="t" x="{x}" y="{y}" font-size="{size}"{weight} fill="{colour}">{text}</text>')
    a("</svg>")
    return panel.keep_clear("\n".join(out) + "\n")


FILES = {
    # The star and its orbit at the banner's own layout (star.CX, star.CY), the name beside it.
    "banner.svg": render(1200, 0.3, star.system(), [
        (360, 138, 62, True, "#ffffff", "Logan M Edwards"),
        (362, 186, 26, False, "#aab6d3", "Astronomy &amp; Astrophysics  •  Planetary Science"),
        (362, 228, 20, False, "#93a0c4", "Florida Tech  •  loganmedwardsastrophy.com"),
    ], meteor=True),
    # Phones: the system at 0.6 scale on the left, and under the name each line its own.
    "banner-compact.svg": render(680, 0.15, star.nested(108, 150, 0.6), [
        (214, 104, 50, True, "#ffffff", "Logan M Edwards"),
        (216, 152, 28, False, "#aab6d3", "Astronomy &amp; Astrophysics"),
        (216, 188, 28, False, "#aab6d3", "Planetary Science"),
        (216, 236, 23, False, "#93a0c4", "Florida Tech"),
        (216, 266, 23, False, "#93a0c4", "loganmedwardsastrophy.com"),
    ], meteor=False),
}

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for name, svg in FILES.items():
    (out / name).write_text(svg, encoding="utf-8", newline="\n")
    print(name)
