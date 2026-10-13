"""Generate docs/typing.svg: the line under the banner that types out each research area.

Self-hosted so the top of the profile does not depend on a third-party image service.
Uses SMIL only (works inside <img>, where scripts are stripped), and system monospace
fonts, so character width is estimated at 0.6 em and each line is centred from that.

The text sits on its own dark bar, styled like the link buttons below it, so it keeps
its contrast in GitHub's light theme as well as the dark one. The bar is as wide as the
longest line plus padding; the README's <img width> should match W.
"""
import sys

LINES = [
    "Asteroid catalogs and mining economics",
    "Asteroid belt origins and Mars mapping",
    "Deep learning on survey imagery",
    "Orbit simulation in pure Python",
]
SIZE = 18
CHAR = 0.6 * SIZE          # estimated monospace advance
H = 36
W = round(max(len(s) for s in LINES) * CHAR + 2 * 36)
TYPE_PER_CHAR = 0.06       # seconds per character typed
HOLD = 1.8                 # seconds the full line stays up
ERASE = 0.35               # seconds to clear it
COLOR = "#5BA3DC"

slots = [len(s) * TYPE_PER_CHAR + HOLD + ERASE for s in LINES]
T = sum(slots)


def kt(t):
    return f"{t / T:.4f}"


out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
    f'aria-label="{". ".join(LINES)}.">',
    "<defs>",
]
body = []
start = 0.0
for i, (line, slot) in enumerate(zip(LINES, slots)):
    width = len(line) * CHAR
    x0 = (W - width) / 2
    typed = start + len(line) * TYPE_PER_CHAR
    held = typed + HOLD
    end = start + slot
    # Clip width grows in whole-character steps while typing, then holds, then drops to zero.
    times, widths = ["0"], ["0"]
    if start > 0:
        times.append(kt(start)); widths.append("0")
    for c in range(1, len(line) + 1):
        times.append(kt(start + c * TYPE_PER_CHAR)); widths.append(f"{c * CHAR:.1f}")
    times.append(kt(held)); widths.append(f"{width:.1f}")
    times.append(kt(held + 0.02)); widths.append("0")
    if end < T - 1e-9:
        times.append("1"); widths.append("0")
    else:
        times[-1] = "1"
    out.append(
        f'<clipPath id="c{i}"><rect x="{x0:.1f}" y="0" width="0" height="{H}">'
        f'<animate attributeName="width" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{";".join(times)}" values="{";".join(widths)}"/></rect></clipPath>'
    )
    body.append(
        f'<text x="{x0:.1f}" y="{H / 2 + SIZE * 0.35:.1f}" clip-path="url(#c{i})" fill="{COLOR}" '
        f'font-size="{SIZE}" font-family="Consolas, Menlo, \'DejaVu Sans Mono\', \'Courier New\', monospace" '
        f'textLength="{width:.1f}" lengthAdjust="spacing" xml:space="preserve">{line}</text>'
    )
    # Cursor follows the typed edge while this line is active.
    cx_times, cx_vals = ["0"], [f"{x0:.1f}"]
    for c in range(1, len(line) + 1):
        cx_times.append(kt(start + c * TYPE_PER_CHAR)); cx_vals.append(f"{x0 + c * CHAR:.1f}")
    vis_times = ["0", kt(start), kt(held)] if start > 0 else ["0", kt(held)]
    vis_vals = ["0", "1", "0"] if start > 0 else ["1", "0"]
    body.append(
        f'<rect y="{H / 2 - SIZE * 0.55:.1f}" width="2" height="{SIZE * 1.1:.1f}" fill="{COLOR}" opacity="0">'
        f'<animate attributeName="x" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{";".join(cx_times)}" values="{";".join(cx_vals)}"/>'
        f'<animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{";".join(vis_times)}" values="{";".join(vis_vals)}"/></rect>'
    )
    start = end

out.append("</defs>")
out.append(f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="{H / 2 - 0.75}" fill="#13213f" stroke="#2f4a7a" stroke-width="1.5"/>')
out += body
out.append("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print(f"ok, cycle {T:.1f}s")
