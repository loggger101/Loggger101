"""Fetch the asteroids passing Earth in the coming week, for the flyby chart (flybys.py).

Asks NASA/JPL's Small-Body Database close-approach API for every approach to Earth from
now to seven days on, within MAX_AU (20 lunar distances), nearest first. Writes "flybys"
in tools/counts.json: the window, and for each approach the designation, time (TDB),
nominal distance in au, speed relative to Earth in km/s, absolute magnitude H and, when
JPL has one, a measured diameter in km. Then writes the chart's alt text into the README;
run flybys.py afterwards to redraw it.

Stops with an error, changing nothing, if the API can't be reached or answers in a form
it doesn't expect. The weekly workflow lets this step fail without holding back the other
counts: the chart prints its window, so a week it couldn't refresh shows its own dates.

    python tools/refresh_flybys.py
"""
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / "tools" / "counts.json"
API = "https://ssd-api.jpl.nasa.gov/cad.api"
MAX_AU = 0.0514      # 20 lunar distances (1 LD = 384,400 km = 0.002570 au)
FIELDS = ["des", "cd", "dist", "v_rel", "h", "diameter"]


def fetch(today):
    query = {"date-min": today.isoformat(), "date-max": (today + dt.timedelta(days=7)).isoformat(),
             "dist-max": str(MAX_AU), "sort": "dist", "diameter": "true"}
    req = urllib.request.Request(f"{API}?{urllib.parse.urlencode(query)}",
                                 headers={"User-Agent": "loggger101 profile (github.com/loggger101)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def rows_from(answer):
    """The approaches in an answer from the API, or an error if it isn't in the form expected."""
    if "fields" not in answer and int(answer.get("count", -1)) == 0:
        return []                                       # a quiet week: the API sends no fields
    missing = [f for f in FIELDS if f not in answer.get("fields", [])]
    if missing:
        sys.exit(f"JPL's close-approach API answered without {missing}: {str(answer)[:200]}")
    at = {f: answer["fields"].index(f) for f in FIELDS}
    return [{"des": raw[at["des"]], "time": raw[at["cd"]], "dist_au": float(raw[at["dist"]]),
             "v_kms": float(raw[at["v_rel"]]), "h": float(raw[at["h"]]) if raw[at["h"]] else None,
             "diameter_km": float(raw[at["diameter"]]) if raw[at["diameter"]] else None}
            for raw in answer.get("data", [])]


def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    try:
        answer = fetch(today)
    except (OSError, ValueError) as e:
        sys.exit(f"JPL's close-approach API couldn't be read: {e}")
    rows = rows_from(answer)
    data = json.loads(COUNTS.read_text(encoding="utf-8"))
    data["flybys"] = {"from": today.isoformat(), "to": (today + dt.timedelta(days=7)).isoformat(),
                      "source": "NASA/JPL SBDB Close Approach Data API", "rows": rows}
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    import flybys       # reads the counts just written
    readme_path = ROOT / "README.md"
    readme_path.write_text(flybys.update_readme(readme_path.read_text(encoding="utf-8")),
                           encoding="utf-8", newline="\n")
    print(f"{len(rows)} approaches within {MAX_AU} au, {today} to {today + dt.timedelta(days=7)}")


if __name__ == "__main__":
    main()
