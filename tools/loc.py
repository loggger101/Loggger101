"""Count the lines of code in each repo the profile lists, and write them into the README.

Counts what is on each repo's default branch on GitHub, not a local clone: it makes a
shallow partial clone that downloads only the source files (General_Research is 833 MB,
almost all of it hosted papers), counts them, and deletes it.

A line of code is a line with code on it. Blank lines, comment lines and Python docstrings
don't count; notebooks count their code cells only. Config, data, prose and LaTeX don't
count. Neither do files the repo generates or archives (economicspace's master.py is its
modules joined together; the two nonprofit sites commit their built pages) or files it
hosts but didn't write (General_Research's full_texts).

Writes tools/counts.json ("loc") and the "N lines of code" line under each repo's name in
the README. The private repos (aspirecures, SistersHopeFoundation) need your own GitHub
login to clone; with --public-only, which the weekly workflow uses, they keep the count
already in counts.json.

    python tools/loc.py                 # every repo
    python tools/loc.py --public-only   # skip the private ones
"""
import io
import json
import re
import subprocess
import sys
import tempfile
import tokenize
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / "tools" / "counts.json"

# repo: (link in its README row, private, extra exclude patterns)
REPOS = {
    "economicspace": ("https://github.com/loggger101/economicspace", False, ["master.py"]),
    "AsteroidCatalog": ("https://github.com/loggger101/AsteroidCatalog", False, []),
    "spacecost": ("https://github.com/loggger101/spacecost", False, []),
    "General_Research": ("https://github.com/loggger101/General_Research", False, ["*/full_texts/*"]),
    "asteroid-belt-gradient": ("https://github.com/loggger101/asteroid-belt-gradient", False, []),
    "Mars_Terrestrial_GlobalMosaic_GIS-Data": ("https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data", False, []),
    "star-spectral-classifier": ("https://github.com/loggger101/star-spectral-classifier", False, []),
    "drone-target-id": ("https://github.com/loggger101/drone-target-id", False, []),
    "Satellite-Space-Flight": ("https://github.com/loggger101/Satellite-Space-Flight", False, []),
    "website": ("https://github.com/loggger101/website", False, []),
    # Pages are built by tools/build-*.pl and committed; the Perl is the source.
    "aspirecures": ("https://www.aspirecures.com", True, ["*.html"]),
    # archive/ is the old Squarespace site and content/ the page text; tools/build.py wraps each
    # page in templates/base.html and commits the result all over the tree.
    "SistersHopeFoundation": ("https://www.sistershopefoundation.org", True, ["archive/*", "content/*", "*.html", "!templates/*"]),
}
# Patterns match the whole path (fnmatch's * crosses "/"); a "!" pattern keeps what it matches.
EXCLUDE = ["*node_modules/*", "*vendor/*", "*third_party/*", "*.min.js", "*.min.css"]

HASH = {".sh", ".ps1", ".pl", ".pm", ".r"}       # '#' line comments
SLASH = {".js", ".mjs", ".ts", ".css"}           # '//' and /* */ comments
OTHER = {".py", ".ipynb", ".html", ".htm", ".bat"}
EXTS = HASH | SLASH | OTHER


def python_lines(src):
    """Lines holding a Python token other than a comment or a docstring."""
    lines, prev = set(), tokenize.NEWLINE
    tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
    for i, tok in enumerate(tokens):
        if tok.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                        tokenize.DEDENT, tokenize.ENDMARKER):
            if tok.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                prev = tok.type
            continue
        nxt = tokens[i + 1].type if i + 1 < len(tokens) else tokenize.ENDMARKER
        docstring = (tok.type == tokenize.STRING and prev in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)
                     and nxt in (tokenize.NEWLINE, tokenize.ENDMARKER))
        prev = tok.type
        if not docstring:
            lines.update(range(tok.start[0], tok.end[0] + 1))
    return len(lines)


def strip_blocks(src, start, end):
    return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: "\n" * m[0].count("\n"), src, flags=re.S)


def count(path):
    ext = path.suffix.lower()
    src = path.read_text(encoding="utf-8", errors="replace")
    if ext == ".py":
        try:
            return python_lines(src)
        except (tokenize.TokenError, SyntaxError, IndentationError) as e:
            sys.exit(f"can't tokenize {path}: {e}")
    if ext == ".ipynb":
        cells = json.loads(src).get("cells", [])
        code = ["".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in cells if c["cell_type"] == "code"]
        # Cells may hold %magics or !shell lines that don't tokenize; count those as code.
        return sum(1 for cell in code for l in cell.splitlines() if l.strip() and not l.lstrip().startswith("#"))
    if ext in (".html", ".htm"):
        src = strip_blocks(src, "<!--", "-->")
        return sum(1 for l in src.splitlines() if l.strip())
    if ext == ".bat":
        return sum(1 for l in src.splitlines() if l.strip() and not re.match(r"\s*(rem\b|::)", l, re.I))
    if ext in SLASH:
        src = strip_blocks(src, "/*", "*/")
        return sum(1 for l in src.splitlines() if l.strip() and not l.lstrip().startswith("//"))
    if ext == ".ps1":
        src = strip_blocks(src, "<#", "#>")
    if ext in (".pl", ".pm"):
        src = re.sub(r"^=[a-zA-Z].*?^=cut\b.*?$", "", src, flags=re.S | re.M)
    return sum(1 for l in src.splitlines() if l.strip() and not l.lstrip().startswith("#"))


def excluded(path, patterns):
    if any(fnmatch(path, p[1:]) for p in patterns if p.startswith("!")):
        return False
    return any(fnmatch(path, p) for p in patterns if not p.startswith("!"))


def repo_loc(name, excludes):
    with tempfile.TemporaryDirectory() as tmp:
        url = f"https://github.com/loggger101/{name}.git"
        run = lambda *a: subprocess.run(a, cwd=tmp, check=True, capture_output=True, text=True)
        run("git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse", url, "r")
        repo = Path(tmp, "r")
        run("git", "-C", "r", "sparse-checkout", "set", "--no-cone", *[f"*{e}" for e in sorted(EXTS)])
        files = run("git", "-C", "r", "ls-files").stdout.splitlines()
        total = 0
        for f in files:
            if Path(f).suffix.lower() not in EXTS or excluded(f, EXCLUDE + excludes):
                continue
            total += count(repo / f)
        return total


def main():
    public_only = "--public-only" in sys.argv[1:]
    data = json.loads(COUNTS.read_text(encoding="utf-8"))
    loc = data.get("loc", {})
    for name, (_, private, excludes) in REPOS.items():
        if private and public_only:
            if name not in loc:
                sys.exit(f"{name} is private and has no stored count; run without --public-only once")
            continue
        loc[name] = repo_loc(name, excludes)
        print(f"{loc[name]:>8,}  {name}")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    for name, (link, _, _) in REPOS.items():
        # The repo's name cell: <b><a href="LINK">Name</a></b><br/><sub>role</sub>, then this line.
        pattern = (r'(<b><a href="' + re.escape(link) + r'">[^<]*</a></b><br/><sub>[^<]*</sub>)'
                   r'(?:<br/><sub>[\d,]+ lines of code</sub>)?')
        readme, n = re.subn(pattern, lambda m: f"{m[1]}<br/><sub>{loc[name]:,} lines of code</sub>", readme)
        if n != 1:
            sys.exit(f"README row for {name} matched {n} times, expected 1")
    data["loc"] = {name: loc[name] for name in REPOS}
    readme_path.write_text(readme, encoding="utf-8", newline="\n")
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
