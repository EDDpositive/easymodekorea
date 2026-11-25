"""Sets the daily price game's first day to fit the day it is published. Run on the branch just before the merge, then commit:

    python tools/won_publish_day.py 2026-11-28

Give the Korean date of the publication; it becomes day 1. Also writes the decision days into docs/won-game.md and rebuilds. Without this step nothing breaks: a later
publication only means that a few earlier days can already be played. It refuses once the game stands on main.
"""
import datetime, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def sub(rel, pat, new):
    p = os.path.join(ROOT, rel); s = open(p, encoding="utf-8", newline="").read()
    s, n = re.subn(pat, new, s)
    if n != 1: raise SystemExit(f"{rel}: {pat} found {n} times")
    open(p, "w", encoding="utf-8", newline="").write(s)


def main():
    if subprocess.run(["git", "cat-file", "-e", "origin/main:won/index.html"], cwd=ROOT, capture_output=True).returncode == 0:
        raise SystemExit("already on main: readers' records are kept by day number, so day 1 must not move any more")
    d = datetime.date.fromisoformat(sys.argv[1]); day = lambda n: (d + datetime.timedelta(n)).isoformat()
    sub("src/won.py", r'(?m)^START = "[\d-]+"', f'START = "{d}"')
    sub("docs/won-game.md", r"공개일: \*\*[^*]+\*\*.*", f"공개일: **{d}**. 14일째 {day(14)}, 28일째 {day(28)}(보는 한 주: {day(22)} ~ {day(28)}).")
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "build.py")], check=True, cwd=ROOT)
    print("day 1 =", d, "| check", day(14), "| decide", day(28))


if __name__ == "__main__":
    main()
