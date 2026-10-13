"""Check the profile is consistent with itself. Runs offline, in a few seconds; CI runs it on
every push (.github/workflows/check.yml).

1. Every generated image in docs/ is what its generator makes today, so nothing was edited
   by hand or left behind after a generator changed. (gallery.py is skipped: it reads
   the project clones, which CI doesn't have.)
2. Every docs/ file the README uses exists, and every file in docs/ is used.
3. The README's numbers are the ones in tools/counts.json: rewriting the README from the
   stored counts, with refresh_counts.py's and loc.py's own code, changes nothing.
4. The typing line's <img width> matches the SVG's width, and the Astropy and pygame
   badges carry the logos badge_logos.py draws.
5. No OneDrive conflict copies (*-DESKTOP-*) are in the repo.
6. With --links (online; the weekly workflow): every link and badge in the README answers.

Prints each problem and exits 1 if there are any.
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"

# generator: the path under docs/ it is given (a file or a directory)
GENERATORS = {
    "banner.py": "banner.svg",
    "typing_line.py": "typing.svg",
    "footer.py": ".",
    "tiles.py": "stats",
    "pipeline.py": ".",
    "links.py": "links",
    "badge_logos.py": "logos",
}
# In docs/ but not made by a generator above.
NOT_GENERATED = {"spacer.svg"}
# In docs/ but not referenced by path: the logos reach the README inside badge URLs.
UNREFERENCED_OK = {"logos/astropy.svg", "logos/pygame.svg"}

problems = []


def lf(data):
    return data.replace(b"\r\n", b"\n")


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_generated():
    made, badge_urls = set(), []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        for script, target in GENERATORS.items():
            dest = out / target
            if target.endswith(".svg"):
                dest.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run([sys.executable, str(TOOLS / script), str(dest)], cwd=ROOT,
                               capture_output=True, text=True, encoding="utf-8")
            if r.returncode:
                problems.append(f"{script} failed:\n{r.stderr.strip()}")
                continue
            if script == "badge_logos.py":
                badge_urls = r.stdout.split()
        for f in sorted(p for p in out.rglob("*") if p.is_file()):
            rel = f.relative_to(out).as_posix()
            made.add(rel)
            have = DOCS / rel
            if not have.exists():
                problems.append(f"docs/{rel} is generated but not committed")
            elif lf(have.read_bytes()) != lf(f.read_bytes()):
                problems.append(f"docs/{rel} differs from what tools/ makes; rerun its generator")
    for f in sorted(p for p in DOCS.rglob("*") if p.is_file()):
        rel = f.relative_to(DOCS).as_posix()
        if rel not in made and rel not in NOT_GENERATED and not rel.startswith("gallery/"):
            problems.append(f"docs/{rel} has no generator; add it to GENERATORS or NOT_GENERATED")
    return badge_urls


def check_references(readme):
    used = set(re.findall(r'(?:src|srcset)="docs/([^"]+)"', readme))
    for rel in sorted(used):
        if not (DOCS / rel).is_file():
            problems.append(f"README uses docs/{rel}, which doesn't exist")
    for f in sorted(p for p in DOCS.rglob("*") if p.is_file()):
        rel = f.relative_to(DOCS).as_posix()
        if rel not in used and rel not in UNREFERENCED_OK:
            problems.append(f"docs/{rel} isn't used by the README")


def check_counts(readme):
    counts = json.loads((TOOLS / "counts.json").read_text(encoding="utf-8"))
    for name, update in (("refresh_counts", lambda m: m.update_readme(readme, counts)),
                         ("loc", lambda m: m.update_readme(readme, counts["loc"]))):
        try:
            rewritten = update(load(name))
        except SystemExit as e:
            problems.append(f"{name}.py can't find its place in the README: {e}")
            continue
        if rewritten != readme:
            problems.append(f"README numbers differ from tools/counts.json (rerun {name}.py)")


def check_typing_and_badges(readme, badge_urls):
    m = re.search(r'src="docs/typing\.svg" width="(\d+)"', readme)
    svg = re.search(r'<svg[^>]* width="(\d+)"', (DOCS / "typing.svg").read_text(encoding="utf-8"))
    if not m or not svg or m[1] != svg[1]:
        problems.append(f"typing line: README width {m and m[1]} but typing.svg is {svg and svg[1]}")
    for url in badge_urls:
        if url not in readme:
            problems.append(f"README badge isn't badge_logos.py's current output: {url[:70]}...")


def check_conflict_copies():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    on_disk = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*-DESKTOP-*") if ".git" not in p.parts]
    for f in sorted(set(on_disk) | {t for t in tracked if "-DESKTOP-" in t}):
        problems.append(f"OneDrive conflict copy: {f}")


# LinkedIn answers every script with 999; a 999 from it says nothing about the link.
LINK_STATUS_OK = {"www.linkedin.com": {999}}


def check_links(readme):
    """Every link and badge in the README answers. Online, so only with --links."""
    import urllib.error
    import urllib.parse
    import urllib.request
    urls = sorted(set(re.findall(r'(?:href|src)="(https?://[^"]+)"', readme)))
    for url in urls:
        req = urllib.request.Request(url.replace("&amp;", "&"), headers={"User-Agent": "Mozilla/5.0 (profile link check)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status = r.status
        except urllib.error.HTTPError as e:
            status = e.code
        except (urllib.error.URLError, TimeoutError) as e:
            problems.append(f"link unreachable: {url} ({e})")
            continue
        if status >= 400 and status not in LINK_STATUS_OK.get(urllib.parse.urlsplit(url).hostname, set()):
            problems.append(f"link answers {status}: {url}")
    print(f"checked {len(urls)} links")


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    badge_urls = check_generated()
    check_references(readme)
    check_counts(readme)
    check_typing_and_badges(readme, badge_urls)
    check_conflict_copies()
    if "--links" in sys.argv[1:]:
        check_links(readme)
    for p in problems:
        print(f"- {p}")
    if problems:
        sys.exit(f"{len(problems)} problem(s)")
    print("profile checks pass")


if __name__ == "__main__":
    main()
