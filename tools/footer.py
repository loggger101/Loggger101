"""Generate the strip that closes the profile README (docs/footer.svg, docs/footer-compact.svg).

A slim version of the banner: the same background, a starfield, and the star with its
orbiting body at a third of the size, the same fraction of the way across as the
banner's star so the two line up. It carries no text and the README gives it empty
alt text, as decoration.

`footer.svg` is 1200 wide like the banner. At phone widths that leaves a strip about
24px tall, so `footer-compact.svg` is half as wide at the same height, and the README
swaps it in with <picture>, as it does for the tiles.
"""
import random
import sys
from pathlib import Path

import star

H = 84
SCALE = 0.3
OUT = Path(sys.argv[1])


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
    out.extend(star.nested(w * star.CX / 1200, H / 2, SCALE))
    a("</g>")
    a("</svg>")
    return "\n".join(out) + "\n"


for name, w in (("footer.svg", 1200), ("footer-compact.svg", 600)):
    (OUT / name).write_text(render(w, 7), encoding="utf-8", newline="\n")
    print(name)
