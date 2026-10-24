"""The line-art glyphs and colours the link buttons (links.py) and section icons (icons.py)
share. Each glyph is drawn in an 18 x 18 box at the origin."""

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, NAVY = "#5ba3dc", "#dbe3f5", "#0b1020"
TILE, EDGE = "#13213f", "#2f4a7a"     # a button's or icon tile's fill and border

# Icons are drawn in an 18 x 18 box at the origin.
LINE = f'fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "globe": f'<circle cx="9" cy="9" r="7.5" {LINE}/><ellipse cx="9" cy="9" rx="3.2" ry="7.5" {LINE}/>'
             f'<path d="M1.8 6.5h14.4M1.8 11.5h14.4" {LINE}/>',
    "page": f'<path d="M4 1.5h6.5l4 4v11h-10.5z" {LINE}/><path d="M10.5 1.5v4h4M6.8 9.5h5M6.8 12.5h5" {LINE}/>',
    "mail": f'<rect x="1.5" y="3.5" width="15" height="11" rx="2" {LINE}/><path d="M2 4.5l7 5.5 7-5.5" {LINE}/>',
    "linkedin": f'<rect width="18" height="18" rx="3.5" fill="{BLUE}"/><rect x="3.4" y="7.1" width="2.4" height="7.5" fill="{NAVY}"/>'
                f'<circle cx="4.6" cy="4.5" r="1.45" fill="{NAVY}"/>'
                f'<path d="M7.6 7.1h2.3v1.1c.4-.7 1.3-1.35 2.55-1.35 2.25 0 2.85 1.5 2.85 3.45v4.3h-2.4v-3.75c0-1-.2-1.9-1.3-1.9s-1.6.75-1.6 1.9v3.75h-2.45z" fill="{NAVY}"/>',
    "kaggle": f'<rect width="18" height="18" rx="3.5" fill="{BLUE}"/>'
              f'<text x="9" y="13.6" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="{NAVY}">k</text>',
    # The section icons (icons.py).
    # A lumpy asteroid with two craters.
    "asteroid": f'<path d="M4.6 4.2C6.6 2.2 10.4 1.9 12.8 3.4c2.7 1.6 3.9 4.4 3.1 7.3-.6 2.4-2 3.3-3.4 4.4'
                f'-1.9 1.4-4.4 1.2-6.4.4C3.6 14.6 2 12.6 1.9 10c-.1-2.3 1-4.1 2.7-5.8z" {LINE}/>'
                f'<circle cx="7.4" cy="7.6" r="1.9" {LINE}/><circle cx="11.8" cy="11.3" r="1.2" {LINE}/>'
                f'<circle cx="12.2" cy="6.4" r="0.5" fill="{BLUE}"/>',
    # The Sun with a dotted belt round it, tilted like the banner's orbit.
    "belt": f'<ellipse cx="9" cy="9" rx="7.6" ry="3.3" transform="rotate(-20 9 9)" fill="none" stroke="{BLUE}" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-dasharray="0.01 2.5"/><circle cx="9" cy="9" r="2.6" fill="{BLUE}"/>',
    # Three layers of a network; the nodes are filled with the tile so the edges stop at them.
    "network": f'<path d="M3 5 9 3M3 5 9 9M3 5 9 15M3 13 9 3M3 13 9 9M3 13 9 15M9 3 15 9M9 9 15 9M9 15 15 9" '
               f'stroke="{BLUE}" stroke-width="1" stroke-opacity="0.8"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{TILE}" stroke="{BLUE}" stroke-width="1.4"/>'
                         for x, y in ((3, 5), (3, 13), (9, 3), (9, 9), (9, 15), (15, 9))),
    # Earth inside a tilted orbit: the back half passes behind it, the front half in front,
    # with a satellite on the front half. (Ends of the major axis: 9 +- 7.6(cos 25, -sin 25).)
    "orbit": f'<ellipse cx="9" cy="9" rx="7.6" ry="3.4" transform="rotate(-25 9 9)" {LINE} stroke-opacity="0.55"/>'
             f'<circle cx="9" cy="9" r="3.7" fill="{TILE}" stroke="{BLUE}" stroke-width="1.6"/>'
             f'<path d="M2.11 12.21A7.6 3.4 -25 0 0 15.89 5.79" {LINE}/>'
             f'<circle cx="4.65" cy="13.44" r="1.7" fill="{BLUE}" stroke="{TILE}" stroke-width="0.8"/>',
    # A heart with a pulse across it.
    "heart": f'<path d="M9 15.6C4.2 12.4 1.6 9.6 1.6 6.4a3.7 3.7 0 0 1 7.4-.9 3.7 3.7 0 0 1 7.4.9c0 3.2-2.6 6-7.4 9.2z" {LINE}/>'
             f'<path d="M3.6 8.9h2.6l1.3-2.1 2 4.3 1.3-2.2h3.6" {LINE}/>',
    # The activity panel in small: two orbits that stop short of twelve o'clock, round a star.
    # (Each arc runs clockwise from the top for 300 degrees.)
    "rings": f'<path d="M9 1.4A7.6 7.6 0 1 1 2.42 5.2M9 4.4A4.6 4.6 0 1 1 5.02 6.7" {LINE}/>'
             f'<circle cx="9" cy="9" r="1.5" fill="{BLUE}"/><circle cx="15.58" cy="12.8" r="1.5" fill="{BLUE}"/>'
             f'<circle cx="7.43" cy="13.32" r="1.2" fill="{BLUE}"/>',
    # Earth, with an asteroid going by, its trail behind it.
    "flyby": f'<circle cx="7" cy="11" r="4.6" {LINE}/><path d="M2.6 9.6q4.4-1.6 8.8 0" {LINE} stroke-opacity="0.55"/>'
             f'<path d="M15.6 4.2 17.3 2.5M13.4 2.4l1-1M17.4 6.5l1-1" {LINE} stroke-opacity="0.6"/>'
             f'<circle cx="14.2" cy="5.6" r="1.8" fill="{BLUE}"/>',
    # Angle brackets round a slash.
    "code": f'<path d="M5.5 4.5 1.5 9l4 4.5M12.5 4.5l4 4.5-4 4.5M10.6 2.8 7.4 15.2" {LINE}/>',
    # A box with an arrow leaving it.
    "external": f'<path d="M7.5 3.5h-4v11h11v-4" {LINE}/><path d="M10.5 2.5h5v5M15.5 2.5 8.5 9.5" {LINE}/>',
}
