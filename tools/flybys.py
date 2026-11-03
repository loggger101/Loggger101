"""Generate the flyby chart (docs/flybys.svg, docs/flybys-compact.svg): the asteroids passing
Earth in the week refresh_flybys.py last looked at, within 20 lunar distances.

The week is a dial round Earth. Time runs clockwise from twelve o'clock, one wedge a day;
distance runs outward on a square-root scale, with rings at the Moon's distance (dashed,
gold), 5, 10 and 20 lunar distances. Each asteroid sits at the moment and distance of its
closest approach, sized by how wide it is likely to be and numbered as in the list beside
the dial, which gives each one's distance, size, speed and day. At most MAX_ROWS of them,
nearest first; the header counts them all and names the closest.

Almost none of these bodies has a measured diameter, so the size comes from the absolute
magnitude H at albedos 0.25 to 0.05, the usual bracket, written as a range ("18-40 m").
A measured diameter, when JPL has one, is used instead.

The numbers are refresh_flybys.py's, from tools/counts.json, so this draws the same thing
until the counts change; the header prints the week, so a stale chart is plainly dated.
When it loads, each asteroid drifts in to its place along its day's ray, the nearest first,
and its number and line in the list fade in; with reduced motion it is drawn finished.

`flybys.svg` is for desktop widths, the list beside the dial. `flybys-compact.svg` puts the
list under the dial, drops the speeds and uses larger text, for phones; the README swaps it
in with <picture>.
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
SMALL = panel.SMALL

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


def moment(row):
    """JPL's '2026-Oct-27 01:10' (TDB, within a minute of UTC) as a datetime."""
    return dt.datetime.strptime(row["time"], "%Y-%b-%d %H:%M")


def when(row):
    """'Tue 27 Oct'."""
    t = moment(row)
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
        ".fly { animation: fly 1.8s cubic-bezier(0.2, 0.7, 0.2, 1) both; }",
        "@keyframes fly { from { transform: translate(var(--dx), var(--dy)); opacity: 0; } 25% { opacity: 1; } }",
        *panel.FADE,
    ), animated=("fly", "fade"))


def delay(k, after=0.0):
    return f"animation-delay:{0.2 + after + 0.15 * k:.2f}s"


def dial(cx, cy, r_max, size, full):
    """The week round Earth, and each asteroid at its moment and distance."""
    r_min = size * 1.5
    start = dt.datetime.combine(FROM, dt.time())
    days = (TO - FROM).days
    rad = lambda v: r_min + (r_max - r_min) * math.sqrt(min(max(v, 0), MAX_LD) / MAX_LD)
    turn = lambda t: -math.pi / 2 + 2 * math.pi * min(max((t - start).total_seconds() / (days * 86400), 0), 1)
    pt = lambda a, r: (cx + r * math.cos(a), cy + r * math.sin(a))
    parts = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size * 1.6:.1f}" fill="url(#halo)"/>',
             f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size * 0.85:.1f}" fill="url(#earth)"/>']
    # A spoke at each midnight, and the day's name in the middle of its wedge.
    for k in range(days):
        (x1, y1), (x2, y2) = (pt(turn(start + dt.timedelta(days=k)), r) for r in (r_min, r_max + 6))
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#2a3b63" stroke-width="1"/>')
        day = FROM + dt.timedelta(days=k)
        lx, ly = pt(turn(start + dt.timedelta(days=k + 0.5)), r_max + size * 1.7)
        parts.append(f'<text x="{lx:.1f}" y="{ly + size * 0.3:.1f}" text-anchor="middle" font-size="{size * SMALL:.1f}" '
                     f'fill="{DIM}">{f"{day:%a} {day.day}" if full else f"{day:%a}"}</text>')
    # The rings, the Moon's dashed in gold; the others labelled just clockwise of twelve.
    for v in (1, 5, 10, MAX_LD):
        style = f'stroke="{GOLD}" stroke-opacity="0.65" stroke-dasharray="3 4"' if v == 1 else 'stroke="#2a3b63"'
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad(v):.1f}" fill="none" {style} stroke-width="1.2"/>')
    for v in (5, 10, MAX_LD):
        parts.append(f'<text x="{cx + 4:.1f}" y="{cy - rad(v) - 4:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">{v} LD</text>')
    parts.append(f'<text x="{cx + rad(1) + 4:.1f}" y="{cy + size * 0.3:.1f}" font-size="{size * SMALL:.1f}" fill="{GOLD}">Moon</text>')
    biggest = max((size_m(r)[1] for r in ROWS if size_m(r)), default=1)
    for k, r in enumerate(ROWS):
        a = turn(moment(r))
        x, y = pt(a, rad(ld(r)))
        s = size_m(r)
        # Dot area follows the likely width (the middle of the range), from a speck to a marble.
        radius = size * (0.25 + 0.4 * math.sqrt(math.sqrt(s[0] * s[1]) / biggest)) if s else size * 0.25
        ox, oy = pt(a, r_max + size * 2)
        parts.append(f'<circle class="fly" cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="url(#rock)" '
                     f'style="--dx:{ox - x:.1f}px;--dy:{oy - y:.1f}px;{delay(k)}"/>')
        # Its number beside it, clockwise of it (out of the day names' way), once it has arrived.
        off = radius + size * 0.55
        parts.append(f'<text class="fade" x="{x - math.sin(a) * off:.1f}" y="{y + math.cos(a) * off + size * 0.3:.1f}" '
                     f'text-anchor="middle" font-size="{size * 0.8:.1f}" font-weight="700" fill="{TEXT}" '
                     f'style="{delay(k, 1.0)}">{k + 1}</text>')
    return parts


KEY = "Clockwise: the week. Outward: distance. Dot: likely width."


def header(x, y, size, full):
    """The count, the week and the closest pass. Returns the parts and the y the list starts at."""
    big = size * 2.75
    unit = "lunar distances" if full else "LD"
    closest = (f"Closest: {CLOSEST['des']}, {ld(CLOSEST):.1f} {unit} on {when(CLOSEST)}." if CLOSEST else "None this week.")
    line1 = f'{"asteroid passes" if COUNT == 1 else "asteroids pass"} Earth within {MAX_LD} {unit}'
    line2 = f"{span()}. {closest}"
    # Phones get the key under the header, where the dial follows.
    key = [] if full else [f'<text x="{x}" y="{y + big * 0.8 + size * 2.8:.1f}" font-size="{size * SMALL:.1f}" '
                           f'fill="{DIM}">Clockwise: the week. Outward: distance.</text>']
    base = y + big * 0.8
    return [f'<text x="{x}" y="{base:.1f}" font-size="{big:.1f}" font-weight="700" fill="{BLUE}">{COUNT}</text>',
            f'<text x="{x + big * 0.62 * len(str(COUNT)) + size * 0.6:.1f}" y="{base:.1f}" font-size="{size}" '
            f'fill="{TEXT}">{line1}</text>',
            f'<text x="{x}" y="{base + size * 1.6:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">{html.escape(line2)}</text>',
            *key], base + size * (1.6 if full else 2.8)


def listing(x, top, size, row_gap, full):
    """One line for each asteroid on the dial, numbered as there."""
    if not ROWS:
        return [f'<text x="{x}" y="{top:.1f}" font-size="{size}" fill="{DIM}">no asteroid comes this close this week</text>']
    parts = []
    for k, r in enumerate(ROWS):
        y = top + k * row_gap
        parts.append(f'<circle cx="{x + size * 0.55:.1f}" cy="{y - size * 0.33:.1f}" r="{size * 0.58:.1f}" fill="none" '
                     f'stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.2"/>')
        parts.append(f'<text x="{x + size * 0.55:.1f}" y="{y - size * 0.05:.1f}" text-anchor="middle" '
                     f'font-size="{size * 0.75:.1f}" font-weight="700" fill="{TEXT}">{k + 1}</text>')
        parts.append(f'<text x="{x + size * 1.6:.1f}" y="{y:.1f}" font-size="{size}" fill="#b9c6e4">{html.escape(r["des"])}</text>')
        facts = (f"{ld(r):.1f} LD · {size_text(r)} · {r['v_kms']:.1f} km/s · {when(r)}" if full
                 else f"{ld(r):.1f} LD · {size_text(r)} · {when(r).split()[0]}")
        parts.append(f'<text class="fade" x="{x + size * 7.4:.1f}" y="{y:.1f}" font-size="{size * 0.9:.1f}" '
                     f'fill="{TEXT}" style="{delay(k)}">{html.escape(facts)}</text>')
    more = f"And {COUNT - len(ROWS)} more farther out. " if COUNT > len(ROWS) else ""
    if more or full:
        parts.append(f'<text x="{x}" y="{top + (len(ROWS) - 0.2) * row_gap:.1f}" font-size="{size * SMALL:.1f}" '
                     f'fill="{DIM}">{more}{"From NASA/JPL close-approach data, every Monday." if full else ""}</text>')
    if full:
        parts.append(f'<text x="{x}" y="{top + (len(ROWS) + 0.7) * row_gap:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
                     f'{KEY}</text>')
    return parts


def render(w, seed, pad, size, row_gap, r_max, full):
    margin = size * 2.8                     # room for the day names round the dial
    lines = max(len(ROWS), 1) + (2 if full else COUNT > len(ROWS))
    if full:                                # the dial on the left, the header and list beside it
        cx = cy = pad + margin + r_max
        x = round(cx + r_max + margin + size)
        head, base = header(x, pad + size * 0.3, size, full)
        body = dial(cx, cy, r_max, size, full) + head + listing(x, base + row_gap * 1.3, size, row_gap, full)
        h = round(max(cy + r_max + margin, base + row_gap * (lines + 0.9)) + pad * 0.6)
    else:                                   # the header, the dial under it, the list under that
        head, base = header(pad, pad * 0.6, size, full)
        cx, cy = w / 2, base + margin + r_max + size
        top = cy + r_max + margin + size
        body = head + dial(cx, cy, r_max, size, full) + listing(pad, top, size, row_gap, full)
        h = round(top + (lines - 0.4) * row_gap + pad * 0.8)
    parts = [background(w, h, seed), f'<g font-family="{FONT}">', *body, "</g>\n</svg>\n"]
    return panel.keep_clear("\n".join(parts))


def update_readme(readme):
    """The README with this chart's alt text written in, so a screen reader hears what it
    shows. refresh_flybys.py calls it after refreshing; check.py checks it."""
    readme = panel.write_alt(readme, "flybys.svg", ALT)
    return readme


def files():
    return {
        "flybys.svg": render(1200, 41, 36, 19, 42, 200, True),
        "flybys-compact.svg": render(680, 42, 36, 24, 46, 230, False),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for file, svg in files().items():
        (out / file).write_text(svg, encoding="utf-8", newline="\n")
        print(file)


if __name__ == "__main__":
    main()
