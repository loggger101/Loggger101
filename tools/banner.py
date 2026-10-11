"""Generate the animated profile banner (docs/banner.svg): a star drawn as light, an orbiting body, and the name."""
import random
import sys

import star

W, H = 1200, 300
rng = random.Random(42)

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Logan M Edwards, Astronomy and Astrophysics, Planetary Science">')
a(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="0.55" stop-color="#0f1e3d"/>
    <stop offset="1" stop-color="#1e1640"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.3" cy="0.35" r="0.5">
    <stop offset="0" stop-color="#1d3f74" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#1d3f74" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="0.85" cy="0.95" r="0.45">
    <stop offset="0" stop-color="#3b2470" stop-opacity="0.5"/>
    <stop offset="1" stop-color="#3b2470" stop-opacity="0"/>
  </radialGradient>
{star.DEFS}
</defs>
<style>
  .tw {{ animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%, 100% {{ opacity: 0.15; }} 50% {{ opacity: 1; }} }}
{star.STYLE}
  .t {{ font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
  @media (prefers-reduced-motion: reduce) {{ .tw, {", ".join(star.ANIMATED)} {{ animation: none; }} }}
</style>""")
# Rounded corners, to match the stat tiles
a(f'<clipPath id="round"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
a('<g clip-path="url(#round)">')
a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
a(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
a(f'<rect width="{W}" height="{H}" fill="url(#glow2)"/>')

# Static starfield
for _ in range(170):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    r = rng.choice([0.6, 0.7, 0.8, 0.9, 1.1, 1.3])
    op = rng.uniform(0.25, 0.8)
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{op:.2f}"/>')
# Twinkling stars
for _ in range(28):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    r = rng.choice([1.2, 1.4, 1.6])
    d = rng.uniform(0, 4)
    dur = rng.uniform(3, 6)
    a(f'<circle class="tw" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dbe7ff" style="animation-delay:-{d:.2f}s;animation-duration:{dur:.2f}s"/>')

# The star and its orbit, at the banner's own layout (star.CX, star.CY)
out.extend(star.system())

# Text
a('<text class="t" x="360" y="138" font-size="62" font-weight="700" fill="#ffffff">Logan M Edwards</text>')
a('<text class="t" x="362" y="186" font-size="26" fill="#aab6d3">Astronomy &amp; Astrophysics  •  Planetary Science</text>')
a('<text class="t" x="362" y="228" font-size="20" fill="#93a0c4">Florida Tech  •  loganmedwardsastrophy.com</text>')
a("</g>")
a("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("ok")
