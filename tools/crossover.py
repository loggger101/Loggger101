"""Generate the crossover chart (docs/crossover.svg, docs/crossover-compact.svg): what the
asteroid-belt-gradient paper found, one row for each sample it fits.

Each row is a logistic fit of the C-type fraction against distance from the Sun: the dot
is where C-types reach half (a50) with its bootstrap interval, and the bar runs from 10% to
90% C, shaded from S-type gold to C-type blue. The first row is the raw count; the others
are corrected for collisional families and for the brightness bias that favors S-types.
The main belt is shaded behind them and the snow line dashed across, so the eye can see
the corrected turn sit inside the line and run wider than the belt.

The numbers are refresh_counts.py's, read from the paper repo's results/summary.json and
kept in tools/counts.json ("belt"), so this draws the same thing until they change. When
the chart loads, each corrected row slides in from where the raw count put it; with
reduced motion it is drawn finished.

`crossover.svg` is for desktop widths. `crossover-compact.svg` drops the descriptions and
counts and uses larger text, for phones; the README swaps it in with <picture>.
"""
import html
import json
import re
import sys
from pathlib import Path

import panel

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM, GOLD = "#5ba3dc", "#dbe3f5", "#7d8fb3", "#e8c27a"
SMALL = panel.SMALL

BELT = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["belt"]
ROWS, SNOW = BELT["crossover"], BELT["snow_line_au"]
# The main belt as the paper bounds it (its zones run from 2.1 to 3.3 au).
INNER, OUTER = 2.1, 3.3
LO, HI = 1.6, 3.8       # the axis, in au
# summary.json's name for each sample: the row's label, what it holds, and the label on phones.
SAMPLES = {
    "raw": ("Raw count", "every classified S and C", "Raw count"),
    "collapsed, IPW, D≥10 km": ("Families collapsed", "D ≥ 10 km, weighted for brightness bias", "Collapsed, ≥10 km"),
    "collapsed, D≥53 km": ("Families collapsed", "D ≥ 53 km, complete in size", "Collapsed, ≥53 km"),
    "background, D≥53 km": ("Background only", "D ≥ 53 km, family members left out", "Background, ≥53 km"),
}
RAW = next(r for r in ROWS if r["sample"] == "raw")
CORRECTED = [r for r in ROWS if r["sample"] != "raw"]


def label(sample):
    return SAMPLES.get(sample, (sample, "", sample))


def span(values, places):
    """2.41–2.47, or one number when they round the same."""
    lo, hi = f"{min(values):.{places}f}", f"{max(values):.{places}f}"
    return lo if lo == hi else f"{lo}–{hi}"


def where(rows, snow):
    """Where the corrected crossovers sit against the snow line."""
    if max(r["a50"] for r in rows) < snow:
        return "inside"
    if min(r["a50"] for r in rows) > snow:
        return "beyond"
    return "across"


def wide(rows):
    """How the corrected 10-90% transitions compare with the belt's own width."""
    if min(r["width"] for r in rows) > OUTER - INNER:
        return "wider than the belt itself"
    if max(r["width"] for r in rows) < OUTER - INNER:
        return "narrower than the belt"
    return "about as wide as the belt"


def finding(rows, snow):
    """The README's sentence on what the corrected fits say, from the numbers."""
    return (f"Corrected, the turn sits at {span([r['a50'] for r in rows], 2)} au, {where(rows, snow)} the snow line "
            f"at {snow:.2f} au, and takes {span([r['width'] for r in rows], 1)} au to go from 10% to 90% C-types, "
            f"{wide(rows)}.")


ALT = (f"Where the asteroid belt turns from S-types to C-types, from asteroid-belt-gradient's results: the raw count puts "
       f"the crossover at {RAW['a50']:.2f} au; corrected, "
       + ", ".join(f"{r['a50']:.2f} au ({label(r['sample'])[0].lower()}, {label(r['sample'])[1]})" for r in CORRECTED)
       + f", each {span([r['width'] for r in CORRECTED], 1)} au from 10% to 90% C-types, {wide(CORRECTED)}; "
       f"the snow line is at {SNOW:.2f} au and the main belt runs from {INNER} to {OUTER} au.")


def background(w, h, seed):
    return panel.background(w, h, seed, ALT, defs=(
        f'<linearGradient id="sc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}"/>'
        f'<stop offset="1" stop-color="{BLUE}"/></linearGradient>',
    ), rules=(
        ".slide { animation: slide 1.4s cubic-bezier(0.2, 0.7, 0.2, 1) both; }",
        "@keyframes slide { from { transform: translateX(var(--from)); } }",
    ), animated=("slide",))


def render(w, seed, pad, big, size, row_gap, name_w, track_w, full):
    head = pad + big * 0.8
    top = head + size * 1.6 + size * 0.9 + row_gap * 1.5
    h = round(top + (len(ROWS) - 1) * row_gap + row_gap * 0.6 + size * 4.4 + pad * 0.6)
    x0 = pad + name_w
    at = lambda au: x0 + track_w * (min(max(au, LO), HI) - LO) / (HI - LO)
    bar = size * 0.55
    parts = [background(w, h, seed), f'<g font-family="{FONT}">',
             f'<text x="{pad}" y="{head:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">'
             f'{span([r["a50"] for r in CORRECTED], 2)} au</text>',
             f'<text x="{pad}" y="{head + size * 1.5:.1f}" font-size="{size}" fill="{TEXT}">'
             + ("where the belt turns from S-types to C-types, once corrected" if full else "where S-types give way to C-types")
             + '</text>',
             f'<text x="{pad}" y="{head + size * 2.6:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
             + html.escape(f"The raw count says {RAW['a50']:.2f} au. Corrected, the turn is {where(CORRECTED, SNOW)} the snow line "
                           f"and {wide(CORRECTED)}." if full else
                           f"Raw count: {RAW['a50']:.2f} au. Snow line: {SNOW:.2f} au.", quote=False) + '</text>']
    upper, bottom = top - row_gap * 0.8, top + (len(ROWS) - 1) * row_gap + row_gap * 0.6
    # The main belt behind the rows, and the snow line across them.
    parts.append(f'<rect x="{at(INNER):.1f}" y="{upper:.1f}" width="{at(OUTER) - at(INNER):.1f}" '
                 f'height="{bottom - upper:.1f}" fill="{BLUE}" fill-opacity="0.07"/>')
    # On phones the belt is too narrow to name beside the snow line; the key names it instead.
    if full:
        parts.append(f'<text x="{at(INNER) + 6:.1f}" y="{upper + size * 0.95:.1f}" font-size="{size * SMALL:.1f}" '
                     f'fill="{DIM}">main belt</text>')
    parts.append(f'<line x1="{at(SNOW):.1f}" y1="{upper:.1f}" x2="{at(SNOW):.1f}" y2="{bottom:.1f}" '
                 f'stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    parts.append(f'<text x="{at(SNOW) + 6:.1f}" y="{upper - size * 0.35:.1f}" font-size="{size * SMALL:.1f}" '
                 f'fill="{GOLD}">snow line</text>')
    # Every tick says au on desktop; on phones only the last has room to.
    for v in (2.0, 2.5, 3.0, 3.5):
        parts.append(f'<line x1="{at(v):.1f}" y1="{bottom:.1f}" x2="{at(v):.1f}" y2="{bottom + 6:.1f}" stroke="{DIM}" stroke-width="1.2"/>')
        parts.append(f'<text x="{at(v):.1f}" y="{bottom + 6 + size * 1.1:.1f}" text-anchor="middle" font-size="{size * SMALL:.1f}" '
                     f'fill="{DIM}">{v:.1f}{" au" if full or v == 3.5 else ""}</text>')
    for k, r in enumerate(ROWS):
        y = top + k * row_gap
        name, about, short = label(r["sample"])
        raw = r is RAW
        x, x1, x2 = at(r["a50"]), at(r["a50"] - r["width"] / 2), at(r["a50"] + r["width"] / 2)
        delay = f"animation-delay:{0.2 + 0.1 * k:.2f}s"
        if full and about:
            parts.append(f'<text x="{pad}" y="{y - size * 0.1:.1f}" font-size="{size}" fill="#b9c6e4">{html.escape(name)}</text>')
            parts.append(f'<text x="{pad}" y="{y + size * 0.95:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
                         f'{html.escape(about)}</text>')
        else:
            parts.append(f'<text x="{pad}" y="{y + size * 0.35:.1f}" font-size="{size}" fill="#b9c6e4">'
                         f'{html.escape(name if full else short)}</text>')
        parts.append(f'<line x1="{at(LO):.1f}" y1="{y:.1f}" x2="{at(HI):.1f}" y2="{y:.1f}" stroke="#2a3b63" stroke-width="1"/>')
        # A corrected row slides in from where the raw count put the turn.
        move = "" if raw else f' class="slide" style="--from:{at(RAW["a50"]) - x:.1f}px;{delay}"'
        parts.append(f'<g{move}>')
        parts.append(f'<rect x="{x1:.1f}" y="{y - bar / 2:.1f}" width="{x2 - x1:.1f}" height="{bar:.1f}" rx="{bar / 2:.1f}" '
                     f'fill="url(#sc)" fill-opacity="{0.45 if raw else 0.8}"/>')
        parts.append(f'<line x1="{at(r["lo"]):.1f}" y1="{y:.1f}" x2="{at(r["hi"]):.1f}" y2="{y:.1f}" stroke="#ffffff" '
                     f'stroke-width="{size * 0.9:.1f}" stroke-opacity="0.35" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 0.32:.1f}" fill="{"#0f1e3d" if raw else TEXT}" '
                     f'stroke="{TEXT}" stroke-width="2"/>')
        parts.append("</g>")
        right = x0 + track_w + size * 4.4
        parts.append(f'<text x="{right:.1f}" y="{y + size * 0.35:.1f}" text-anchor="end" font-size="{size}" '
                     f'fill="{TEXT}">{r["a50"]:.2f} au</text>')
        if full:
            parts.append(f'<text x="{right + size * 0.8:.1f}" y="{y + size * 0.35:.1f}" font-size="{size * SMALL:.1f}" '
                         f'fill="{DIM}">{r["n"]:,} asteroids</text>')
    # What the marks are.
    ly = bottom + 6 + size * 3
    parts.append(f'<circle cx="{pad + size * 0.4:.1f}" cy="{ly - size * 0.3:.1f}" r="{size * 0.32:.1f}" fill="{TEXT}"/>')
    parts.append(f'<text x="{pad + size * 1.2:.1f}" y="{ly:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
                 + ("half C-types, and its bootstrap range" if full else "half C-types") + '</text>')
    lx = pad + size * (17 if full else 7.6)
    parts.append(f'<rect x="{lx:.1f}" y="{ly - size * 0.3 - bar / 2:.1f}" width="{size * 2.4:.1f}" height="{bar:.1f}" '
                 f'rx="{bar / 2:.1f}" fill="url(#sc)" fill-opacity="0.8"/>')
    parts.append(f'<text x="{lx + size * 2.9:.1f}" y="{ly:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
                 + ("10% to 90% C, from S-type gold to C-type blue" if full else "10% to 90% C") + '</text>')
    if not full:
        bx = lx + size * 10.6
        parts.append(f'<rect x="{bx:.1f}" y="{ly - size * 0.75:.1f}" width="{size * 0.9:.1f}" height="{size * 0.9:.1f}" '
                     f'fill="{BLUE}" fill-opacity="0.2" stroke="{BLUE}" stroke-opacity="0.4"/>')
        parts.append(f'<text x="{bx + size * 1.2:.1f}" y="{ly:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">main belt</text>')
    parts.append("</g>\n</svg>\n")
    return panel.keep_clear("\n".join(parts))


def update_readme(readme):
    """The README with this chart's alt text written in, and the sentence above it saying
    what the corrected fits find, so the prose can't keep an old result. refresh_counts.py
    calls it after refreshing the counts; check.py checks it."""
    readme = panel.write_alt(readme, "crossover.svg", ALT)
    readme, n = re.subn(r"Corrected, the turn sits at .*? C-types, [^.]*\.", lambda m: finding(CORRECTED, SNOW), readme)
    if n != 1:
        sys.exit(f"README's sentence above the crossover chart matched {n} times, expected 1")
    readme, n = re.subn(r"(the bar runs from 10% to 90%\. The raw count puts it at )[\d.]+( au\.)",
                        lambda m: f"{m[1]}{RAW['a50']:.2f}{m[2]}", readme)
    if n != 1:
        sys.exit(f"README's raw crossover above the crossover chart matched {n} times, expected 1")
    return readme


def files():
    return {
        "crossover.svg": render(1200, 41, 40, 52, 19, 56, 300, 560, True),
        "crossover-compact.svg": render(680, 42, 36, 60, 24, 50, 232, 290, False),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for file, svg in files().items():
        (out / file).write_text(svg, encoding="utf-8", newline="\n")
        print(file)


if __name__ == "__main__":
    main()
