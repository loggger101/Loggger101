"""Generate the break-even chart (docs/breakeven.svg, docs/breakeven-compact.svg): where
economicspace's asteroid-mining pipeline stands, one row for each destination it can
deliver to.

Each row is that destination's latest full-catalog run: what the best mission there costs
for each dollar its cargo earns (the filled dot) and what the median asteroid's mission
does (the open dot), on a log scale with break-even, 1x, marked. Left of the line pays for
itself. Beside each row, the ratio and the winning asteroid with its taxonomy class.

The numbers are refresh_counts.py's, read from the destinations table in economicspace's
README and kept in tools/counts.json ("economics"), so this draws the same thing until
they change. When the chart loads, each best dot slides in from the median's place, so the
eye follows the gap between the typical body and the best one; with reduced motion it is
drawn finished.

`breakeven.svg` is for desktop widths. `breakeven-compact.svg` drops the winners and uses
larger text, for phones; the README swaps it in with <picture>.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

import panel

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM, GOLD, GREEN = "#5ba3dc", "#dbe3f5", "#7d8fb3", "#e8c27a", "#5fbf8f"

ROWS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["economics"]
NAMES = {"mars_surface": "Mars surface", "lunar_surface": "Lunar surface", "mars_orbit": "Mars orbit",
         "cislunar": "Cislunar", "geo": "GEO", "gto": "GTO", "leo": "LEO", "earth_surface": "Earth surface"}
# Where each delivers to, as a sentence says it.
PLACES = {"mars_surface": "the surface of Mars", "lunar_surface": "the Moon's surface", "mars_orbit": "Mars orbit",
          "cislunar": "cislunar space", "geo": "GEO", "gto": "GTO", "leo": "LEO", "earth_surface": "Earth"}
LO, HI = 0.5, 30000     # the axis, in cost per dollar of revenue
BEST = min(ROWS, key=lambda r: r["best"])


def name(dest):
    return NAMES.get(dest, dest.replace("_", " ").capitalize())


def place(dest):
    return PLACES.get(dest, name(dest))


def ratio(x):
    """1.09x, 17.0x, 6,154x: three figures or so, as the table rounds them."""
    if x < 10:
        return f"{x:.2f}×"
    if x < 100:
        return f"{x:.1f}×"
    return f"{x:,.0f}×"


def paying(rows):
    """The places whose best mission earns more than it costs, best first."""
    return [place(r["dest"]) for r in sorted(rows, key=lambda r: r["best"]) if r["best"] < 1]


def listed(words):
    return words[0] if len(words) == 1 else f"{', '.join(words[:-1])} and {words[-1]}"


def verdict(rows):
    """The chart's answer, from the numbers: none of the rows is left of the line yet, or which are."""
    pay = paying(rows)
    if not pay:
        return "No destination breaks even yet."
    return (f"The best mission to {pay[0]} breaks even." if len(pay) == 1
            else f"The best missions to {listed(pay)} break even.")


def short_verdict(rows):
    """verdict() short enough for a phone."""
    n = len(paying(rows))
    return "No destination breaks even yet." if not n else f"{n} destination{'s' if n > 1 else ''} break{'s' if n == 1 else ''} even."


def clause(rows):
    """How the README's sentence above the chart ends ("...a mission pays for itself; none does yet.")."""
    pay = paying(rows)
    if not pay:
        return "none does yet"
    return f"the best mission to {pay[0]} does" if len(pay) == 1 else f"the best missions to {listed(pay)} do"


VERDICT = verdict(ROWS)
ALT = (f"Where the asteroid-mining pipeline stands: {VERDICT[0].lower() + VERDICT[1:-1]}. Cost per dollar earned, "
       "best mission and median asteroid, from economicspace's latest full-catalog runs: "
       + "; ".join(f"{name(r['dest'])} {ratio(r['best'])} ({r['winner']}), median {ratio(r['median'])}" for r in ROWS)
       + ".")


def background(w, h, seed):
    return panel.background(w, h, seed, ALT, rules=(
        ".slide { animation: slide 1.4s cubic-bezier(0.2, 0.7, 0.2, 1) both; }",
        "@keyframes slide { from { transform: translateX(var(--from)); } }",
        *panel.FADE,
    ), animated=("slide", "fade"))


def render(w, seed, pad, big, size, row_gap, name_w, track_w, with_winners):
    head = pad + big * 0.8
    top = head + size * 1.6 + size * 0.9 + row_gap * 1.3
    h = round(top + (len(ROWS) - 1) * row_gap + row_gap * 0.9 + size * 3.2 + pad * 0.6)
    x0 = pad + name_w
    # A ratio off the axis is drawn at its end; the number beside the row still says it.
    at = lambda v: x0 + track_w * math.log10(min(max(v, LO), HI) / LO) / math.log10(HI / LO)
    parts = [background(w, h, seed), f'<g font-family="{FONT}">',
             f'<text x="{pad}" y="{head:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">{ratio(BEST["best"])}</text>',
             f'<text x="{pad}" y="{head + size * 1.5:.1f}" font-size="{size}" fill="{TEXT}">'
             + (f'cost per dollar earned, at best: {html.escape(BEST["winner"])} to {html.escape(place(BEST["dest"]))}'
                if with_winners else "cost per dollar earned, at best") + '</text>',
             f'<text x="{pad}" y="{head + size * 2.6:.1f}" font-size="{size * 0.8:.1f}" fill="{DIM}">'
             + html.escape(f"{VERDICT} One row for each, from economicspace's latest full-catalog runs."
                           if with_winners else short_verdict(ROWS), quote=False) + '</text>']
    bottom = top + (len(ROWS) - 1) * row_gap + row_gap * 0.6
    # The side of the line where a mission pays, and the line itself.
    parts.append(f'<rect x="{at(LO):.1f}" y="{top - row_gap * 0.7:.1f}" width="{at(1) - at(LO):.1f}" '
                 f'height="{bottom - top + row_gap * 0.7:.1f}" fill="{GREEN}" fill-opacity="0.10"/>')
    parts.append(f'<line x1="{at(1):.1f}" y1="{top - row_gap * 0.7:.1f}" x2="{at(1):.1f}" y2="{bottom:.1f}" '
                 f'stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    parts.append(f'<text x="{at(1) + 6:.1f}" y="{top - row_gap * 0.7 + size * 0.2:.1f}" font-size="{size * 0.75:.1f}" '
                 f'fill="{GOLD}">break-even</text>')
    # The decades along the bottom; on phones the big ones are written short to fit.
    for v in (1, 10, 100, 1000, 10000):
        label = f"{v:,}×" if with_winners or v < 1000 else f"{v // 1000}k×"
        parts.append(f'<line x1="{at(v):.1f}" y1="{bottom:.1f}" x2="{at(v):.1f}" y2="{bottom + 6:.1f}" stroke="{DIM}" stroke-width="1.2"/>')
        parts.append(f'<text x="{at(v):.1f}" y="{bottom + 6 + size * 1.1:.1f}" text-anchor="middle" font-size="{size * 0.8:.1f}" '
                     f'fill="{GOLD if v == 1 else DIM}">{label}</text>')
    for k, r in enumerate(ROWS):
        y = top + k * row_gap
        xb, xm = at(r["best"]), at(r["median"])
        delay = f"animation-delay:{0.2 + 0.1 * k:.2f}s"
        parts.append(f'<text x="{pad}" y="{y + size * 0.35:.1f}" font-size="{size}" fill="#b9c6e4">{name(r["dest"])}</text>')
        parts.append(f'<line x1="{at(LO):.1f}" y1="{y:.1f}" x2="{at(HI):.1f}" y2="{y:.1f}" stroke="#2a3b63" stroke-width="1"/>')
        parts.append(f'<line class="fade" x1="{xb:.1f}" y1="{y:.1f}" x2="{xm:.1f}" y2="{y:.1f}" stroke="{BLUE}" '
                     f'stroke-opacity="0.45" stroke-width="{size * 0.25:.1f}" stroke-linecap="round" style="{delay}"/>')
        parts.append(f'<circle cx="{xm:.1f}" cy="{y:.1f}" r="{size * 0.3:.1f}" fill="#0f1e3d" stroke="{DIM}" stroke-width="2"/>')
        parts.append(f'<circle class="slide" cx="{xb:.1f}" cy="{y:.1f}" r="{size * 0.36:.1f}" fill="{BLUE}" '
                     f'style="--from:{xm - xb:.1f}px;{delay}"/>')
        parts.append(f'<text x="{x0 + track_w + size * 4.2:.1f}" y="{y + size * 0.35:.1f}" text-anchor="end" font-size="{size}" '
                     f'fill="{TEXT}">{ratio(r["best"])}</text>')
        if with_winners:
            parts.append(f'<text x="{x0 + track_w + size * 5:.1f}" y="{y + size * 0.35:.1f}" font-size="{size * 0.9:.1f}" '
                         f'fill="#b9c6e4">{html.escape(r["winner"])}</text>')
    # What the two dots are.
    ly = bottom + 6 + size * 2.7
    parts.append(f'<circle cx="{pad + size * 0.4:.1f}" cy="{ly - size * 0.3:.1f}" r="{size * 0.36:.1f}" fill="{BLUE}"/>')
    parts.append(f'<text x="{pad + size * 1.2:.1f}" y="{ly:.1f}" font-size="{size * 0.8:.1f}" fill="{DIM}">best mission</text>')
    parts.append(f'<circle cx="{pad + size * 8.4:.1f}" cy="{ly - size * 0.3:.1f}" r="{size * 0.3:.1f}" fill="#0f1e3d" stroke="{DIM}" stroke-width="2"/>')
    parts.append(f'<text x="{pad + size * 9.2:.1f}" y="{ly:.1f}" font-size="{size * 0.8:.1f}" fill="{DIM}">median asteroid</text>')
    parts.append(f'<rect x="{pad + size * 17.4:.1f}" y="{ly - size * 0.75:.1f}" width="{size * 0.9:.1f}" height="{size * 0.9:.1f}" '
                 f'fill="{GREEN}" fill-opacity="0.25" stroke="{GREEN}" stroke-opacity="0.5"/>')
    parts.append(f'<text x="{pad + size * 18.6:.1f}" y="{ly:.1f}" font-size="{size * 0.8:.1f}" fill="{DIM}">pays for itself</text>')
    parts.append("</g>\n</svg>\n")
    return "\n".join(parts)


def update_readme(readme):
    """The README with this chart's alt text written in, so a screen reader hears the numbers
    it shows, and the sentence above it ending in clause(), so the prose can't go on saying
    none breaks even once one does. refresh_counts.py calls it after refreshing the counts;
    check.py checks it."""
    readme = panel.write_alt(readme, "breakeven.svg", ALT)
    readme, n = re.subn(r"(Left of the dashed line, a mission pays for itself; )[^.]*\.",
                        lambda m: f"{m[1]}{clause(ROWS)}.", readme)
    if n != 1:
        sys.exit(f"README's sentence above the break-even chart matched {n} times, expected 1")
    return readme


def files():
    return {
        "breakeven.svg": render(1200, 31, 40, 52, 19, 40, 170, 680, True),
        "breakeven-compact.svg": render(680, 32, 36, 60, 24, 46, 170, 330, False),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for file, svg in files().items():
        (out / file).write_text(svg, encoding="utf-8", newline="\n")
        print(file)


if __name__ == "__main__":
    main()
