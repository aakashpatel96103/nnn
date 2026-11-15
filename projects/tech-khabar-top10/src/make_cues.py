"""Build src/cues.json from src/words.json + the scene map (same math the HTML uses)."""
import json, re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
words = json.loads((P / "src" / "words.json").read_text())
FPS = 30
DUR = json.loads((P / "project.json").read_text())["duration"]

lines = sorted({w["line"] for w in words})
SC = [next(w["s"] for w in words if w["line"] == i) for i in lines]
SC[0] = 0.0

def wt(i, rx, frac=.45):
    for w in [x for x in words if x["line"] == i]:
        if re.search(rx, re.sub(r"[^\w.$%]", "", w["w"])):
            return w["s"]
    nxt = SC[i + 1] if i + 1 < len(SC) else DUR
    return SC[i] + frac * (nxt - SC[i])

cues = []
def add(t, sound, gain, label):
    cues.append({"frame": int(round(t * FPS)), "sound": sound, "gain": gain, "label": label})

add(0.0, "curated/hook-impact.wav", -6, "opening frame")
add(0.35, "curated/ui-pop.wav", -4, "intro card lands")
for i in range(2, 12):
    add(SC[i] + .28, "curated/ui-pop.wav", -4, f"item {i-1:02d} number stamp")
add(wt(2, r"400"), "sub-impact.wav", -9, "Apple $400 premium")
add(wt(3, r"212"), "thock.wav", -7, "GTA6 212 GB")
add(wt(3, r"212") + .55, "tick.wav", -12, "storage bar fills")
add(wt(4, r"3"), "tick.wav", -13, "AMD 3 Nov")
add(wt(5, r"rok|bada", .26), "latch.wav", -6, "BLOCKED stamp")
add(wt(6, r"2027"), "thock.wav", -9, "Jan 2027 date")
add(wt(7, r"139"), "sub-impact.wav", -8, "$139M fraud figure")
add(wt(8, r"37"), "sub-impact.wav", -9, "37M records")
add(wt(8, r"37") + .6, "tick.wav", -12, "safe badge")
add(wt(9, r"50"), "tick.wav", -12, "~50 participants")
add(wt(10, r"Carbon|10", .4), "thock.wav", -11, "Gemini 4 Carbon")
add(wt(11, r"30"), "curated/ui-pop.wav", -8, "+30% speed bars")
add(SC[12] + .15, "curated/ui-pop.wav", -4, "recap card")
add(SC[13] - .36, "curated/zoom-swish.wav", -4, "halftone wipe into outro")
add(SC[13] + .55, "clean-ding.wav", -5, "subscribe end card")
add(wt(13, r"GTA", .18), "curated/ui-pop.wav", -5, "comment GTA sticker")

cues = sorted(cues, key=lambda c: c["frame"])
(P / "src" / "cues.json").write_text(json.dumps({"fps": FPS, "total": DUR, "cues": cues}, indent=1))
print(f"{len(cues)} cues, last at frame {cues[-1]['frame']}")
