"""Generate the animated profile banner (docs/banner.svg): a star drawn as light, an orbiting body, and the name."""
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
  <radialGradient id="corona" cx="0.5" cy="0.5" r="0.5">
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
  <filter id="bloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<style>
  .tw { animation: tw 4s ease-in-out infinite; }
  @keyframes tw { 0%, 100% { opacity: 0.15; } 50% { opacity: 1; } }
  .breathe { animation: breathe 6s ease-in-out infinite; transform-origin: 170px 150px; }
  @keyframes breathe { 0%, 100% { transform: scale(1); opacity: 0.85; } 50% { transform: scale(1.08); opacity: 1; } }
  .rays { animation: rays 6s ease-in-out infinite; transform-origin: 170px 150px; }
  @keyframes rays { 0%, 100% { transform: scale(0.94); opacity: 0.8; } 50% { transform: scale(1.04); opacity: 1; } }
  .rays2 { animation: rays2 4.5s ease-in-out infinite; transform-origin: 170px 150px; }
  @keyframes rays2 { 0%, 100% { opacity: 0.55; } 50% { opacity: 0.9; } }
  .t { font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
  @media (prefers-reduced-motion: reduce) { .tw, .breathe, .rays, .rays2 { animation: none; } }
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

# Orbit around the eight-point star, tilted ellipse
cx, cy = 170, 150
a(f'<g transform="rotate(-18 {cx} {cy})">')
a(f'<ellipse cx="{cx}" cy="{cy}" rx="125" ry="42" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>')
path = f"M {cx + 125} {cy} A 125 42 0 1 1 {cx - 125} {cy} A 125 42 0 1 1 {cx + 125} {cy}"
a(f'<circle r="5" fill="url(#body)"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/></circle>')
a("</g>")

# The star, drawn as light: a corona, diffraction spikes and a white-hot core.
# Each spike is a long thin diamond through the centre, filled with a gradient
# that is white at the middle and clear at both tips, then rotated into place.
def spike(length, width, angle):
    return (f'<polygon points="{cx - length},{cy} {cx},{cy - width} {cx + length},{cy} {cx},{cy + width}" '
            f'fill="url(#spike)" transform="rotate({angle} {cx} {cy})"/>')


a(f'<circle class="breathe" cx="{cx}" cy="{cy}" r="135" fill="url(#corona)"/>')
main = "".join(spike(126, 3.2, ang) for ang in (0, 90))
diag = "".join(spike(80, 2.2, ang) for ang in (45, 135))
a(f'<g class="rays"><g filter="url(#bloom)" opacity="0.55">{main}</g><g filter="url(#soft)">{main}</g></g>')
a(f'<g class="rays2" filter="url(#soft)">{diag}</g>')
a(f'<circle class="breathe" cx="{cx}" cy="{cy}" r="24" fill="url(#core)"/>')
a(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#ffffff"/>')

# Near half of the orbit, redrawn over the star so the body passes in front of it.
# The path runs clockwise from the right end, so its first half is the near (lower) arc.
a(f'<g transform="rotate(-18 {cx} {cy})">')
a(f'<path d="M {cx + 125} {cy} A 125 42 0 0 1 {cx - 125} {cy}" fill="none" stroke="#8fb6e8" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>')
a(f'<circle r="5" fill="url(#body)"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/>'
  '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" calcMode="discrete" values="1;0" keyTimes="0;0.5"/></circle>')
a("</g>")

# Text
a('<text class="t" x="360" y="138" font-size="62" font-weight="700" fill="#ffffff">Logan M Edwards</text>')
a('<text class="t" x="362" y="186" font-size="26" fill="#aab6d3">Astronomy &amp; Astrophysics  •  Planetary Science</text>')
a('<text class="t" x="362" y="228" font-size="20" fill="#93a0c4">Florida Tech  •  loganmedwardsastrophy.com</text>')
a("</g>")
a("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("ok")
