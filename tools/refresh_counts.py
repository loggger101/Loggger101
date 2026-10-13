"""Refresh the counts that keep growing: research sources and agent skills.

Reads them from the source repos on GitHub, writes tools/counts.json, and rewrites the
README sentences and alt text that quote them. Run tiles.py afterwards to redraw the
tiles. The weekly workflow (.github/workflows/refresh-counts.yml) does both.

- sources: rows in General_Research's sources.csv (the registry; rejected sources are
  kept out of it, in INDEX.md).
- skills, skill_categories: the opening line of Hermes_Skills' README.

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
    return {"sources": sources, "skills": int(m[1]), "skill_categories": int(m[2])}


# Each README pattern must match exactly once.
README_PATTERNS = [
    (r'alt="\d[\d,]* research sources \(General_Research\)"',
     lambda c: f'alt="{c["sources"]:,} research sources (General_Research)"'),
    (r'alt="\d[\d,]* agent skills \(Hermes_Skills\)"',
     lambda c: f'alt="{c["skills"]:,} agent skills (Hermes_Skills)"'),
    (r"My library of \d[\d,]* agent skills in \d+ categories",
     lambda c: f"My library of {c['skills']:,} agent skills in {c['skill_categories']} categories"),
]


def main():
    counts = live_counts()
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    for pattern, repl in README_PATTERNS:
        readme, n = re.subn(pattern, repl(counts), readme)
        if n != 1:
            sys.exit(f"README pattern matched {n} times, expected 1: {pattern}")
    readme_path.write_text(readme, encoding="utf-8", newline="\n")
    (ROOT / "tools" / "counts.json").write_text(json.dumps(counts, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(" ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
