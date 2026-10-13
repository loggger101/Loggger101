"""Count the lines of code in each repo the profile lists, and write them into the README.

Counts what is on each repo's default branch on GitHub, not a local clone: it makes a
shallow partial clone that downloads only the source files (General_Research is 833 MB,
almost all of it hosted papers), counts them, and deletes it.

The rules are the usual ones, cloc's for counting lines and GitHub Linguist's for which
files are code:
- A line of code has code on it. Blank lines and comment-only lines don't count; a line
  with code and a trailing comment does. Python docstrings count as comments (cloc's
  default), and notebooks count their code cells only.
- Programming and markup languages count (Python, JavaScript, HTML, CSS, shell, Perl,
  PowerShell, batch, VBScript, Dockerfiles, scripts found by their #! line). Data and
  prose don't (JSON, YAML, TOML, CSV, Markdown, TeX).
- Files a repo marks linguist-generated, linguist-vendored or linguist-documentation in
  its .gitattributes don't count, nor do vendored folders and minified files. Identical
  files count once.
- REPOS lists what each repo generates, archives or hosts without marking it (the two
  nonprofit sites commit their built pages; General_Research hosts papers).

Writes tools/counts.json ("loc") and the "N lines of code" line under each repo's name in
the README. The private repos (aspirecures, SistersHopeFoundation) need your own GitHub
login to clone; with --public-only, which the weekly workflow uses, they keep the count
already in counts.json.

    python tools/loc.py                 # every repo
    python tools/loc.py --public-only   # skip the private ones
"""
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import tokenize
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / "tools" / "counts.json"

# repo: (link in its README row, private, what it generates, archives or hosts without
# marking it in .gitattributes)
REPOS = {
    "economicspace": ("https://github.com/loggger101/economicspace", False, []),
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

# How each language marks comments.
BY_EXT = {
    ".py": "python", ".ipynb": "notebook",
    ".js": "c", ".mjs": "c", ".cjs": "c", ".ts": "c", ".css": "css",
    ".html": "html", ".htm": "html",
    ".sh": "hash", ".bash": "hash", ".command": "hash", ".r": "hash",
    ".pl": "perl", ".pm": "perl", ".ps1": "powershell",
    ".bat": "batch", ".cmd": "batch", ".vbs": "vbscript",
}
BY_NAME = {"Dockerfile": "hash", "Makefile": "hash"}
BY_SHEBANG = {"python": "python", "node": "c", "perl": "perl"}  # anything else uses '#'
LINGUIST = ("linguist-generated", "linguist-vendored", "linguist-documentation")


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
    # A multi-line string spans its blank lines too; a blank line never counts.
    blank = {i for i, l in enumerate(src.splitlines(), 1) if not l.strip()}
    return len(lines - blank)


def c_lines(src, line_comments=True):
    """Lines with code in C-style syntax (JavaScript; CSS without // comments). Quotes are
    tracked, so a /* or // inside a string is not a comment. One exception: a template
    literal can hold a whole program (a page's <script>, a stub module), and a line in it
    that starts with // is a comment line of that program, so it doesn't count."""
    code, line, i, n = set(), 1, 0, len(src)
    state, quote, quiet = "code", "", 0
    while i < n:
        ch, two = src[i], src[i:i + 2]
        if ch == "\n":
            line += 1
            if state == "line" or (state == "string" and quote != "`"):
                state = "code"
            if line_comments and state == "string":         # still inside a template literal
                end = src.find("\n", i + 1)
                if src[i + 1:end if end != -1 else n].lstrip().startswith("//"):
                    quiet = line
            i += 1
            continue
        if state == "code":
            if two == "/*":
                state, i = "block", i + 2
                continue
            if line_comments and two == "//":
                state, i = "line", i + 2
                continue
            if ch in "'\"`":
                state, quote = "string", ch
            if not ch.isspace():
                code.add(line)
        elif state == "block":
            if two == "*/":
                state, i = "code", i + 2
                continue
        elif state == "string":
            if line != quiet and not ch.isspace():
                code.add(line)
            if ch == "\\":
                i += 2
                if i - 1 < n and src[i - 1] == "\n":
                    line += 1
                continue
            if ch == quote:
                state = "code"
        i += 1
    return len(code)


def strip_blocks(src, start, end):
    return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: "\n" * m[0].count("\n"), src, flags=re.S)


def nonblank(src, comment):
    """Lines that aren't blank and don't match the comment regex."""
    return sum(1 for l in src.splitlines() if l.strip() and not re.match(comment, l))


def count(path, lang):
    src = path.read_text(encoding="utf-8", errors="replace")
    try:
        if lang == "python":
            return python_lines(src)
        if lang == "notebook":
            total = 0
            for cell in json.loads(src).get("cells", []):
                if cell["cell_type"] != "code":
                    continue
                text = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
                # %magic and !shell lines are code but not Python; stand in a statement for each.
                text = re.sub(r"(?m)^(\s*)[%!].*$", r"\1pass", text)
                total += python_lines(text)
            return total
    except (tokenize.TokenError, SyntaxError) as e:
        sys.exit(f"can't tokenize {path}: {e}")
    if lang == "c":
        return c_lines(src)
    if lang == "css":
        return c_lines(src, line_comments=False)
    if lang == "html":
        return nonblank(strip_blocks(src, "<!--", "-->"), r"$^")
    if lang == "batch":
        return nonblank(src, r"(?i)\s*@?(rem\b|::)")
    if lang == "vbscript":
        return nonblank(src, r"(?i)\s*('|rem\b)")
    if lang == "powershell":
        src = strip_blocks(src, "<#", "#>")
    if lang == "perl":
        src = re.split(r"(?m)^__(?:END|DATA)__\s*$", src)[0]       # the rest is data
        src = re.sub(r"(?ms)^=[a-zA-Z].*?^=cut\b.*?$", "", src)    # POD documentation
    return nonblank(src, r"\s*#")


def language(path, read_head):
    """The comment syntax a file uses, or None if it isn't code."""
    p = PurePosixPath(path)
    if p.suffix.lower() in BY_EXT:
        return BY_EXT[p.suffix.lower()]
    if p.name in BY_NAME or p.name.startswith("Dockerfile."):
        return BY_NAME.get(p.name, "hash")
    if p.suffix == "":
        head = read_head(path)
        # "#!/bin/bash", "#!/usr/bin/env python3": the interpreter's name, letters only.
        m = re.match(rb"#!\s*(?:\S*/)?(?:env\s+(?:-\S+\s+)*)?([A-Za-z]+)", head)
        if m:
            return BY_SHEBANG.get(m[1].decode(), "hash")
    return None


def linguist_excluded(path, rules):
    """Whether .gitattributes marks the path generated, vendored or documentation."""
    state = dict.fromkeys(LINGUIST, False)
    for pattern, attrs in rules:
        p = pattern.lstrip("/").replace("**", "*")
        hit = fnmatch(PurePosixPath(path).name, p) if "/" not in pattern.rstrip("/") else fnmatch(path, p)
        if not hit:
            continue
        for a in attrs:
            name, _, value = a.lstrip("-!").partition("=")
            if name in state:
                state[name] = not a.startswith(("-", "!")) and value != "false"
    return any(state.values())


def gitattributes(repo):
    f = repo / ".gitattributes"
    rules = []
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if parts and not parts[0].startswith("#"):
                rules.append((parts[0], parts[1:]))
    return rules


def excluded(path, patterns):
    if any(fnmatch(path, p[1:]) for p in patterns if p.startswith("!")):
        return False
    return any(fnmatch(path, p) for p in patterns if not p.startswith("!"))


def repo_loc(name, excludes):
    with tempfile.TemporaryDirectory() as tmp:
        url = f"https://github.com/loggger101/{name}.git"
        run = lambda *a, **kw: subprocess.run(a, cwd=tmp, check=True, capture_output=True, **kw)
        run("git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse", url, "r")
        repo = Path(tmp, "r")
        # No -l: asking a partial clone for blob sizes downloads every blob, one at a time.
        listing = run("git", "-C", "r", "ls-tree", "-r", "-z", "HEAD").stdout.decode("utf-8").split("\0")
        paths = []
        for entry in filter(None, listing):
            meta, path = entry.split("\t", 1)
            mode, kind, _ = meta.split()
            if kind == "blob" and mode != "120000":      # files, not submodules or symlinks
                paths.append(path)
        # Fetch the source files, plus every extensionless file so its #! line can be read
        # (in these repos they are git hooks, licences and ArcGIS log messages, all small).
        escape = lambda p: "/" + re.sub(r"([\\*?\[!#])", r"\\\1", p)
        maybe = [escape(p) for p in paths if PurePosixPath(p).suffix == ""]
        patterns = ["/.gitattributes", "Dockerfile*", "Makefile", *[f"*{e}" for e in BY_EXT], *maybe]
        run("git", "-C", "r", "sparse-checkout", "set", "--no-cone", "--stdin", input="\n".join(patterns).encode())
        rules = gitattributes(repo)
        head = lambda p: (repo / p).read_bytes()[:128]
        total, seen = 0, set()
        for path in sorted(paths):
            if excluded(path, EXCLUDE + excludes) or linguist_excluded(path, rules):
                continue
            lang = language(path, head)
            if lang is None:
                continue
            if not (repo / path).is_file():
                sys.exit(f"{name}: {path} wasn't checked out")
            digest = hashlib.sha1((repo / path).read_bytes()).digest()
            if digest in seen:          # identical files count once, as cloc does
                continue
            seen.add(digest)
            total += count(repo / path, lang)
        return total


def update_readme(readme, loc):
    """The README with these line counts written in. check.py calls it with the stored counts."""
    for name, (link, _, _) in REPOS.items():
        # The repo's name cell: <b><a href="LINK">Name</a></b><br/><sub>role</sub>, then this line.
        pattern = (r'(<b><a href="' + re.escape(link) + r'">[^<]*</a></b><br/><sub>[^<]*</sub>)'
                   r'(?:<br/><sub>[\d,]+ lines of code</sub>)?')
        readme, n = re.subn(pattern, lambda m: f"{m[1]}<br/><sub>{loc[name]:,} lines of code</sub>", readme)
        if n != 1:
            sys.exit(f"README row for {name} matched {n} times, expected 1")
    return readme


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
    readme = update_readme(readme_path.read_text(encoding="utf-8"), loc)
    data["loc"] = {name: loc[name] for name in REPOS}
    readme_path.write_text(readme, encoding="utf-8", newline="\n")
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
