# How the profile is made

Apart from a one-pixel spacer, nothing in `docs/` is drawn by hand. Each picture on the
profile comes from a script in this folder, most of them from data the scripts fetch from
the repos themselves, and a weekly workflow (`.github/workflows/refresh-counts.yml`,
Mondays) fetches it again and redraws them.

| on the profile | drawn by | from | refreshed |
|---|---|---|---|
| banner, typing line, footer, link buttons, section icons | `banner.py`, `typing_line.py`, `footer.py`, `links.py`, `icons.py` | the scripts alone | when changed |
| stat tiles | `tiles.py` | General_Research's `sources.csv` and Hermes_Skills' README (`refresh_counts.py`); the catalog and belt numbers are set in `tiles.py` | weekly |
| gallery cards | `gallery.py`, `sim_clip.py` | the project clones: screenshots, figures, map layouts, a demo video and the simulator running | by hand |
| repo diagram | `pipeline.py` | the repos' READMEs, read by hand | when a link changes |
| line counts under each repo, the languages panel | `loc.py`, `languages.py` | each repo's default branch | weekly; the two private repos by hand |
| sparklines, the activity panel, the latest commits | `refresh_activity.py`, `sparks.py`, `activity.py` | each repo's commit history | weekly; the two private repos by hand |
| break-even chart | `refresh_counts.py`, `breakeven.py` | the destinations table in economicspace's README | weekly |
| flyby chart | `refresh_flybys.py`, `flybys.py` | NASA/JPL's close-approach API | weekly |

Run from the repo root. Fetch the data first (each writes `counts.json` and the README's
alt text):

```bash
python tools/refresh_counts.py         # research sources, agent skills, economicspace's destinations
python tools/loc.py                    # lines of code and total lines per repo, and by language (--public-only skips the private two)
python tools/refresh_activity.py       # every commit of mine to each repo, by week, and the latest few (--public-only as above)
python tools/refresh_flybys.py         # NASA/JPL's close approaches to Earth for the week ahead
```

then draw:

```bash
python tools/tiles.py docs/stats       # stat tiles, plus the -compact versions phones get
python tools/pipeline.py docs          # the repo diagram, plus -compact
python tools/breakeven.py docs         # economicspace's cost per dollar earned for each destination, plus -compact
python tools/activity.py docs          # every commit so far as orbits, plus -compact
python tools/sparks.py docs/sparks     # the commits-per-week line under each repo's name
python tools/languages.py docs         # lines of code by language, plus -compact
python tools/flybys.py docs            # the week's close approaches, plus -compact
python tools/gallery.py docs/gallery   # project cards (three animated), plus -compact; name cards (mars drone) to make only those
python tools/banner.py docs/banner.svg
python tools/typing_line.py docs/typing.svg
python tools/footer.py docs            # the strip that closes the page, plus -compact
python tools/links.py docs/links       # the link buttons (Website, CV, LinkedIn, Kaggle, Contact form)
python tools/icons.py docs/icons       # the icons beside the section headings
python tools/badge_logos.py docs/logos # Astropy and pygame badge icons; prints the badge URLs to paste into the README
```

Before committing, run

```bash
python tools/check.py           # add --links to also check every link in the README (online)
python tools/test_loc.py        # loc.py's counting rules
python tools/test_tools.py      # the economicspace and JPL readers, commit subjects, anchors, the panel frame
```

`check.py` reruns the generators and fails if anything in `docs/` differs from their output,
if a `docs/` file is missing or unused, if the README's numbers or alt text disagree with
`counts.json`, if a section link names no heading, or if an OneDrive conflict copy is
present. CI runs all three on every push (`check.yml`), and the weekly workflow runs
`check.py` before committing and checks the links in a separate job.

The wide panels (activity, languages, break-even, flybys, repo diagram) open with
`panel.background` from `panel.py`: the frame, the stars and the reduced-motion rule, which
stops every class a panel names as animated. Change the frame there.

The banner, footer, tiles, repo diagram and the panels move, with CSS animations in each
SVG: stars twinkle everywhere; the tiles' numbers roll up like an odometer; points of light
run along the diagram's data arrows and its citation dashes creep; the activity panel's
dots come in round the orbit in time order; and the bars grow in. The odometer places each
character itself, using Segoe UI Bold's widths (`ADVANCE` in `tiles.py`), since CI has no
fonts to measure with. Each SVG stops it all under `prefers-reduced-motion`, and every
animation's resting state is the finished picture, so a still render (reduced motion, a
thumbnail) shows everything. Anything that shows only while moving, like the banner's
shooting star or the diagram's points of light, is hidden when still.

`links.py` and `icons.py` draw their glyphs from `glyphs.py`.

`banner.py` and `footer.py` draw the same star and orbit from `star.py`; change it
there and rerun both.

`gallery.py` reads each project's images from the local clones under
the `GitHub` folder this repo sits in and needs Pillow and numpy. The satellite, Mars and
drone cards also come animated (`-motion.webp`, listed in `MOTION`):
- satellite: one ISS orbit recorded from the simulator itself by `sim_clip.py`, which
  needs the simulator's clone and pygame;
- Mars: Ius Chasma's three type-area layouts (visible, night IR, Iso Cluster classes),
  which share one map frame, crossfading into the still card's ±60° landform map;
- drone: five seconds of the website's demo video, cut with ffmpeg.

The README shows them to everyone but those who ask for reduced motion, who get the still
card through a `<picture>` source. A full run takes about twelve minutes, nearly all of it
WebP compressing the animations; name cards after the output folder to make only those.

The catalog and belt numbers on the tiles are set in `tiles.py`; check them against the
source repos before changing.
The sources and skills numbers are in `counts.json`, which `refresh_counts.py` rewrites from
General_Research's `sources.csv` and Hermes_Skills' README, along with the README text that quotes
them. A weekly workflow (`.github/workflows/refresh-counts.yml`) runs it and `tiles.py`, along
with `loc.py`, `refresh_activity.py` and the two panels, and commits whatever changed.

`breakeven.py` draws the destinations table in economicspace's README (its latest
full-catalog run for each place the pipeline delivers to), which `refresh_counts.py` reads
into `counts.json`, keeping the winning asteroid but not its vehicle. If that table changes
shape, `refresh_counts.py` stops with an error instead of publishing a half-read chart.

`flybys.py` draws the asteroids passing Earth within 20 lunar distances in the week after
`refresh_flybys.py` last ran, from JPL's close-approach API. Sizes come from H at albedos
0.25 to 0.05 unless JPL has a measured diameter. The API is the one outside source the
weekly workflow can't vouch for, so that step may fail without stopping the others; the
chart prints its week, so a stale one is plainly dated.

`activity.py` and `languages.py` draw only from `counts.json`, so `check.py` can rerun them
offline. Each also has an `update_readme()` that writes its panel's numbers into the
README's alt text, which `refresh_activity.py` and `loc.py` call after a refresh and
`check.py` checks, so a screen reader hears what the image shows. `activity.py`'s also
writes the list of my latest commits under the panel, between the `latest commits`
markers: the newest six across the public repos, two at most from any one, merges left
out. Private repos' commit messages are never fetched into `counts.json`.

`refresh_activity.py` counts the commits whose author name or email holds
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
