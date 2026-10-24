"""Count my commits to each repo the profile lists, week by week, for the activity panel
(activity.py draws it from what this writes).

Reads each repo's default branch on GitHub through a commit-only clone (no trees or files,
so even General_Research comes down in seconds) and deletes it. A commit counts if its
author's name or email holds "loggger101"; every name and address I commit under does,
and the bots (the website's deploy workflow, General_Research's cron) don't. Weeks start
on Monday and are dated by the commit's author date.

Writes "activity" in tools/counts.json: the date it ran, and for each repo the date of my
first and last commits, my commits in every week between, by the week's Monday, and, for
a public repo, my last RECENT commits other than merges (hash, date, subject line) for the
README's list of latest commits. A private repo's commit messages are never kept. Then
writes the activity panel's alt text and that list into the README; run activity.py
afterwards to redraw the panel. The private repos (aspirecures, SistersHopeFoundation) need your own GitHub
login to clone; with --public-only, which the weekly workflow uses, they keep what is
stored.

    python tools/refresh_activity.py                 # every repo
    python tools/refresh_activity.py --public-only   # skip the private ones
"""
import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from loc import REPOS

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / "tools" / "counts.json"
# Every repo with a row in the README: loc.py's, plus Hermes_Skills, which has no line count
# but is still my work.
ACTIVITY_REPOS = {name: private for name, (_, private, _) in REPOS.items()} | {"Hermes_Skills": False}
AUTHOR = "loggger101"
RECENT = 3      # latest commits kept from each public repo


def monday(day):
    return day - dt.timedelta(days=day.weekday())


def repo_activity(name, private):
    with tempfile.TemporaryDirectory() as tmp:
        url = f"https://github.com/loggger101/{name}.git"
        subprocess.run(["git", "clone", "--quiet", "--bare", "--filter=tree:0", url, "r"],
                       cwd=tmp, check=True, capture_output=True)
        # --author matches the name or the email.
        log = lambda *a: subprocess.run(["git", "-C", "r", "log", f"--author={AUTHOR}", "--date=short", *a, "HEAD"],
                                        cwd=tmp, check=True, capture_output=True, text=True, encoding="utf-8").stdout
        dates = log("--format=%ad").split()
        recent = [] if private else [line.split("\t", 2) for line in log("--no-merges", f"-n{RECENT}", "--format=%H%x09%ad%x09%s").splitlines()]
    days = [dt.date.fromisoformat(d) for d in dates]
    if not days:
        sys.exit(f"{name}: no commits by {AUTHOR}; has the author check stopped matching?")
    weeks = {}
    for day in days:
        key = monday(day).isoformat()
        weeks[key] = weeks.get(key, 0) + 1
    out = {"first": min(days).isoformat(), "last": max(days).isoformat(), "weeks": dict(sorted(weeks.items()))}
    if recent:
        out["recent"] = recent
    return out


def main():
    public_only = "--public-only" in sys.argv[1:]
    today = dt.datetime.now(dt.timezone.utc).date()
    data = json.loads(COUNTS.read_text(encoding="utf-8"))
    stored = data.get("activity", {}).get("repos", {})
    repos = {}
    for name, private in ACTIVITY_REPOS.items():
        if private and public_only:
            if name not in stored:
                sys.exit(f"{name} is private and has no stored activity; run without --public-only once")
            repos[name] = stored[name]
            continue
        repos[name] = repo_activity(name, private)
        print(f"{sum(repos[name]['weeks'].values()):>6,} commits, last {repos[name]['last']}  {name}")
    data["activity"] = {"as_of": today.isoformat(), "repos": repos}
    COUNTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    import activity     # reads the counts just written
    readme_path = ROOT / "README.md"
    readme_path.write_text(activity.update_readme(readme_path.read_text(encoding="utf-8")),
                           encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
