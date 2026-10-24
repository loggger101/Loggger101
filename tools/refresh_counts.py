"""Refresh the counts that keep growing: research sources, agent skills, the catalog's
size, and where the mining pipeline stands.

Reads them from the source repos on GitHub, writes tools/counts.json, and rewrites the
README sentences and alt text that quote them. Run tiles.py and pipeline.py afterwards to
redraw the tiles and the repo diagram. The weekly workflow
(.github/workflows/refresh-counts.yml) does all of it.

- sources: rows in General_Research's sources.csv (the registry; rejected sources are
  kept out of it, in INDEX.md).
- skills, skill_categories: the opening line of Hermes_Skills' README.
- catalog_rows: the row count in the manifest of AsteroidCatalog's latest release, shown
  everywhere as millions to two places ("1.58M", "about 1.58 million").
- economics: the destinations table in economicspace's README, the latest full-catalog
  run for each place the pipeline delivers to (best cost per dollar of revenue, the
  winning asteroid, the median body's). breakeven.py draws it; this also writes that
  chart's alt text and the sentence above it into the README, so run breakeven.py
  afterwards to redraw the chart.

Stops with an error, changing nothing, if a source can't be read or a README sentence
it rewrites has gone missing, so a reworded README can't leave a stale number behind.
"""
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/loggger101"
MANIFEST = "https://github.com/loggger101/AsteroidCatalog/releases/latest/download/manifest.json"


def fetch(path):
    with urllib.request.urlopen(f"{RAW}/{path}", timeout=30) as r:
        return r.read().decode("utf-8")


def live_counts():
    sources = len(list(csv.DictReader(io.StringIO(fetch("General_Research/main/sources.csv")))))
    m = re.search(r"\*\*(\d+) Hermes Agent skills\*\* across (\d+) categories",
                  fetch("Hermes_Skills/main/README.md"))
    if not m:
        sys.exit("Hermes_Skills README no longer states its skill and category counts")
    if sources < 100:
        sys.exit(f"sources.csv has only {sources} rows; refusing to publish that")
    with urllib.request.urlopen(MANIFEST, timeout=30) as r:
        rows = int(json.loads(r.read().decode("utf-8"))["rows"])
    if rows < 1_000_000:
        sys.exit(f"AsteroidCatalog's latest manifest says {rows} rows; refusing to publish that")
    return {"sources": sources, "skills": int(m[1]), "skill_categories": int(m[2]), "catalog_rows": rows,
            "economics": destinations(fetch("economicspace/main/README.md"))}


def millions(rows):
    """1575889 -> "1.58": how the profile writes the catalog's size, everywhere."""
    return f"{rows / 1e6:.2f}"


def destinations(readme):
    """The rows of economicspace's destinations table: [{dest, best, winner, median}].
    Bold, code marks and footnote signs are dropped; the winner is the asteroid and its
    taxonomy class, without the vehicle."""
    m = re.search(r"^#### Every destination at this release.*?^\| destination \| cost / revenue \| winner \| median body \|\n"
                  r"\|[-|]+\|\n((?:\|[^\n]*\|\n)+)", readme, re.M | re.S)
    if not m:
        sys.exit("economicspace's README no longer has its destinations table in the form expected")
    number = lambda cell: float(re.sub(r"[^\d.]", "", cell))   # "6,154.06x†" -> 6154.06
    rows = []
    for line in m[1].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # An asteroid's name has no comma, and a taxonomy class is one to three letters, so
        # "2015 DS, Falcon Heavy (expendable)" isn't taken for one.
        winner = len(cells) == 4 and re.match(r"([^,(]+? \([A-Za-z]{1,3}\))", cells[2])
        if not winner:
            sys.exit(f"economicspace's destinations table has a row this can't read: {line}")
        rows.append({"dest": re.sub(r"[*`]", "", cells[0]), "best": number(cells[1]),
                     "winner": winner[1], "median": number(cells[3])})
    if len(rows) < 5 or not all(r["best"] > 0 and r["median"] > 0 for r in rows):
        sys.exit(f"economicspace's destinations table doesn't look right: {rows}")
    return rows


# Each README pattern must match exactly once.
README_PATTERNS = [
    (r'alt="\d[\d,]* research sources \(General_Research\)"',
     lambda c: f'alt="{c["sources"]:,} research sources (General_Research)"'),
    (r'alt="\d[\d,]* agent skills \(Hermes_Skills\)"',
     lambda c: f'alt="{c["skills"]:,} agent skills (Hermes_Skills)"'),
    (r"My library of \d[\d,]* agent skills in \d+ categories",
     lambda c: f"My library of {c['skills']:,} agent skills in {c['skill_categories']} categories"),
    (r'alt="[\d.]+M asteroids cataloged \(AsteroidCatalog\)"',
     lambda c: f'alt="{millions(c["catalog_rows"])}M asteroids cataloged (AsteroidCatalog)"'),
    (r"I built a catalog of about [\d.]+ million of them",
     lambda c: f"I built a catalog of about {millions(c['catalog_rows'])} million of them"),
    (r"About [\d.]+ million asteroids from JPL SBDB",
     lambda c: f"About {millions(c['catalog_rows'])} million asteroids from JPL SBDB"),
]


def update_readme(readme, counts):
    """The README with these counts written in. check.py calls it with the stored counts."""
    for pattern, repl in README_PATTERNS:
        readme, n = re.subn(pattern, repl(counts), readme)
        if n != 1:
            sys.exit(f"README pattern matched {n} times, expected 1: {pattern}")
    return readme


def main():
    counts = live_counts()
    readme_path = ROOT / "README.md"
    readme = update_readme(readme_path.read_text(encoding="utf-8"), counts)
    readme_path.write_text(readme, encoding="utf-8", newline="\n")
    # counts.json also holds loc.py's line counts; keep them.
    path = ROOT / "tools" / "counts.json"
    data = json.loads(path.read_text(encoding="utf-8")) | counts
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    import breakeven    # reads the counts just written
    readme_path.write_text(breakeven.update_readme(readme_path.read_text(encoding="utf-8")),
                           encoding="utf-8", newline="\n")
    print(" ".join(f"{k}={v}" for k, v in counts.items() if k != "economics"))
    print(" ".join(f"{r['dest']}={r['best']}" for r in counts["economics"]))


if __name__ == "__main__":
    main()
