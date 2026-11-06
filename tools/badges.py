"""Fetch the badges under each project from shields.io into docs/badges/<name>.svg.

The README shows these copies, not shields' URLs: GitHub loads a remote image through its
proxy on the visitor's behalf, and if that fails the visitor sees a broken image. shields
still draws them, so the badges keep its look and its icons, and the release badges show
each repo's latest version as of the last refresh. To add a badge, add it to BADGES, run
this and use docs/badges/<name>.svg in the README.

Writes "badges" in tools/counts.json: the date it ran. Stops with an error, changing
nothing, if a badge can't be read or a release badge came back with shields' error text
(which it serves as an ordinary 200) in place of a version. The weekly workflow lets this
step fail without holding back the other counts: last week's badges stay, and check.py
--fresh notices if that goes on.

    python tools/badges.py docs/badges
"""
import base64
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / "tools" / "counts.json"
LOGOS = ROOT / "docs" / "logos"
SHIELDS = "https://img.shields.io"
NAVY, BLUE = "1f3354", "5ba3dc"


def tech(label, logo):
    return f"{SHIELDS}/badge/{label}-{NAVY}?style=flat-square&logo={logo}&logoColor=white"


def drawn(label, name):
    """A badge with a logo from badge_logos.py, which shields takes as a data URI."""
    svg = (LOGOS / f"{name}.svg").read_text(encoding="utf-8").strip()
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    return f"{SHIELDS}/badge/{label}-{NAVY}?style=flat-square&logo={urllib.parse.quote(uri, safe='')}"


def link(label, logo):
    return f"{SHIELDS}/badge/{label}-{BLUE}?style=flat-square&logo={logo}&logoColor=white"


def labeled(label, message, logo):
    return (f"{SHIELDS}/badge/{label}-{message}-{BLUE}?style=flat-square&labelColor={NAVY}"
            f"&logo={logo}&logoColor=white")


def release(repo, kind="release"):
    return (f"{SHIELDS}/github/v/{kind}/loggger101/{repo}?style=flat-square&label=release"
            f"&labelColor={NAVY}&color={BLUE}")


BADGES = {
    "python": tech("Python", "python"),
    "pandas": tech("pandas", "pandas"),
    "numpy": tech("NumPy", "numpy"),
    "scipy": tech("SciPy", "scipy"),
    "docker": tech("Docker", "docker"),
    "parquet": tech("Parquet", "apacheparquet"),
    "latex": tech("LaTeX", "latex"),
    "arcgis-pro": tech("ArcGIS_Pro", "arcgis"),
    "tensorflow": tech("TensorFlow", "tensorflow"),
    "yolo": tech("YOLO", "ultralytics"),
    "opencv": tech("OpenCV", "opencv"),
    "streamlit": tech("Streamlit", "streamlit"),
    "cloudflare-pages": tech("Cloudflare_Pages", "cloudflarepages"),
    "html5": tech("HTML5", "html5"),
    "css": tech("CSS", "css"),
    "javascript": tech("JavaScript", "javascript"),
    "markdown": tech("Markdown", "markdown"),
    "git": tech("git", "git"),
    "astropy": drawn("Astropy", "astropy"),
    "pygame": drawn("pygame", "pygame"),
    "matlab": drawn("MATLAB", "matlab"),
    "project-page": link("Project_page", "googlechrome"),
    "live-cloudflare": link("Live", "cloudflare"),
    "live-github": link("Live", "github"),
    "paper": labeled("Paper", "AASTeX", "latex"),
    "dataset": labeled("Dataset", "Kaggle", "kaggle"),
    "release-AsteroidCatalog": release("AsteroidCatalog"),
    "release-spacevalue": release("spacevalue"),
    "release-spacecost": release("spacecost"),
    "release-asteroid-belt-gradient": release("asteroid-belt-gradient"),
    "release-Mars_Terrestrial_GlobalMosaic_GIS-Data": release("Mars_Terrestrial_GlobalMosaic_GIS-Data"),
    "release-quietlaunch": release("quietlaunch"),
    "release-quietqueue": release("quietqueue"),
    "release-samebytes": release("samebytes", kind="tag"),
}


def problem_with(name, svg):
    """What's wrong with a fetched badge, or None. shields answers 200 with a badge saying
    "no releases or repo not found" or "rate limited by upstream service", and committing
    one would put that on the profile."""
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        return f"isn't valid XML: {e}"
    if not root.tag.endswith("}svg"):
        return f"is a <{root.tag}>, not an SVG"
    if name.startswith("release-") and not re.fullmatch(r"release: \S*\d\S*", root.get("aria-label", "")):
        return f"says {root.get('aria-label')!r}, not a version"
    return None


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (profile badge refresh)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    out = Path(sys.argv[1])
    today = dt.datetime.now(dt.timezone.utc).date()
    fetched = {}
    for name, url in BADGES.items():
        try:
            fetched[name] = fetch(url)
        except (OSError, ValueError) as e:
            sys.exit(f"shields.io couldn't draw the {name} badge: {e}")
        if why := problem_with(name, fetched[name]):
            sys.exit(f"the {name} badge {why}")
    out.mkdir(parents=True, exist_ok=True)
    for name, svg in fetched.items():
        (out / f"{name}.svg").write_text(svg.rstrip() + "\n", encoding="utf-8", newline="\n")
    data = json.loads(COUNTS.read_text(encoding="utf-8"))
    data["badges"] = {"as_of": today.isoformat()}
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(fetched)} badges")


if __name__ == "__main__":
    main()
