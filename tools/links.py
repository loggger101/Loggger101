"""Generate the link buttons under the banner (docs/links/*.svg) in the tiles' style.

Each button is its own SVG so each can be its own link. The label width is measured
with Segoe UI Bold, the font GitHub's Windows viewers get, and padded slightly so the
Helvetica/Arial fallbacks on other systems still fit (checked with each).
"""
import sys
from pathlib import Path

from PIL import ImageFont

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MEASURE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 100)
H, SIZE, PAD, ICON, GAP = 36, 15, 14, 18, 8
BLUE, TEXT, NAVY = "#5ba3dc", "#dbe3f5", "#0b1020"

# Icons are drawn in an 18 x 18 box at the origin.
LINE = f'fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "globe": f'<circle cx="9" cy="9" r="7.5" {LINE}/><ellipse cx="9" cy="9" rx="3.2" ry="7.5" {LINE}/>'
             f'<path d="M1.8 6.5h14.4M1.8 11.5h14.4" {LINE}/>',
    "page": f'<path d="M4 1.5h6.5l4 4v11h-10.5z" {LINE}/><path d="M10.5 1.5v4h4M6.8 9.5h5M6.8 12.5h5" {LINE}/>',
    "linkedin": f'<rect width="18" height="18" rx="3.5" fill="{BLUE}"/><rect x="3.4" y="7.1" width="2.4" height="7.5" fill="{NAVY}"/>'
                f'<circle cx="4.6" cy="4.5" r="1.45" fill="{NAVY}"/>'
                f'<path d="M7.6 7.1h2.3v1.1c.4-.7 1.3-1.35 2.55-1.35 2.25 0 2.85 1.5 2.85 3.45v4.3h-2.4v-3.75c0-1-.2-1.9-1.3-1.9s-1.6.75-1.6 1.9v3.75h-2.45z" fill="{NAVY}"/>',
    "kaggle": f'<rect width="18" height="18" rx="3.5" fill="{BLUE}"/>'
              f'<text x="9" y="13.6" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="{NAVY}">k</text>',
}

# name: (label, icon, alt text)
LINKS = {
    "website": ("Website", "globe", "Website: loganmedwardsastrophy.com"),
    "cv": ("CV", "page", "CV (PDF)"),
    "linkedin": ("LinkedIn", "linkedin", "LinkedIn: logan-edwards"),
    "kaggle": ("Kaggle", "kaggle", "Kaggle: loggger"),
}

for name, (label, icon, alt) in LINKS.items():
    text_w = MEASURE.getlength(label) * SIZE / 100 * 1.03   # 3% slack: Arial, the usual fallback, measures within 1.5px
    w = round(PAD + ICON + GAP + text_w + PAD)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" role="img" aria-label="{alt}">
<rect x="0.75" y="0.75" width="{w - 1.5}" height="{H - 1.5}" rx="{H / 2 - 0.75}" fill="#13213f" stroke="#2f4a7a" stroke-width="1.5"/>
<g transform="translate({PAD} {(H - ICON) / 2})">{ICONS[icon]}</g>
<text x="{PAD + ICON + GAP}" y="{H / 2 + SIZE * 0.35:.1f}" font-family="{FONT}" font-size="{SIZE}" font-weight="700" fill="{TEXT}">{label}</text>
</svg>
"""
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8", newline="\n")
    print(name, w)
