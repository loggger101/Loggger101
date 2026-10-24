"""Generate the activity panel (docs/activity.svg, docs/activity-compact.svg): every commit
I've made to the repos the README lists, drawn as orbits round the banner's star.

Each ring is one section of the README, the outermost the first. Time runs clockwise from
my first commit at twelve o'clock to this week, stopping short of twelve to leave the wedge
where the rings are named. A dot is one week's commits to that section's repos, its area in
proportion to the count; past MAX_DOTS weeks, a dot takes in as many weeks as it needs to
keep the rings from running together. Beside the rings: the total, each section's, the
busiest week and the latest commit.

The numbers are refresh_activity.py's, from tools/counts.json, and the orbit ends at the
week it last ran, so this draws the same thing until the counts change.

`activity.svg` puts the panel beside the rings, for desktop widths; `activity-compact.svg`
puts it underneath with larger text, for phones, and the README swaps it in with <picture>.
"""
import datetime as dt
import html
import json
import math
import random
import re
import sys
from pathlib import Path

from loc import README_NAMES

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM, GOLD = "#5ba3dc", "#dbe3f5", "#7d8fb3", "#e8c27a"

ACTIVITY = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["activity"]
# The README's sections, in its order, and the repos in each.
SECTIONS = {
    "Space economics": ["economicspace", "AsteroidCatalog", "spacecost", "General_Research", "starred-repos"],
    "Planetary science": ["asteroid-belt-gradient", "Mars_Terrestrial_GlobalMosaic_GIS-Data"],
    "Deep learning": ["star-spectral-classifier", "drone-target-id"],
    "Simulation": ["Satellite-Space-Flight"],
    "Rare-disease work": ["aspirecures", "SistersHopeFoundation"],
    "Elsewhere": ["website", "quietlaunch", "quietqueue", "Hermes_Skills"],
}
listed = [r for repos in SECTIONS.values() for r in repos]
if sorted(listed) != sorted(ACTIVITY["repos"]):
    sys.exit(f"SECTIONS and counts.json disagree on the repos: {sorted(set(listed) ^ set(ACTIVITY['repos']))}")

GAP = 62            # degrees left empty at the top left for the ring names
MAX_DOTS = 60       # dots a ring holds at most; the inner ring can't fit more apart
AS_OF = dt.date.fromisoformat(ACTIVITY["as_of"])
FIRST_DAY = min(dt.date.fromisoformat(r["first"]) for r in ACTIVITY["repos"].values())
FIRST_MONDAY = FIRST_DAY - dt.timedelta(days=FIRST_DAY.weekday())
LAST_MONDAY = AS_OF - dt.timedelta(days=AS_OF.weekday())
N_WEEKS = (LAST_MONDAY - FIRST_MONDAY).days // 7 + 1
WEEKS = [FIRST_MONDAY + dt.timedelta(weeks=i) for i in range(N_WEEKS)]
PER_DOT = math.ceil(N_WEEKS / MAX_DOTS)     # weeks in a dot
N_DOTS = math.ceil(N_WEEKS / PER_DOT)


def by_section():
    """{section: [commits in each week from the first]}"""
    out = {}
    for section, repos in SECTIONS.items():
        counts = [0] * N_WEEKS
        for repo in repos:
            for week, n in ACTIVITY["repos"][repo]["weeks"].items():
                i = (dt.date.fromisoformat(week) - FIRST_MONDAY).days // 7
                if 0 <= i < N_WEEKS:
                    counts[i] += n
        out[section] = counts
    return out


COUNTS = by_section()
DOTS = {s: [sum(c[i:i + PER_DOT]) for i in range(0, N_WEEKS, PER_DOT)] for s, c in COUNTS.items()}
TOTAL = sum(map(sum, COUNTS.values()))
PEAK = max(max(d) for d in DOTS.values())
WEEK_TOTALS = [sum(c[i] for c in COUNTS.values()) for i in range(N_WEEKS)]
BUSIEST = max(range(N_WEEKS), key=lambda i: (WEEK_TOTALS[i], i))
LATEST = max(ACTIVITY["repos"], key=lambda r: (ACTIVITY["repos"][r]["last"], r))
LATEST_DAY = dt.date.fromisoformat(ACTIVITY["repos"][LATEST]["last"])


def day(d):
    return f"{d.day} {d:%b %Y}"


def angle(t):
    """Degrees clockwise from twelve o'clock for t in [0, 1] of the way from the first week to now."""
    return t * (360 - GAP)


def point(cx, cy, r, deg):
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, d0, d1):
    x0, y0 = point(cx, cy, r, d0)
    x1, y1 = point(cx, cy, r, d1)
    return f"M{x0:.1f} {y0:.1f} A{r} {r} 0 {int(d1 - d0 > 180)} 1 {x1:.1f} {y1:.1f}"


ALT = (f"Every commit I've made to these repos, from the first on {day(FIRST_DAY)} to {day(AS_OF)}, "
       f"drawn as one orbit per section of this page: {TOTAL:,} in all, "
       + ", ".join(f"{s} {sum(c):,}" for s, c in COUNTS.items())
       + f". Busiest week: {WEEK_TOTALS[BUSIEST]:,} commits, the week of {day(WEEKS[BUSIEST])}. "
       f"Latest: {README_NAMES.get(LATEST, LATEST)}, {day(LATEST_DAY)}.")


def background(w, h, seed):
    rng = random.Random(seed)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, w - 8):.1f}" cy="{rng.uniform(8, h - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(int(w * h / 4500))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(ALT)}">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#112650"/></linearGradient>
<radialGradient id="corona" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/><stop offset="0.1" stop-color="#e6f2ff" stop-opacity="0.7"/><stop offset="0.35" stop-color="#9ccaf2" stop-opacity="0.35"/><stop offset="1" stop-color="#5ba3dc" stop-opacity="0"/></radialGradient>
</defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#g)" stroke="#2a3b63"/>
{stars}
"""


def field(cx, cy, r_in, r_step, label_size, month_size):
    """The star, the rings with their dots, the month names and the ring names."""
    rings = list(DOTS.items())[::-1]         # innermost first: the README's last section
    r_out = r_in + r_step * (len(rings) - 1)
    dot_max = r_step * 0.42
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{r_in * 0.55:.1f}" fill="url(#corona)"/>',
             f'<circle cx="{cx}" cy="{cy}" r="{r_in * 0.06:.1f}" fill="#ffffff"/>']
    for k, (section, counts) in enumerate(rings):
        r = r_in + k * r_step
        parts.append(f'<path d="{arc(cx, cy, r, 0, angle(1))}" fill="none" stroke="#8fb6e8" '
                     f'stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="3 5"/>')
        for i, n in enumerate(counts):
            if n:
                # A dot sits at the middle of its weeks; the last one may hold fewer.
                mid = (i * PER_DOT + min((i + 1) * PER_DOT, N_WEEKS)) / 2
                x, y = point(cx, cy, r, angle(mid / N_WEEKS))
                size = 1.8 + (dot_max - 1.8) * math.sqrt(n / PEAK)
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="{BLUE}" fill-opacity="0.8"/>')
        # The ring's name, right-aligned just left of where its orbit begins.
        parts.append(f'<text x="{cx - 10}" y="{cy - r + label_size * 0.35:.1f}" text-anchor="end" '
                     f'font-size="{label_size}" fill="{TEXT}">{section}</text>')
    # A tick outside the rings at the first of each month; none falls in the wedge. January
    # is named by its year. The other months are named too while there are few enough of
    # them (two years' worth) to read.
    span = N_WEEKS * 7
    months = []
    m = dt.date(FIRST_MONDAY.year, FIRST_MONDAY.month, 1)
    while m <= AS_OF:
        if m >= FIRST_MONDAY:
            months.append(m)
        m = dt.date(m.year + m.month // 12, m.month % 12 + 1, 1)
    for m in months:
        t = (m - FIRST_MONDAY).days / span
        named = m.month == 1 or len(months) <= 24
        tick0, tick1 = point(cx, cy, r_out + 12, angle(t)), point(cx, cy, r_out + (20 if named else 16), angle(t))
        parts.append(f'<line x1="{tick0[0]:.1f}" y1="{tick0[1]:.1f}" x2="{tick1[0]:.1f}" y2="{tick1[1]:.1f}" stroke="{DIM}" stroke-width="1.2"/>')
        if named:
            tx, ty = point(cx, cy, r_out + 22 + month_size * (1.3 if m.month == 1 else 0.9), angle(t))
            parts.append(f'<text x="{tx:.1f}" y="{ty + month_size * 0.35:.1f}" text-anchor="middle" '
                         f'font-size="{month_size}" fill="{TEXT if m.month == 1 else DIM}">'
                         f'{m.year if m.month == 1 else f"{m:%b}"}</text>')
    # Where the orbit ends: this week.
    e0, e1 = point(cx, cy, r_in - r_step * 0.6, angle(1)), point(cx, cy, r_out + r_step * 0.6, angle(1))
    parts.append(f'<line x1="{e0[0]:.1f}" y1="{e0[1]:.1f}" x2="{e1[0]:.1f}" y2="{e1[1]:.1f}" stroke="{GOLD}" '
                 f'stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round"/>')
    nx, ny = point(cx, cy, r_out + 22 + month_size * 0.9, angle(1))
    parts.append(f'<text x="{nx:.1f}" y="{ny + month_size * 0.35:.1f}" text-anchor="middle" '
                 f'font-size="{month_size}" font-weight="700" fill="{GOLD}">now</text>')
    return parts


def panel(x, y, big, size, row_gap, width):
    """The total, each section's count with a bar, the busiest week and the latest commit."""
    parts = [f'<text x="{x}" y="{y + big * 0.8:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">{TOTAL:,}</text>',
             f'<text x="{x}" y="{y + big * 0.8 + size * 1.5:.1f}" font-size="{size}" fill="{TEXT}">commits since my first, in {FIRST_DAY:%B %Y}</text>']
    top = y + big * 0.8 + size * 1.5 + row_gap * 1.1
    most = max(sum(c) for c in COUNTS.values())
    name_w, num_w = size * 9.2, size * 3.2
    bar_x, bar_w = x + name_w, width - name_w - num_w
    for k, (section, counts) in enumerate(COUNTS.items()):
        ry = top + k * row_gap
        n = sum(counts)
        parts.append(f'<text x="{x}" y="{ry:.1f}" font-size="{size}" fill="#b9c6e4">{section}</text>')
        parts.append(f'<rect x="{bar_x:.1f}" y="{ry - size * 0.62:.1f}" width="{bar_w:.1f}" height="{size * 0.6:.1f}" rx="{size * 0.3:.1f}" fill="#13213f"/>')
        if n:
            parts.append(f'<rect x="{bar_x:.1f}" y="{ry - size * 0.62:.1f}" width="{max(bar_w * n / most, size * 0.6):.1f}" '
                         f'height="{size * 0.6:.1f}" rx="{size * 0.3:.1f}" fill="{BLUE}"/>')
        parts.append(f'<text x="{x + width:.1f}" y="{ry:.1f}" text-anchor="end" font-size="{size}" fill="{TEXT}">{n:,}</text>')
    ry = top + len(COUNTS) * row_gap + row_gap * 0.4
    parts.append(f'<line x1="{x}" y1="{ry - size * 1.2:.1f}" x2="{x + width}" y2="{ry - size * 1.2:.1f}" stroke="#2a3b63"/>')
    for label, value in (("Busiest week", f"{WEEK_TOTALS[BUSIEST]:,} commits, the week of {day(WEEKS[BUSIEST])}"),
                         ("Latest", f"{README_NAMES.get(LATEST, LATEST)}, {day(LATEST_DAY)}")):
        parts.append(f'<text x="{x}" y="{ry:.1f}" font-size="{size}"><tspan fill="{DIM}">{label}</tspan>'
                     f'<tspan x="{x + size * 6.5:.1f}" fill="{TEXT}">{value}</tspan></text>')
        ry += row_gap
    return parts


def render(w, h, seed, field_args, panel_args):
    parts = [background(w, h, seed), f'<g font-family="{FONT}">']
    parts += field(*field_args)
    parts += panel(*panel_args)
    parts.append("</g>\n</svg>\n")
    return "\n".join(parts)


def update_readme(readme):
    """The README with this panel's alt text written in, so a screen reader hears the numbers
    the image shows. refresh_activity.py calls it after refreshing the counts; check.py checks it."""
    pattern = r'(src="docs/activity\.svg" width="100%" alt=")[^"]*(")'
    readme, n = re.subn(pattern, lambda m: m[1] + html.escape(ALT, quote=False).replace('"', '&quot;') + m[2], readme)
    if n != 1:
        sys.exit(f"README image docs/activity.svg matched {n} times, expected 1")
    return readme


def files():
    # Desktop: rings on the left, the panel on the right.
    # Phones: the rings on top, the panel under them, both larger for a screen about 350px wide.
    return {
        "activity.svg": render(1200, 640, 11, (330, 326, 112, 30, 17, 16), (690, 110, 52, 19, 40, 470)),
        "activity-compact.svg": render(680, 1240, 12, (340, 360, 108, 33, 21, 20), (44, 724, 60, 25, 46, 592)),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, svg in files().items():
        (out / name).write_text(svg, encoding="utf-8", newline="\n")
        print(name)


if __name__ == "__main__":
    main()
