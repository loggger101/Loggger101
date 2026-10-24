# Image generators

The banner, typing line, link buttons, stat tiles, repo diagram, gallery cards, activity and languages panels and footer in `docs/` are generated, not hand-edited.
Run from the repo root:

```bash
python tools/banner.py docs/banner.svg
python tools/refresh_counts.py         # pull the sources and skills counts from their repos
python tools/loc.py                    # lines of code and total lines under each repo's name, and by language (--public-only skips the private two)
python tools/refresh_activity.py       # every commit of mine to each repo, by week, for the activity panel (--public-only as above)
python tools/tiles.py docs/stats      # full tiles plus the -compact versions phones get
python tools/gallery.py docs/gallery  # project cards (two animated), plus the -compact versions phones get
python tools/typing_line.py docs/typing.svg
python tools/pipeline.py docs         # the repo diagram, plus the -compact version phones get
python tools/activity.py docs         # every commit so far as orbits, plus the -compact version phones get
python tools/languages.py docs        # lines of code by language, plus the -compact version phones get
python tools/links.py docs/links      # the link buttons (Website, CV, LinkedIn, Kaggle, Contact form)
python tools/footer.py docs           # the strip that closes the page, plus the -compact version phones get
python tools/badge_logos.py docs/logos # Astropy and pygame badge icons; prints the badge URLs to paste into the README
python tools/icons.py docs/icons       # the icons beside the section headings
```

Before committing, run

```bash
python tools/check.py           # add --links to also check every link in the README (online)
```

It reruns the generators and fails if anything in `docs/` differs from their output, if a
`docs/` file is missing or unused, if the README's numbers disagree with `counts.json`, or
if an OneDrive conflict copy is present. CI runs it on every push (`check.yml`), and the
weekly workflow runs it before committing and checks the links in a separate job.

The banner, footer, tiles, repo diagram and both panels move, with CSS animations in each
SVG: stars twinkle everywhere; points of light run along the diagram's data arrows and its
citation dashes creep; the activity panel's dots come in round the orbit in time order;
and the bars grow in. Each SVG stops it all under `prefers-reduced-motion`, and every
animation's resting state is the finished picture, so a still render (reduced motion, a
thumbnail) shows everything. Anything that shows only while moving, like the banner's
shooting star or the diagram's points of light, is hidden when still.

`links.py` and `icons.py` draw their glyphs from `glyphs.py`.

`banner.py` and `footer.py` draw the same star and orbit from `star.py`; change it
there and rerun both.

`gallery.py` reads each project's images from the local clones under
the `GitHub` folder this repo sits in and needs Pillow and numpy. The satellite and drone
cards also come animated (`-motion.webp`, listed in `MOTION`): the drone card is five
seconds of the website's demo video, cut with ffmpeg, and the satellite card is one ISS
orbit recorded from the simulator itself by `sim_clip.py`, which needs the simulator's
clone and pygame. The README shows them to everyone but those who ask for reduced motion,
who get the still card through a `<picture>` source. A full run takes about nine minutes,
nearly all of it WebP compressing the animations. The catalog and belt
numbers on the tiles are set in `tiles.py`; check them against the source repos before changing.
The sources and skills numbers are in `counts.json`, which `refresh_counts.py` rewrites from
General_Research's `sources.csv` and Hermes_Skills' README, along with the README text that quotes
them. A weekly workflow (`.github/workflows/refresh-counts.yml`) runs it and `tiles.py`, along
with `loc.py`, `refresh_activity.py` and the two panels, and commits whatever changed.

`activity.py` and `languages.py` draw only from `counts.json`, so `check.py` can rerun them
offline. Each also has an `update_readme()` that writes its panel's numbers into the
README's alt text, which `refresh_activity.py` and `loc.py` call after a refresh and
`check.py` checks, so a screen reader hears what the image shows. `refresh_activity.py` counts the commits whose author name or email holds
`loggger101`, which leaves out the bots (the website's deploy workflow, General_Research's
cron), from a commit-only clone of each repo. The panel's rings follow `SECTIONS` in
`activity.py`; a repo added to the README goes there too, or `activity.py` stops with an
error. The orbit runs from my first commit to the week `refresh_activity.py` last ran, so
the weekly workflow commits a new panel every Monday. Past 60 weeks a dot takes in several
weeks (`MAX_DOTS`), so the rings stay readable as the history grows.

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

The "total lines" under each count are every line of every text file of the repo owner's own:
code with its blank and comment lines, notebooks (all cells, no outputs), docs, the paper's
TeX, data, config and logs. Binary files don't count, nor does anything lines of code leave
out for being built, archived, hosted or vendored (notebooks marked documentation do count).
`TOTAL_EXCLUDE` in `loc.py` lists the rest that's left out, with the reason beside each:
other people's text (licences, a downloaded SDSS table, the AAS LaTeX template, fetched
paper abstracts) and machine output (ArcGIS metadata, generated sitemaps and feeds, lock files).

Hermes_Skills has no count, because many of its skills were ported from other repos. The
workflow runs `loc.py` with `--public-only`, since its token can't clone aspirecures or
SistersHopeFoundation; run it locally to refresh those two.
The arrows in `pipeline.py` follow what each repo's README says it reads from
the others; check both READMEs before adding or moving one.
