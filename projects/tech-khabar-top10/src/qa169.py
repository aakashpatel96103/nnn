"""Layout + file QA for this 1920x1080 project (engine/qa.py checks the 1080x1920 reel frame).

  python src/qa169.py <project> [--video export/x.mp4]

DOM pass (every 1 s): every visible text block / card / sticker sits inside the frame, the headline
never overlaps the stat card, captions stay one line inside 1560x170. Video pass: ffprobe
resolution/fps/duration, ebur128 loudness + true peak, black-frame and frozen-frame scans.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine"))
import render as R
from playwright.sync_api import sync_playwright

W, H = 1920, 1080
proj = Path(sys.argv[1]).resolve()
cfg = json.loads((proj / "project.json").read_text())
DUR, FPS = float(cfg["duration"]), float(cfg.get("fps", 30))
page = R.build(proj)
issues = []

JS = """() => {
  const out = [];
  const vis = el => { const s = getComputedStyle(el); return s.opacity > 0.05 && s.display !== 'none'
     && el.getBoundingClientRect().width > 1; };
  document.querySelectorAll('[data-qa-text], .card, #capin, #chip, .stk').forEach(el => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    out.push({id: el.id || el.className, cls: el.className, l: r.left, t: r.top, r: r.right, b: r.bottom});
  });
  const cap = document.getElementById('capin'), cw = cap.getBoundingClientRect();
  return {boxes: out, cap: {w: cw.width, h: cw.height, l: cw.left, r: cw.right, t: cw.top, b: cw.bottom},
          capOp: getComputedStyle(cap).opacity};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(page.as_uri())
    pg.wait_for_timeout(700)
    t = 0.0
    while t <= DUR:
        pg.evaluate(f"render({t})")
        d = pg.evaluate(JS)
        for bx in d["boxes"]:
            if bx["l"] < -1 or bx["t"] < -1 or bx["r"] > W + 1 or bx["b"] > H + 1:
                issues.append(["FAIL", f"outside frame: {bx['id']} {bx['l']:.0f},{bx['t']:.0f},{bx['r']:.0f},{bx['b']:.0f}", t])
        heads = [x for x in d["boxes"] if x["id"].startswith("h")]
        cards = [x for x in d["boxes"] if "card" in x["cls"]]
        for h in heads:
            for c in cards:
                if h["r"] > c["l"] + 2 and h["l"] < c["r"] and h["b"] > c["t"] + 2 and h["t"] < c["b"]:
                    issues.append(["FAIL", f"headline overlaps card ({h['id']} x {c['id']})", t])
        cap = d["cap"]
        if float(d["capOp"]) > .5:
            if cap["w"] > 1560 or cap["h"] > 170:
                issues.append(["FAIL", f"caption too big {cap['w']:.0f}x{cap['h']:.0f}", t])
            if cap["l"] < 60 or cap["r"] > W - 60 or cap["b"] > H - 80:
                issues.append(["FAIL", f"caption outside safe area {cap['l']:.0f}-{cap['r']:.0f} b{cap['b']:.0f}", t])
        t = round(t + 1.0, 2)
    if errs:
        issues.append(["FAIL", "page errors: " + "; ".join(errs[:3]), 0])
    b.close()

if "--video" in sys.argv:
    v = Path(sys.argv[sys.argv.index("--video") + 1]).resolve()
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(v)],
                                      capture_output=True, text=True).stdout)
    st = next(s for s in probe["streams"] if s["codec_type"] == "video")
    if (st["width"], st["height"]) != (1920, 1080):
        issues.append(["FAIL", f"resolution {st['width']}x{st['height']} (need 1920x1080)", 0])
    num, den = map(int, st["r_frame_rate"].split("/"))
    if abs(num / den - FPS) > .5:
        issues.append(["WARN", f"fps {num/den:.2f}", 0])
    dur = float(probe["format"]["duration"])
    if abs(dur - DUR) > .6:
        issues.append(["FAIL", f"duration {dur:.2f}s vs {DUR}s", 0])
    if not any(s["codec_type"] == "audio" for s in probe["streams"]):
        issues.append(["WARN", "no audio stream", 0])
    eb = subprocess.run(["ffmpeg", "-v", "info", "-i", str(v), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)
    if m: print(f"INFO loudness {float(m[-1]):.1f} LUFS")
    if tp: print(f"INFO true peak {float(tp[-1]):.1f} dBTP")
    if m and abs(float(m[-1]) + 14) > 1.5:
        issues.append(["WARN", f"loudness {float(m[-1]):.1f} LUFS (target -14)", 0])
    bf = subprocess.run(["ffmpeg", "-v", "info", "-i", str(v), "-vf", "blackdetect=d=0.25:pix_th=0.10", "-an", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    if bf.count("black_start"): issues.append(["WARN", f"{bf.count('black_start')} black segment(s)", 0])
    fr = subprocess.run(["ffmpeg", "-v", "info", "-i", str(v), "-vf", "freezedetect=n=0.001:d=1.2", "-an", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    if fr.count("freeze_start"): issues.append(["WARN", f"{fr.count('freeze_start')} frozen segment(s)", 0])

seen = set()
for lvl, msg, t in issues:
    k = (lvl, msg.split("(")[0])
    if k in seen: continue
    seen.add(k); print(f"{lvl}  t={t:7.2f}  {msg}")
fails = sum(1 for i in issues if i[0] == "FAIL")
warns = sum(1 for i in issues if i[0] == "WARN")
print(f"\nQA: {fails} FAIL, {warns} WARN  -> {'PASS' if not fails else 'FAIL'}")
sys.exit(1 if fails else 0)
