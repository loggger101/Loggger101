# Image generators

The banner, typing line, link buttons, stat tiles, repo diagram, gallery cards and footer in `docs/` are generated, not hand-edited.
Run from the repo root:

```bash
python tools/banner.py docs/banner.svg
python tools/refresh_counts.py         # pull the sources and skills counts from their repos
python tools/tiles.py docs/stats      # full tiles plus the -compact versions phones get
python tools/gallery.py docs/gallery  # project cards, plus the -compact versions phones get
python tools/typing_line.py docs/typing.svg
python tools/pipeline.py docs         # the repo diagram, plus the -compact version phones get
python tools/links.py docs/links      # the link buttons (Website, CV, LinkedIn, Kaggle, Contact form)
python tools/footer.py docs           # the strip that closes the page, plus the -compact version phones get
```

`banner.py` and `footer.py` draw the same star and orbit from `star.py`; change it
there and rerun both.

`gallery.py` reads each project's images from the local clones under
`C:\Users\Loggg\OneDrive\Documents\GitHub` and needs Pillow and numpy. The catalog and belt
numbers on the tiles are set in `tiles.py`; check them against the source repos before changing.
The sources and skills numbers are in `counts.json`, which `refresh_counts.py` rewrites from
General_Research's `sources.csv` and Hermes_Skills' README, along with the README text that quotes
them. A weekly workflow (`.github/workflows/refresh-counts.yml`) runs it and `tiles.py`, and commits
only when a count has changed.
The arrows in `pipeline.py` follow what each repo's README says it reads from
the others; check both READMEs before adding or moving one.
