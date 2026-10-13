# Image generators

The banner, typing line, link buttons, stat tiles, repo diagram, gallery cards and footer in `docs/` are generated, not hand-edited.
Run from the repo root:

```bash
python tools/banner.py docs/banner.svg
python tools/refresh_counts.py         # pull the sources and skills counts from their repos
python tools/loc.py                    # lines of code under each repo's name (--public-only skips the private two)
python tools/tiles.py docs/stats      # full tiles plus the -compact versions phones get
python tools/gallery.py docs/gallery  # project cards, plus the -compact versions phones get
python tools/typing_line.py docs/typing.svg
python tools/pipeline.py docs         # the repo diagram, plus the -compact version phones get
python tools/links.py docs/links      # the link buttons (Website, CV, LinkedIn, Kaggle, Contact form)
python tools/footer.py docs           # the strip that closes the page, plus the -compact version phones get
python tools/badge_logos.py docs/logos # Astropy and pygame badge icons; prints the badge URLs to paste into the README
```

Before committing, run

```bash
python tools/check.py           # add --links to also check every link in the README (online)
```

It reruns the generators and fails if anything in `docs/` differs from their output, if a
`docs/` file is missing or unused, if the README's numbers disagree with `counts.json`, or
if an OneDrive conflict copy is present. CI runs it on every push (`check.yml`), and the
weekly workflow runs it before committing and checks the links in a separate job.

`banner.py` and `footer.py` draw the same star and orbit from `star.py`; change it
there and rerun both.

`gallery.py` reads each project's images from the local clones under
the `GitHub` folder this repo sits in and needs Pillow and numpy. The catalog and belt
numbers on the tiles are set in `tiles.py`; check them against the source repos before changing.
The sources and skills numbers are in `counts.json`, which `refresh_counts.py` rewrites from
General_Research's `sources.csv` and Hermes_Skills' README, along with the README text that quotes
them. A weekly workflow (`.github/workflows/refresh-counts.yml`) runs it and `tiles.py`, and commits
only when a count has changed.

`loc.py` counts each repo's default branch on GitHub, not the local clone, by the usual
rules: cloc's for lines, GitHub Linguist's for files.

- A line of code isn't blank and isn't only a comment; a trailing comment doesn't stop a
  line counting. Python docstrings are comments (cloc's default). Comment markers inside
  strings are not comments.
- Programming and markup languages count, including Dockerfiles and extensionless scripts
  found by their `#!` line. Data and prose (JSON, YAML, TOML, CSV, Markdown, TeX) don't.
- Files a repo's `.gitattributes` marks `linguist-generated`, `-vendored` or
  `-documentation` don't count. That is why the two classifiers count `src/` only: both mark
  their notebooks as documentation. Vendored folders, minified files and duplicate files
  (counted once) are left out too.
- What a repo generates, archives or hosts without marking it is listed in `REPOS`, with
  the reason beside each.

Hermes_Skills has no count, because many of its skills were ported from other repos. The
workflow runs `loc.py` with `--public-only`, since its token can't clone aspirecures or
SistersHopeFoundation; run it locally to refresh those two.
The arrows in `pipeline.py` follow what each repo's README says it reads from
the others; check both READMEs before adding or moving one.
