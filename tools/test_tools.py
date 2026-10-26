"""Tests for the parts of the tools that read other people's formats or write the README's
text: the economicspace and JPL readers, the commit-subject cleaner, the heading-anchor
rule, the break-even verdict, the flyby sizes and alt text, and the shared panel frame. One small sample per rule, with what it
should give. Offline; CI runs it on every push (.github/workflows/check.yml).

    python tools/test_tools.py
"""
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
sys.stdout.reconfigure(encoding="utf-8")   # the sizes print an en dash


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fails = 0


def eq(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got!r}, want {want!r}")


def stops(name, f, *args):
    """f(*args) must stop with an error (sys.exit), as the readers do on a format they don't know."""
    global fails
    try:
        f(*args)
    except SystemExit:
        print(f"ok   {name}: stops")
        return
    fails += 1
    print(f"FAIL {name}: went on")


# economicspace's destinations table (refresh_counts.py).
rc = load("refresh_counts")
TABLE = """#### Every destination at this release: Mars surface is now the best case

Some words.

| destination | cost / revenue | winner | median body |
|---|---|---|---|
| **`mars_surface`** | **1.0914x** | 2015 DS (X), Falcon Heavy (expendable) on iodine, aerocaptured, 2 missions | **2.0246x** |
| `lunar_surface` | 2.9353x‡ | 2005 QP87 (X), Falcon Heavy (expendable) on iodine | 8.2537x |
| `mars_orbit` | 4.5908x | 350751 (B), New Glenn on iodine | 13.9410x |
| `cislunar` | 4.8379x | 2018 DT (M), above | 20.9073x |
| `earth_surface` | 6,154.06x† | 2018 DT (M), Falcon Heavy (expendable) on iodine | 24,301.21x |

† A footnote.
"""
rows = rc.destinations(TABLE)
eq("table rows", len(rows), 5)
eq("bold and code marks dropped", rows[0]["dest"], "mars_surface")
eq("bold number", rows[0]["best"], 1.0914)
eq("footnote sign and thousands", rows[4]["best"], 6154.06)
eq("winner without the vehicle", rows[0]["winner"], "2015 DS (X)")
eq("numbered asteroid", rows[2]["winner"], "350751 (B)")
eq("'above' for a vehicle", rows[3]["winner"], "2018 DT (M)")
stops("heading renamed", rc.destinations, TABLE.replace("#### Every destination at this release", "#### Destinations"))
stops("column dropped", rc.destinations, TABLE.replace("| destination | cost / revenue | winner | median body |",
                                                       "| destination | cost / revenue | median body |"))
stops("winner without a class", rc.destinations, TABLE.replace("2015 DS (X), Falcon", "2015 DS, Falcon"))
stops("too few rows", rc.destinations, "\n".join(l for l in TABLE.splitlines() if "x |" not in l or "mars_surface" in l))

# The catalog's size, written the same way everywhere (refresh_counts.py).
eq("millions rounds", rc.millions(1575889), "1.58")
eq("millions keeps two places", rc.millions(1568878), "1.57")
PROSE = ('<img src="docs/stats/catalog.svg" width="23.5%" alt="1.57M asteroids cataloged (AsteroidCatalog)"> '
         "I built a catalog of about 1.57 million of them. About 1.57 million asteroids from JPL SBDB, "
         'alt="602 research sources (General_Research)" alt="253 agent skills (Hermes_Skills)" '
         "My library of 253 agent skills in 23 categories")
out = rc.update_readme(PROSE, {"sources": 605, "skills": 253, "skill_categories": 23, "catalog_rows": 1575889})
eq("catalog size rewritten in three places", out.count("1.58"), 3)
eq("nothing left at the old size", "1.57" in out, False)
stops("a sentence gone missing", rc.update_readme, PROSE.replace("I built a catalog", "I made a catalog"),
      {"sources": 605, "skills": 253, "skill_categories": 23, "catalog_rows": 1575889})

# JPL's close-approach answers (refresh_flybys.py).
rf = load("refresh_flybys")
ANSWER = {"count": "1", "fields": ["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf",
                                   "t_sigma_f", "h", "diameter", "diameter_sigma"],
          "data": [["2026 TB94", "3", "2461340.5", "2026-Oct-27 01:10", "0.0130929688951845", "0.0129", "0.0132",
                    "11.6119243205877", "11.59", "00:03", "25.616", None, None]]}
got = rf.rows_from(ANSWER)
eq("approach read", (got[0]["des"], got[0]["time"], round(got[0]["dist_au"], 6), round(got[0]["v_kms"], 2), got[0]["h"]),
   ("2026 TB94", "2026-Oct-27 01:10", 0.013093, 11.61, 25.616))
eq("no diameter", got[0]["diameter_km"], None)
eq("quiet week", rf.rows_from({"signature": {}, "count": 0}), [])
stops("field missing", rf.rows_from, ANSWER | {"fields": [f for f in ANSWER["fields"] if f != "v_rel"]})

# Flyby sizes (flybys.py): H at albedos 0.25 to 0.05, or a measured diameter.
fb = load("flybys")
lo, hi = fb.size_m({"h": 25.616, "diameter_km": None})
eq("size from H", (round(lo), round(hi)), (20, 45))
eq("size text", fb.size_text({"h": 25.616, "diameter_km": None}), "20–45 m")
eq("measured diameter", fb.size_text({"h": 18.0, "diameter_km": 1.2}), "1.2 km")
eq("no H", fb.size_text({"h": None, "diameter_km": None}), "size unknown")

# The flyby chart's alt text says what the chart does, including the rows it leaves off.
ROW = {"des": "2026 TB94", "time": "2026-Oct-27 01:10", "dist_au": 0.0130929688951845, "v_kms": 11.6119243205877,
       "h": 25.616, "diameter_km": None}
eq("alt names a row", "2026 TB94, 5.1 lunar distances on Tue 27 Oct, 20–45 m, 11.6 km/s." in fb.alt_text([ROW]), True)
eq("alt counts the rows left off", fb.alt_text([ROW] * (fb.MAX_ROWS + 2)).endswith("; and 2 more farther out."), True)
eq("alt leaves nothing off", "farther out" in fb.alt_text([ROW] * fb.MAX_ROWS), False)
eq("alt for a quiet week", fb.alt_text([]).endswith("none this week."), True)

# The break-even verdict (breakeven.py) follows the numbers, so the chart, its alt text and
# the README's sentence can't say none breaks even once one does.
be = load("breakeven")
NONE = [{"dest": "mars_surface", "best": 1.09}, {"dest": "leo", "best": 17.0}]
ONE = [{"dest": "leo", "best": 17.0}, {"dest": "mars_surface", "best": 0.92}]
TWO = ONE + [{"dest": "lunar_surface", "best": 0.98}]
eq("none yet", (be.verdict(NONE), be.clause(NONE)), ("No destination breaks even yet.", "none does yet"))
eq("one pays", (be.verdict(ONE), be.short_verdict(ONE), be.clause(ONE)),
   ("The best mission to the surface of Mars breaks even.", "1 destination breaks even.",
    "the best mission to the surface of Mars does"))
eq("two pay, best first", (be.verdict(TWO), be.short_verdict(TWO)),
   ("The best missions to the surface of Mars and the Moon's surface break even.", "2 destinations break even."))
profile = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
eq("README sentence follows", "pays for itself; none does yet." in be.update_readme(profile), True)
stops("README sentence gone", be.update_readme, profile.replace("Left of the dashed line", "Left of the line"))

# Commit subjects for the latest-commits list (activity.py).
ac = load("activity")
eq("bookkeeping dropped", ac.subject("The final started: the drive merged (KB §69, §69.1) (#2)"),
   "The final started: the drive merged")
eq("markdown escaped", ac.subject("keeps elements_to_state and [x] *y*"), r"keeps elements\_to\_state and \[x\] \*y\*")
eq("html escaped", ac.subject("a <b> & c"), "a &lt;b&gt; &amp; c")
eq("cut at a word", ac.subject("word " * 30, limit=20), "word word word word…")

# Heading anchors (check.py), checked against the anchors GitHub gave the live profile.
ck = load("check")
eq("icon heading", ck.anchor('<picture><img src="docs/icons/x.svg" alt=""></picture> Space economics'), "-space-economics")
eq("hyphen kept", ck.anchor('<picture><img src="x" alt=""></picture> Rare-disease work'), "-rare-disease-work")
eq("plain heading", ck.anchor("Image generators"), "image-generators")

# Freshness (check.py --fresh): a missed week is flagged, a normal Monday isn't.
data = json.loads((TOOLS / "counts.json").read_text(encoding="utf-8"))
oldest = min(dt.date.fromisoformat(data["flybys"]["from"]), dt.date.fromisoformat(data["activity"]["as_of"]))
ck.problems.clear()
ck.check_fresh(today=oldest + dt.timedelta(days=7))
eq("a week on: fresh", ck.problems, [])
ck.problems.clear()
ck.check_fresh(today=oldest + dt.timedelta(days=15))
eq("two weeks on: both flagged", len(ck.problems), 2)
ck.problems.clear()

# Quoted figures (check.py FACTS): the README holds each phrase; a source that drops its
# figure, or can't be read, is reported.
readme = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
ck.problems.clear()
ck.check_fact_phrases(readme)
eq("every quoted phrase in the README", ck.problems, [])
ck.problems.clear()
ck.check_fact_phrases(readme.replace("87.1% on fine class", "87.6% on fine class"))
eq("a reworded figure flagged", len(ck.problems), 1)
everything = " ".join(b for _, _, b in ck.FACTS)
ck.problems.clear()
ck.check_facts(fetch=lambda repo: everything)
eq("sources that still say it", ck.problems, [])
ck.problems.clear()
ck.check_facts(fetch=lambda repo: everything.replace("84.30%", "85.10%"))
eq("a source whose result changed", len(ck.problems), 1)


def unreachable(repo):
    raise OSError("no network")


ck.problems.clear()
ck.check_facts(fetch=unreachable)
eq("an unreadable source, once per repo", len(ck.problems), len({r for _, r, _ in ck.FACTS}))
ck.problems.clear()

# The shared frame (panel.py): every animated class is stopped under reduced motion.
pn = load("panel")
svg = pn.background(400, 300, 1, 'a "quoted" alt', rules=pn.FADE, animated=("fade", "spin"))
eq("reduced motion stops all", "{ .tw, .fade, .spin { animation: none; } }" in svg, True)
eq("alt escaped", 'aria-label="a &quot;quoted&quot; alt"' in svg, True)
eq("one-line defs without extras", "<defs><linearGradient" in svg, True)
eq("same seed, same stars", pn.background(400, 300, 1, "x") == pn.background(400, 300, 1, "x"), True)
# No star on a word or a mark; the rest stay put. A word in a clipped group counts only as its clip.
svg = ('<circle cx="30.0" cy="20.0" r="1.0" fill="#fff" opacity="0.5"/>'
       '<circle class="tw" cx="300.0" cy="200.0" r="1.2" fill="#dbe7ff"/>'
       '<circle cx="200.0" cy="20.0" r="0.6" fill="#fff" opacity="0.5"/>'
       '<circle cx="380.0" cy="100.0" r="0.6" fill="#fff" opacity="0.5"/>'
       '<g font-size="20"><text x="20" y="25">a word</text></g>'
       '<line x1="250" y1="200" x2="350" y2="200"/>'
       '<g clip-path="url(#w)"><text x="190" y="-20" font-size="40">9</text></g>'
       '<circle cx="380" cy="104" r="1"/>')
kept = pn.keep_clear(svg)
eq("stars on a word and a line go", ('cx="30.0"' in kept, 'cx="300.0"' in kept), (False, False))
eq("a star clear of all stays", 'cx="200.0"' in kept, True)
eq("a star by a dot goes", 'cx="380.0"' in kept, False)

sys.exit(f"{fails} failed" if fails else 0)
