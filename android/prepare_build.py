"""Used by the Android build workflow. Copies twa-manifest.json into android/build with the icon
addresses pointed at a local copy of this repo, so the app is built from the icons in the commit
being built and not from whatever the live site serves at that moment.
Usage: python android/prepare_build.py http://127.0.0.1:8000/ [versionCode] [versionName]
"""
import json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
base = sys.argv[1]
m = json.load(open(os.path.join(here, "twa-manifest.json"), encoding="utf-8"))
swap = lambda u: u.replace("https://easymodekorea.com/", base)
m["iconUrl"] = swap(m["iconUrl"]); m["maskableIconUrl"] = swap(m["maskableIconUrl"])
for s in m["shortcuts"]: s["chosenIconUrl"] = swap(s["chosenIconUrl"])
if len(sys.argv) > 2 and sys.argv[2]: m["appVersionCode"] = int(sys.argv[2])
if len(sys.argv) > 3 and sys.argv[3]: m["appVersion"] = sys.argv[3]
os.makedirs(os.path.join(here, "build"), exist_ok=True)
json.dump(m, open(os.path.join(here, "build", "twa-manifest.json"), "w", encoding="utf-8"), indent=2)
print(f"package {m['packageId']}  version {m['appVersion']} ({m['appVersionCode']})")
