"""Generate the animated profile banner (docs/banner.svg) in the portfolio's og.jpg style."""
import math
import random
import sys

W, H = 1200, 300
rng = random.Random(42)

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Logan M Edwards, Astronomy and Astrophysics, Planetary Science">')
a("""<defs>
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
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#5ba3dc" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#5ba3dc" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  .tw { animation: tw 4s ease-in-out infinite; }
  @keyframes tw { 0%, 100% { opacity: 0.15; } 50% { opacity: 1; } }
  .pulse { animation: pulse 6s ease-in-out infinite; transform-origin: 170px 150px; }
  @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
  .t { font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
  @media (prefers-reduced-motion: reduce) { .tw, .pulse { animation: none; } }
</style>""")
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

# Orbit around the eight-point star, tilted ellipse
cx, cy = 170, 150
a(f'<g transform="rotate(-18 {cx} {cy})">')
a(f'<ellipse cx="{cx}" cy="{cy}" rx="125" ry="42" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>')
path = f"M {cx + 125} {cy} A 125 42 0 1 1 {cx - 125} {cy} A 125 42 0 1 1 {cx + 125} {cy}"
a(f'<circle r="4.5" fill="#e8c27a"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/></circle>')
a("</g>")

# Halo and eight-point star
a(f'<circle cx="{cx}" cy="{cy}" r="95" fill="url(#halo)"/>')
pts = []
for i in range(16):
    ang = -math.pi / 2 + i * math.pi / 8
    rad = 72 if i % 2 == 0 else 28
    pts.append(f"{cx + rad * math.cos(ang):.1f},{cy + rad * math.sin(ang):.1f}")
a(f'<polygon class="pulse" points="{" ".join(pts)}" fill="#5ba3dc"/>')

# Near half of the orbit, redrawn over the star so the body passes in front of it.
# The path runs clockwise from the right end, so its first half is the near (lower) arc.
a(f'<g transform="rotate(-18 {cx} {cy})">')
a(f'<path d="M {cx + 125} {cy} A 125 42 0 0 1 {cx - 125} {cy}" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>')
a(f'<circle r="4.5" fill="#e8c27a"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/>'
  '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" calcMode="discrete" values="1;0" keyTimes="0;0.5"/></circle>')
a("</g>")

# Text
a('<text class="t" x="360" y="138" font-size="62" font-weight="700" fill="#ffffff">Logan M Edwards</text>')
a('<text class="t" x="362" y="186" font-size="26" fill="#aab6d3">Astronomy &amp; Astrophysics  •  Planetary Science</text>')
a('<text class="t" x="362" y="226" font-size="18" fill="#7d89ad">Florida Tech  •  loganmedwardsastrophy.com</text>')
a("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("ok")
