"""The banner's star and its orbiting body, shared by banner.py and footer.py.

The system is drawn in its own 340 x 300 coordinate box centred on (170, 150), the
banner's layout. The animations scale about that fixed point (CSS transform-origin),
so a page that wants the system somewhere else, or smaller, places it with a nested
<svg> viewport (see `nested`) rather than a transform, which would move the origin.
"""

CX, CY = 170, 150
BOX_W, BOX_H = 340, 300

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
  @keyframes rays2 {{ 0%, 100% {{ opacity: 0.55; }} 50% {{ opacity: 0.9; }} }}"""

# Class names the page's reduced-motion rule must stop.
ANIMATED = (".breathe", ".rays", ".rays2")


def spike(length, width, angle):
    """A long thin diamond through the centre, white in the middle and clear at both tips."""
    return (f'<polygon points="{CX - length},{CY} {CX},{CY - width} {CX + length},{CY} {CX},{CY + width}" '
            f'fill="url(#spike)" transform="rotate({angle} {CX} {CY})"/>')


def system():
    """The orbit's far half, the star, then the near half, so the body passes in front."""
    cx, cy = CX, CY
    path = f"M {cx + 125} {cy} A 125 42 0 1 1 {cx - 125} {cy} A 125 42 0 1 1 {cx + 125} {cy}"
    main = "".join(spike(126, 3.2, ang) for ang in (0, 90))
    diag = "".join(spike(80, 2.2, ang) for ang in (45, 135))
    return [
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


def nested(x_centre, y_centre, scale):
    """The system centred at (x_centre, y_centre) and scaled, in its own viewport."""
    w, h = BOX_W * scale, BOX_H * scale
    return ([f'<svg x="{x_centre - w / 2:g}" y="{y_centre - h / 2:g}" width="{w:g}" height="{h:g}" '
             f'viewBox="0 0 {BOX_W} {BOX_H}" overflow="visible">']
            + system() + ["</svg>"])
