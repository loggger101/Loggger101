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

"Total lines" is every line of every text file of your own in the repo: the code with its
blank and comment lines, notebooks (all their cells, not their outputs), docs, the paper's
TeX, data, config and logs. It leaves out:
- binary files (images, PDFs, models, ArcGIS geodatabases);
- what lines of code also leave out for being built, archived, hosted or vendored (REPOS,
  EXCLUDE, linguist-generated and linguist-vendored; linguist-documentation still counts);
- TOTAL_EXCLUDE: other people's text (licences, a downloaded survey table, the AAS LaTeX
  template, fetched paper abstracts) and machine output (ArcGIS metadata, generated
  sitemaps and feeds, lock files).
Identical files count once.

Writes tools/counts.json ("loc", "lines", and "languages": each repo's lines of code split
by language, which languages.py draws) and the "N lines of code" and "N total lines" lines
under each repo's name in the README, and the languages panel's alt text. The private repos (aspirecures,
SistersHopeFoundation) need your own GitHub login to clone; with --public-only, which the
weekly workflow uses, they keep the counts already in counts.json.

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
    "starred-repos": ("https://github.com/loggger101/starred-repos", False, []),
    "asteroid-belt-gradient": ("https://github.com/loggger101/asteroid-belt-gradient", False, []),
    "Mars_Terrestrial_GlobalMosaic_GIS-Data": ("https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data", False, []),
    "star-spectral-classifier": ("https://github.com/loggger101/star-spectral-classifier", False, []),
    "drone-target-id": ("https://github.com/loggger101/drone-target-id", False, []),
    "Satellite-Space-Flight": ("https://github.com/loggger101/Satellite-Space-Flight", False, []),
    "website": ("https://github.com/loggger101/website", False, []),
    "quietlaunch": ("https://github.com/loggger101/quietlaunch", False, []),
    "quietqueue": ("https://github.com/loggger101/quietqueue", False, []),
    # Pages are built by tools/build-*.pl and committed; the Perl is the source.
    "aspirecures": ("https://www.aspirecures.com", True, ["*.html"]),
    # archive/ is the old Squarespace site and content/ the page text; tools/build.py wraps each
    # page in templates/base.html and commits the result all over the tree.
    "SistersHopeFoundation": ("https://www.sistershopefoundation.org", True, ["archive/*", "content/*", "*.html", "!templates/*"]),
}
# The name a repo's README row shows, where it isn't the repo's own (the panels use it).
README_NAMES = {"Mars_Terrestrial_GlobalMosaic_GIS-Data": "Mars Global Mosaic", "aspirecures": "AspireCURES",
                "SistersHopeFoundation": "Sisters Hope Foundation"}
# Patterns match the whole path (fnmatch's * crosses "/"); a "!" pattern keeps what it matches.
EXCLUDE = ["*node_modules/*", "*vendor/*", "*third_party/*", "*.min.js", "*.min.css"]

# Text files that stay out of the total lines though they aren't built or vendored, because
# someone else wrote them or a program did. repo: patterns ("*" applies to every repo).
TOTAL_EXCLUDE = {
    # Standard licence texts, and lock files pip and npm write.
    "*": ["LICENSE*", "*/LICENSE*", "requirements-lock.txt", "*package-lock.json"],
    # The SDSS asteroid taxonomy table, downloaded for a probe script.
    "starred-repos": ["sdsstax_ast.tab"],
    # The AAS journal class and bibliography styles the paper is set with.
    "asteroid-belt-gradient": ["paper/aastex*.cls", "paper/*.bst"],
    # ArcGIS writes these: training-sample dumps, raster metadata sidecars, world files,
    # geoprocessing messages, the unpacked .aprx project and the file geodatabase.
    # Plus the PDS label that came with a downloaded Mars mosaic.
    "Mars_Terrestrial_GlobalMosaic_GIS-Data": ["*/LabeledObjects/*", "*.aux.xml", "*.tif.xml", "*.tfw",
                                               "*/GpMessages/*", "*/aprx_live/*", "*.gdb/*", "*.lbl"],
    # Natural Earth coastlines.
    "Satellite-Space-Flight": ["assets/coastlines.json"],
    # The weekly research feed's output (paper titles and abstracts fetched from PubMed and
    # others, and the RSS feeds made from them), and the sitemap gen-sitemap.pl writes.
    "aspirecures": ["data/research/*", "research.xml", "research/*.xml", "sitemap.xml"],
    # tools/build.py writes the sitemap and llms.txt; build_events.py the calendar files.
    "SistersHopeFoundation": ["sitemap.xml", "llms.txt", "events/*.ics"],
}
# Not fetched, so General_Research's papers and the Mars rasters aren't downloaded. Anything
# else holding a NUL byte is binary too.
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".tif", ".tiff", ".pdf", ".zip", ".gz",
          ".xlsx", ".docx", ".pptx", ".parquet", ".npy", ".npz", ".h5", ".keras", ".pt", ".pkl",
          ".mp4", ".webm", ".mp3", ".wav", ".ttf", ".otf", ".woff", ".woff2",
          ".aprx", ".atbx", ".gdbtable", ".gdbtablx", ".gdbindexes", ".freelist", ".spx", ".atx",
          ".shp", ".shx", ".dbf", ".cpg", ".ecd", ".ecs", ".emd", ".gsg", ".horizon"}

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

# The language a file is in, by Linguist's names, for the languages panel (languages.py).
# Several share a comment syntax above, so this is its own table.
NAME_BY_EXT = {
    ".py": "Python", ".ipynb": "Jupyter Notebook",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".ts": "TypeScript", ".css": "CSS",
    ".html": "HTML", ".htm": "HTML",
    ".sh": "Shell", ".bash": "Shell", ".command": "Shell", ".r": "R",
    ".pl": "Perl", ".pm": "Perl", ".ps1": "PowerShell",
    ".bat": "Batchfile", ".cmd": "Batchfile", ".vbs": "VBScript",
}
# An extensionless script's language follows from the syntax its #! line gave it.
NAME_BY_SHEBANG = {"python": "Python", "c": "JavaScript", "perl": "Perl", "hash": "Shell"}


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


def total_lines(path, lang):
    """Every line of the file, blank and comment lines included (cloc's blank + comment +
    code). A notebook's are the lines of its cells, code and Markdown; its outputs are what
    the code printed, so they don't count."""
    src = path.read_text(encoding="utf-8", errors="replace")
    if lang == "notebook":
        cells = [c["source"] for c in json.loads(src).get("cells", [])]
        return sum(len(("".join(s) if isinstance(s, list) else s).splitlines()) for s in cells)
    return len(src.splitlines())


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


def language_name(path, syntax):
    """The language a code file is in (syntax is what language() gave it)."""
    p = PurePosixPath(path)
    if p.suffix.lower() in NAME_BY_EXT:
        return NAME_BY_EXT[p.suffix.lower()]
    if p.name == "Makefile":
        return "Makefile"
    if p.name == "Dockerfile" or p.name.startswith("Dockerfile."):
        return "Dockerfile"
    return NAME_BY_SHEBANG[syntax]


def linguist_excluded(path, rules, attrs=LINGUIST):
    """Whether .gitattributes marks the path with any of attrs (generated, vendored or
    documentation)."""
    state = dict.fromkeys(attrs, False)
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
        # Fetch every file that may be text and isn't built, archived or hosted.
        escape = lambda p: "/" + re.sub(r"([\\*?\[!#])", r"\\\1", p)
        wanted = [p for p in paths if PurePosixPath(p).suffix.lower() not in BINARY and not excluded(p, EXCLUDE + excludes)]
        patterns = ["/.gitattributes", *map(escape, wanted)]
        run("git", "-C", "r", "sparse-checkout", "set", "--no-cone", "--stdin", input="\n".join(patterns).encode())
        rules = gitattributes(repo)
        head = lambda p: (repo / p).read_bytes()[:128]
        not_own = TOTAL_EXCLUDE["*"] + TOTAL_EXCLUDE.get(name, [])
        code, total, seen_code, seen_all, by_language = 0, 0, set(), set(), {}
        for path in wanted:
            if linguist_excluded(path, rules, ("linguist-generated", "linguist-vendored")):
                continue
            if not (repo / path).is_file():
                sys.exit(f"{name}: {path} wasn't checked out")
            data = (repo / path).read_bytes()
            if b"\0" in data[:8000]:
                continue
            # Identical files count once, as cloc does.
            digest = hashlib.sha1(data).digest()
            lang = language(path, head)
            if lang and not linguist_excluded(path, rules) and digest not in seen_code:
                seen_code.add(digest)
                n = count(repo / path, lang)
                code += n
                lang_name = language_name(path, lang)
                by_language[lang_name] = by_language.get(lang_name, 0) + n
            if not excluded(path, not_own) and digest not in seen_all:
                seen_all.add(digest)
                total += total_lines(repo / path, lang)
        return code, total, {k: v for k, v in sorted(by_language.items(), key=lambda kv: -kv[1]) if v}


def update_readme(readme, loc, lines):
    """The README with these line counts written in. check.py calls it with the stored counts."""
    for name, (link, _, _) in REPOS.items():
        # The repo's name cell: <b><a href="LINK">Name</a></b><br/><sub>role</sub>, then these two lines.
        pattern = (r'(<b><a href="' + re.escape(link) + r'">[^<]*</a></b><br/><sub>[^<]*</sub>)'
                   r'(?:<br/><sub>[\d,]+ lines of code</sub>)?(?:<br/><sub>[\d,]+ total lines</sub>)?')
        readme, n = re.subn(pattern, lambda m: (f"{m[1]}<br/><sub>{loc[name]:,} lines of code</sub>"
                                                f"<br/><sub>{lines[name]:,} total lines</sub>"), readme)
        if n != 1:
            sys.exit(f"README row for {name} matched {n} times, expected 1")
    return readme


def main():
    public_only = "--public-only" in sys.argv[1:]
    data = json.loads(COUNTS.read_text(encoding="utf-8"))
    loc, lines, languages = data.get("loc", {}), data.get("lines", {}), data.get("languages", {})
    for name, (_, private, excludes) in REPOS.items():
        if private and public_only:
            if name not in loc or name not in lines or name not in languages:
                sys.exit(f"{name} is private and has no stored count; run without --public-only once")
            continue
        loc[name], lines[name], languages[name] = repo_loc(name, excludes)
        print(f"{loc[name]:>8,} code {lines[name]:>8,} total  {name}")

    readme_path = ROOT / "README.md"
    readme = update_readme(readme_path.read_text(encoding="utf-8"), loc, lines)
    data["loc"] = {name: loc[name] for name in REPOS}
    data["lines"] = {name: lines[name] for name in REPOS}
    data["languages"] = {name: languages[name] for name in REPOS}
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    import languages as panel     # reads the counts just written
    readme_path.write_text(panel.update_readme(readme), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
