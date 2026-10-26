"""Generate the activity sparklines under each repo's name in the README (docs/sparks/*.svg):
my commits to that repo week by week, from its first commit to the week
refresh_activity.py last ran.

Each runs over its own repo's life, not one shared axis: most of the repos are a few weeks
old, and on an axis as long as the oldest one's they were a squiggle at the right edge.
The README's alt text, which update_readme() writes, says when each line starts, how many
commits it holds and its busiest week. Heights are each repo's own too, scaled
to its busiest week, so a quiet repo's shape still shows. The last commit is a gold dot,
edged in the line's blue so it shows on a white page. When the page loads the line draws
itself left to right; with reduced motion it is drawn finished.

The numbers are refresh_activity.py's, from tools/counts.json. Drawn at twice the size
the README shows them, so they stay sharp on high-DPI screens.

    python tools/sparks.py docs/sparks
"""
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path

from loc import README_NAMES

BLUE, GOLD, TRACK = "#5ba3dc", "#e8c27a", "#2a3b63"
W, H, PAD = 240, 48, 7          # drawn size; the README shows it at half (width="120")

ACTIVITY = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["activity"]
AS_OF = dt.date.fromisoformat(ACTIVITY["as_of"])
monday = lambda d: d - dt.timedelta(days=d.weekday())
FIRST = monday(min(dt.date.fromisoformat(r["first"]) for r in ACTIVITY["repos"].values()))
N_WEEKS = (monday(AS_OF) - FIRST).days // 7 + 1


def spark(repo):
    r = ACTIVITY["repos"][repo]
    counts = [0] * N_WEEKS
    for week, n in r["weeks"].items():
        i = (dt.date.fromisoformat(week) - FIRST).days // 7
        if 0 <= i < N_WEEKS:
            counts[i] += n
    start = (monday(dt.date.fromisoformat(r["first"])) - FIRST).days // 7
    peak = max(counts) or 1
    x = lambda i: PAD + (W - 2 * PAD) * (i - start) / max(N_WEEKS - 1 - start, 1)
    # Square-root heights, so a busy week doesn't flatten the rest to the floor.
    y = lambda n: H - PAD - (H - 2 * PAD) * math.sqrt(n / peak)
    pts = [(x(i), y(counts[i])) for i in range(start, N_WEEKS)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{pts[0][0]:.1f},{H - PAD} {line} {pts[-1][0]:.1f},{H - PAD}"
    length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:])) or 1
    last = (monday(dt.date.fromisoformat(r["last"])) - FIRST).days // 7
    lx, ly = x(last), y(counts[last])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">
<style>
  .draw {{ stroke-dasharray: {length:.0f}; animation: draw 1.6s ease-out both; }}
  @keyframes draw {{ from {{ stroke-dashoffset: {length:.0f}; }} to {{ stroke-dashoffset: 0; }} }}
  .fade {{ animation: fade 0.6s ease-out 1.2s both; }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .draw, .fade {{ animation: none; }} }}
</style>
<line x1="{PAD}" y1="{H - PAD}" x2="{W - PAD}" y2="{H - PAD}" stroke="{TRACK}" stroke-width="1.5"/>
<polygon class="fade" points="{area}" fill="{BLUE}" fill-opacity="0.3"/>
<polyline class="draw" points="{line}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
<circle class="fade" cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="{GOLD}" stroke="{BLUE}" stroke-width="2"/>
</svg>
"""


def alt(name, r):
    """A sparkline in words: whose, from when, and what it adds up to."""
    first = dt.date.fromisoformat(r["first"])
    return (f"My commits to {name} each week since {first:%B %Y}: {sum(r['weeks'].values()):,} in all, "
            f"{max(r['weeks'].values()):,} in the busiest week")


def update_readme(readme):
    """The README with each sparkline's alt text written in. refresh_activity.py calls it after
    refreshing the counts; check.py checks it. Stops if a repo's sparkline isn't in the README
    exactly once."""
    for repo, r in ACTIVITY["repos"].items():
        pattern = rf'(src="docs/sparks/{re.escape(repo)}\.svg" width="120" alt=")[^"]*(")'
        readme, n = re.subn(pattern, lambda m: m[1] + alt(README_NAMES.get(repo, repo), r) + m[2], readme)
        if n != 1:
            sys.exit(f"README image docs/sparks/{repo}.svg matched {n} times, expected 1")
    return readme


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for repo in ACTIVITY["repos"]:
        (out / f"{repo}.svg").write_text(spark(repo), encoding="utf-8", newline="\n")
        print(repo)


if __name__ == "__main__":
    main()
