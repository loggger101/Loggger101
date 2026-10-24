"""Generate the link buttons under the banner (docs/links/*.svg) in the tiles' style.

Each button is its own SVG so each can be its own link. The label width is measured
with Segoe UI Bold, the font GitHub's Windows viewers get, and padded slightly so the
Helvetica/Arial fallbacks on other systems still fit (checked with each).
"""
import sys
from pathlib import Path

from PIL import ImageFont

from glyphs import FONT, ICONS, TEXT

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
MEASURE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 100)
H, SIZE, PAD, ICON, GAP = 36, 15, 14, 18, 8

# name: (label, icon, alt text)
LINKS = {
    "website": ("Website", "globe", "Website: loganmedwardsastrophy.com"),
    "cv": ("CV", "page", "CV (PDF)"),
    "linkedin": ("LinkedIn", "linkedin", "LinkedIn: logan-edwards"),
    "kaggle": ("Kaggle", "kaggle", "Kaggle: loggger"),
    "contact": ("Contact form", "mail", "Contact form on loganmedwardsastrophy.com"),
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
