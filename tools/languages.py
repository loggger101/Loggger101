"""Generate the languages panel (docs/languages.svg, docs/languages-compact.svg): the lines of
code in the repos the README lists, split by language, with the repos each is mostly in.

The numbers are loc.py's, from tools/counts.json, so they add up to the counts under the
repos' names and follow the same rules (see loc.py). The smallest languages share a row.

`languages.svg` is for desktop widths. `languages-compact.svg` drops the repo names and
uses larger text, for phones; the README swaps it in with <picture>.
"""
import html
import json
import random
import re
import sys
from pathlib import Path

from loc import README_NAMES

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM = "#5ba3dc", "#dbe3f5", "#7d8fb3"
ROWS = 6            # languages with a row of their own; the rest share one

LANGUAGES = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["languages"]
by_language = {}    # language: {repo: lines of code}
for repo, langs in LANGUAGES.items():
    for lang, n in langs.items():
        by_language.setdefault(lang, {})[repo] = n
TOTAL = sum(sum(r.values()) for r in by_language.values())
ranked = sorted(by_language, key=lambda lang: (-sum(by_language[lang].values()), lang))
rest = ranked[ROWS:]
# (label, lines, repos most first, the languages a shared row holds)
rows = [(lang, sum(by_language[lang].values()), by_language[lang], [lang]) for lang in ranked[:ROWS]]
if rest:
    repos = {}
    for lang in rest:
        for repo, n in by_language[lang].items():
            repos[repo] = repos.get(repo, 0) + n
    rows.append((f"{len(rest)} others", sum(repos.values()), repos, rest))


def pct(n):
    p = 100 * n / TOTAL
    return f"{p:.1f}%" if p >= 0.1 else "<0.1%"


def where(repos, langs):
    """'economicspace, Mars Global Mosaic and 11 more', or the languages for a shared row."""
    if len(langs) > 1:
        return ", ".join(langs)
    names = [README_NAMES.get(r, r) for r, _ in sorted(repos.items(), key=lambda kv: (-kv[1], kv[0]))]
    # Two names at most: three of the longer ones overrun the panel.
    if len(names) <= 2:
        return " and ".join(names)
    return f"{names[0]}, {names[1]} and {len(names) - 2} more"


def spoken(label, langs):
    """A row's name for the alt text: the shared row names its languages."""
    return label if len(langs) == 1 else f"{', '.join(langs[:-1])} and {langs[-1]}"


ALT = (f"{TOTAL:,} lines of code in {len(ranked)} languages: "
       + ", ".join(f"{spoken(label, langs)} {n:,} ({pct(n)})" for label, n, _, langs in rows) + ".")


def background(w, h, seed):
    rng = random.Random(seed)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, w - 8):.1f}" cy="{rng.uniform(8, h - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(int(w * h / 4500))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(ALT)}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#112650"/></linearGradient></defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#g)" stroke="#2a3b63"/>
{stars}
"""


def render(w, seed, pad, big, size, row_gap, name_w, bar_w, num_w, with_repos):
    top = pad + big * 0.8 + size * 1.5 + row_gap * 1.1
    h = round(top + (len(rows) - 1) * row_gap + pad * 1.1)
    parts = [background(w, h, seed), f'<g font-family="{FONT}">',
             f'<text x="{pad}" y="{pad + big * 0.8:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">{TOTAL:,}</text>',
             f'<text x="{pad}" y="{pad + big * 0.8 + size * 1.5:.1f}" font-size="{size}" fill="{TEXT}">'
             f'lines of code in {len(ranked)} languages</text>']
    most = rows[0][1]
    bar_x = pad + name_w
    for k, (label, n, repos, langs) in enumerate(rows):
        y = top + k * row_gap
        shared = len(langs) > 1
        parts.append(f'<text x="{pad}" y="{y:.1f}" font-size="{size}" fill="{DIM if shared else "#b9c6e4"}">{label}</text>')
        parts.append(f'<rect x="{bar_x}" y="{y - size * 0.62:.1f}" width="{bar_w}" height="{size * 0.6:.1f}" rx="{size * 0.3:.1f}" fill="#13213f"/>')
        parts.append(f'<rect x="{bar_x}" y="{y - size * 0.62:.1f}" width="{max(bar_w * n / most, size * 0.6):.1f}" '
                     f'height="{size * 0.6:.1f}" rx="{size * 0.3:.1f}" fill="{DIM if shared else BLUE}"/>')
        num_x = bar_x + bar_w + num_w
        parts.append(f'<text x="{num_x:.1f}" y="{y:.1f}" text-anchor="end" font-size="{size}" fill="{TEXT}">{n:,}</text>')
        parts.append(f'<text x="{num_x + size * 0.6:.1f}" y="{y:.1f}" font-size="{size}" fill="{DIM}">{pct(n)}</text>')
        if with_repos:
            parts.append(f'<text x="{num_x + size * 4.6:.1f}" y="{y:.1f}" font-size="{size * 0.9:.1f}" fill="#b9c6e4">{where(repos, langs)}</text>')
    parts.append("</g>\n</svg>\n")
    return "\n".join(parts)


def update_readme(readme):
    """The README with this panel's alt text written in, so a screen reader hears the numbers
    the image shows. loc.py calls it after refreshing the counts; check.py checks it."""
    pattern = r'(src="docs/languages\.svg" width="100%" alt=")[^"]*(")'
    readme, n = re.subn(pattern, lambda m: m[1] + html.escape(ALT) + m[2], readme)
    if n != 1:
        sys.exit(f"README image docs/languages.svg matched {n} times, expected 1")
    return readme


def files():
    return {
        "languages.svg": render(1200, 21, 40, 52, 19, 40, 170, 380, 96, True),
        "languages-compact.svg": render(680, 22, 44, 60, 25, 46, 190, 200, 110, False),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, svg in files().items():
        (out / name).write_text(svg, encoding="utf-8", newline="\n")
        print(name)


if __name__ == "__main__":
    main()
