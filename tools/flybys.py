"""Generate the flyby chart (docs/flybys.svg, docs/flybys-compact.svg): the asteroids passing
Earth in the week refresh_flybys.py last looked at, within 20 lunar distances.

Earth sits at the left with the Moon's distance marked; each asteroid is a row, its dot at
its nominal miss distance on a linear scale in lunar distances and sized by how wide it
is likely to be. Beside each: the distance, the size and the speed. At most MAX_ROWS rows,
nearest first; the header counts them all and names the closest.

Almost none of these bodies has a measured diameter, so the size comes from the absolute
magnitude H at albedos 0.25 to 0.05, the usual bracket, written as a range ("18-40 m").
A measured diameter, when JPL has one, is used instead.

The numbers are refresh_flybys.py's, from tools/counts.json, so this draws the same thing
until the counts change; the header prints the week, so a stale chart is plainly dated.
When it loads, each asteroid flies in from the right along its row, the nearest first; with
reduced motion it is drawn finished.

`flybys.svg` is for desktop widths; `flybys-compact.svg` drops the dates and speeds and uses
larger text, for phones; the README swaps it in with <picture>.
"""
import datetime as dt
import html
import json
import math
import sys
from pathlib import Path

import panel

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM, GOLD = "#5ba3dc", "#dbe3f5", "#7d8fb3", "#e8c27a"

FLYBYS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["flybys"]
LD_AU = 384400 / 149597870.7          # one lunar distance, in au
MAX_LD = 20
MAX_ROWS = 8
ROWS = FLYBYS["rows"][:MAX_ROWS]
FROM, TO = (dt.date.fromisoformat(FLYBYS[k]) for k in ("from", "to"))


def ld(row):
    return row["dist_au"] / LD_AU


def size_m(row):
    """(smallest, largest) likely diameter in metres."""
    if row["diameter_km"]:
        d = row["diameter_km"] * 1000
        return d, d
    if row["h"] is None:
        return None
    d = lambda albedo: 1329e3 / math.sqrt(albedo) * 10 ** (-row["h"] / 5)
    return d(0.25), d(0.05)


def size_text(row):
    s = size_m(row)
    if s is None:
        return "size unknown"
    lo, hi = s
    fmt = lambda m: f"{m / 1000:.1f} km" if m >= 1000 else f"{m:.0f} m"
    return fmt(lo) if lo == hi else (f"{lo:.0f}–{fmt(hi)}" if hi < 1000 else f"{fmt(lo)}–{fmt(hi)}")


def when(row):
    """'Tue 27 Oct' from JPL's '2026-Oct-27 01:10' (TDB, within a minute of UTC)."""
    t = dt.datetime.strptime(row["time"], "%Y-%b-%d %H:%M")
    return f"{t:%a} {t.day} {t:%b}"


def span():
    end = TO - dt.timedelta(days=1)
    return (f"{FROM.day}–{end.day} {end:%b %Y}" if FROM.month == end.month
            else f"{FROM.day} {FROM:%b} – {end.day} {end:%b %Y}")


COUNT = len(FLYBYS["rows"])
CLOSEST = FLYBYS["rows"][0] if FLYBYS["rows"] else None
def alt_text(rows):
    """The chart in words: the count, each row it draws and how many it leaves off, as it does."""
    head = f"Asteroids passing Earth within {MAX_LD} lunar distances, {span()} (NASA/JPL close-approach data): "
    if not rows:
        return head + "none this week."
    shown = rows[:MAX_ROWS]
    listed = "; ".join(f"{r['des']}, {ld(r):.1f} lunar distances on {when(r)}, {size_text(r)}, "
                       f"{r['v_kms']:.1f} km/s" for r in shown)
    more = f"; and {len(rows) - len(shown)} more farther out" if len(rows) > len(shown) else ""
    return head + f"{len(rows)} in all. {listed}{more}."


ALT = alt_text(FLYBYS["rows"])


# Earth, the glow round it, and the asteroids' sunlit rock.
GRADIENTS = (
    '<radialGradient id="earth" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#9fd4ff"/>'
    '<stop offset="0.5" stop-color="#3d7fc4"/><stop offset="1" stop-color="#173a6b"/></radialGradient>',
    '<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.55" stop-color="#5ba3dc" stop-opacity="0.35"/>'
    '<stop offset="1" stop-color="#5ba3dc" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="rock" cx="0.35" cy="0.35" r="0.65"><stop offset="0" stop-color="#fff4d8"/>'
    '<stop offset="0.45" stop-color="#e8c27a"/><stop offset="1" stop-color="#7a5a26"/></radialGradient>',
)


def background(w, h, seed):
    return panel.background(w, h, seed, ALT, defs=GRADIENTS, rules=(
        ".fly { animation: fly 1.6s cubic-bezier(0.2, 0.7, 0.2, 1) both; }",
        "@keyframes fly { from { transform: translateX(var(--from)); opacity: 0; } 20% { opacity: 1; } }",
        *panel.FADE,
    ), animated=("fly", "fade"))


def render(w, seed, pad, big, size, row_gap, name_w, track_w, full):
    head = pad + big * 0.8
    top = head + size * 2.6 + row_gap * 1.3
    n = max(len(ROWS), 1)
    h = round(top + (n - 1) * row_gap + row_gap * 0.6 + size * 2.4 + pad * 0.6)
    x0 = pad + name_w                                   # Earth's centre
    at = lambda v: x0 + track_w * v / MAX_LD
    bottom = top + (n - 1) * row_gap + row_gap * 0.6
    unit = "lunar distances" if full else "LD"
    closest = (f"Closest: {CLOSEST['des']}, {ld(CLOSEST):.1f} {unit} on {when(CLOSEST)}." if CLOSEST else "None this week.")
    # On phones the week moves to the second line, to keep the first short.
    line1 = f'{"asteroid passes" if COUNT == 1 else "asteroids pass"} within {MAX_LD} {unit}' + (f", {span()}" if full else "")
    line2 = f"{closest} NASA/JPL close-approach data." if full else f"{span()}. {closest}"
    parts = [background(w, h, seed), f'<g font-family="{FONT}">',
             f'<text x="{pad}" y="{head:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">{COUNT}</text>',
             f'<text x="{pad + big * 0.62 * len(str(COUNT)) + size * 0.6:.1f}" y="{head:.1f}" font-size="{size}" fill="{TEXT}">{line1}</text>',
             f'<text x="{pad}" y="{head + size * 1.6:.1f}" font-size="{size * 0.8:.1f}" fill="{DIM}">{html.escape(line2)}</text>']
    # Earth, and the Moon's distance.
    mid = (top + bottom - row_gap * 0.6) / 2
    parts.append(f'<circle cx="{x0:.1f}" cy="{mid:.1f}" r="{size * 1.5:.1f}" fill="url(#halo)"/>')
    parts.append(f'<circle cx="{x0:.1f}" cy="{mid:.1f}" r="{size * 0.85:.1f}" fill="url(#earth)"/>')
    parts.append(f'<line x1="{at(1):.1f}" y1="{top - row_gap * 0.7:.1f}" x2="{at(1):.1f}" y2="{bottom:.1f}" '
                 f'stroke="{DIM}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    parts.append(f'<text x="{at(1) + 5:.1f}" y="{top - row_gap * 0.7 + size * 0.2:.1f}" font-size="{size * 0.75:.1f}" fill="{DIM}">the Moon</text>')
    for v in (0, 5, 10, 15, 20):
        parts.append(f'<line x1="{at(v):.1f}" y1="{bottom:.1f}" x2="{at(v):.1f}" y2="{bottom + 6:.1f}" stroke="{DIM}" stroke-width="1.2"/>')
        parts.append(f'<text x="{at(v):.1f}" y="{bottom + 6 + size * 1.1:.1f}" text-anchor="middle" font-size="{size * 0.8:.1f}" '
                     f'fill="{DIM}">{v}{" LD" if v == MAX_LD else ""}</text>')
    if not ROWS:
        parts.append(f'<text x="{at(MAX_LD / 2):.1f}" y="{mid + size * 0.35:.1f}" text-anchor="middle" font-size="{size}" '
                     f'fill="{DIM}">no asteroid comes this close this week</text>')
    biggest = max((size_m(r)[1] for r in ROWS if size_m(r)), default=1)
    for k, r in enumerate(ROWS):
        y = top + k * row_gap
        x = at(min(ld(r), MAX_LD))
        s = size_m(r)
        # Dot area follows the likely width (the middle of the range), from a speck to most of a row.
        radius = size * (0.22 + 0.33 * math.sqrt(math.sqrt(s[0] * s[1]) / biggest)) if s else size * 0.22
        delay = f"animation-delay:{0.2 + 0.12 * k:.2f}s"
        parts.append(f'<text x="{pad}" y="{y + size * 0.35:.1f}" font-size="{size}" fill="#b9c6e4">{html.escape(r["des"])}</text>')
        parts.append(f'<line x1="{x0 + size * 1.2:.1f}" y1="{y:.1f}" x2="{at(MAX_LD):.1f}" y2="{y:.1f}" stroke="#2a3b63" stroke-width="1"/>')
        parts.append(f'<circle class="fly" cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="url(#rock)" '
                     f'style="--from:{at(MAX_LD) + size * 2 - x:.1f}px;{delay}"/>')
        facts = (f"{ld(r):.1f} LD · {size_text(r)} · {r['v_kms']:.1f} km/s · {when(r)}" if full
                 else f"{ld(r):.1f} LD · {size_text(r)}")
        parts.append(f'<text class="fade" x="{at(MAX_LD) + size * 1.4:.1f}" y="{y + size * 0.35:.1f}" font-size="{size * 0.85:.1f}" '
                     f'fill="{TEXT}" style="{delay}">{html.escape(facts)}</text>')
    if COUNT > len(ROWS):
        parts.append(f'<text x="{at(MAX_LD) + size * 1.4:.1f}" y="{bottom + 6 + size * 1.1:.1f}" font-size="{size * 0.75:.1f}" '
                     f'fill="{DIM}">and {COUNT - len(ROWS)} more farther out</text>')
    parts.append("</g>\n</svg>\n")
    return panel.keep_clear("\n".join(parts))


def update_readme(readme):
    """The README with this chart's alt text written in, so a screen reader hears what it
    shows. refresh_flybys.py calls it after refreshing; check.py checks it."""
    readme = panel.write_alt(readme, "flybys.svg", ALT)
    return readme


def files():
    return {
        "flybys.svg": render(1200, 41, 40, 52, 19, 38, 150, 560, True),
        "flybys-compact.svg": render(680, 42, 36, 60, 24, 44, 172, 222, False),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for file, svg in files().items():
        (out / file).write_text(svg, encoding="utf-8", newline="\n")
        print(file)


if __name__ == "__main__":
    main()
