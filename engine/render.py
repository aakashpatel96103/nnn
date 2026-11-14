"""Render a project's src/reel.html (window.render(t) = pure function of time) to PNG snaps or an MP4.

usage:
  python engine/render.py <project_dir> snap <out_dir> t1 t2 ...     # stills at exact times
  python engine/render.py <project_dir> video <out.mp4> [fps] [--ss=2] [--crf=16] [--preset=slow]  # silent 1080x1920 H.264
  python engine/render.py <project_dir> measure <t> id1 id2 ...      # bounding boxes of elements at time t

Reads <project_dir>/project.json for "duration" (seconds) and "fps".
Builds src/_build.html: __WORDS__ -> src/words.json, __DUR__ -> project.json duration.

Footage projects: while the video loop renders, each frame can wait for lazily decoded
<img> pools to finish loading, otherwise screenshot catches an empty image. Configure it in
project.json as "footage_wait" (one dict or a list of dicts):
  {"from": 5.45, "to": 10.4,        # window of output time to apply the wait
   "start": 5.74, "fps": 60, "count": 270,   # frame index = (t - start) * fps, clamped to count-1
   "expr": "() => {const a=FSH[{fi}],b=FP[{fi}];return !!(a&&a.complete&&a.naturalWidth&&b&&b.complete&&b.naturalWidth);}",
   "require": "typeof FSH!=='undefined'",    # optional JS condition; segment skipped if false
   "timeout": 5000}                          # optional ms
Omitting "footage_wait" keeps the original freebuff behaviour (FSH/FP, 5.45-10.4s, 60fps).
NOTE: do NOT run with `python -I` - playwright often lives in user site-packages.
"""
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

W, H = 1080, 1920

# Original freebuff behaviour: a 60fps lazy <img> pool (FSH/FP) decoded between 5.45s and 10.4s.
DEFAULT_FOOTAGE_WAIT = [{
    "from": 5.45, "to": 10.4, "start": 5.74, "fps": 60, "count": 270,
    "require": "typeof FSH!=='undefined'&&typeof FP!=='undefined'",
    "expr": "() => {const a=FSH[{fi}],b=FP[{fi}];"
            "return !!(a&&a.complete&&a.naturalWidth&&b&&b.complete&&b.naturalWidth);}",
    "timeout": 5000,
}]


def footage_waits(pg, cfg: dict) -> list:
    """Normalise project.json "footage_wait" into segments that apply to this page.

    Each segment waits for lazily decoded <img> pools before a screenshot. Segments whose
    "require" JS condition is false (e.g. FSH undefined because this project has no footage
    pool) are dropped, so a shared default is harmless for every other project.
    """
    raw = cfg.get("footage_wait", DEFAULT_FOOTAGE_WAIT)
    segs = [raw] if isinstance(raw, dict) else list(raw or [])
    out = []
    for s in segs:
        s = dict(s)
        s.setdefault("timeout", 5000)
        req = s.get("require")
        if req and not pg.evaluate("()=>!!(" + req + ")"):
            continue
        s.setdefault("expr", DEFAULT_FOOTAGE_WAIT[0]["expr"])
        out.append(s)
    return out


def wait_footage(pg, t: float, segs: list) -> None:
    for s in segs:
        if not (s["from"] < t < s["to"]):
            continue
        fi = max(0, min(int(s.get("count", 1e9)) - 1, int((t - s["start"]) * s["fps"])))
        expr = s["expr"].replace("{fi}", str(fi))
        try:
            pg.wait_for_function(expr, timeout=s["timeout"])
        except Exception as e:
            raise SystemExit(f"footage frame {fi} not decoded at t={t:.2f}s (window {s['from']}-{s['to']}s): {e}")


def load_project(proj: Path) -> dict:
    cfg = json.loads((proj / "project.json").read_text(encoding="utf-8"))
    cfg.setdefault("fps", 30)
    return cfg


def build(proj: Path) -> Path:
    src = proj / "src"
    html = (src / "reel.html").read_text(encoding="utf-8")
    words_file = src / "words.json"
    words = words_file.read_text(encoding="utf-8") if words_file.exists() else "[]"
    dur = str(float(load_project(proj)["duration"]))
    out = src / "_build.html"
    out.write_text(html.replace("__WORDS__", words).replace("__DUR__", dur), encoding="utf-8")
    return out


def open_page(p, page_path: Path, dsf: int = 1):
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=dsf)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.goto(page_path.as_uri())
    pg.wait_for_timeout(600)  # fonts/images
    if errs:
        raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))
    if not pg.evaluate("typeof window.render === 'function'"):
        raise SystemExit("reel.html must define window.render(t)")
    return b, pg, errs


def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    proj, mode, target = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
    cfg = load_project(proj)
    page_path = build(proj)
    dsf = 2 if (mode == "video" and "--ss=2" in sys.argv) else 1
    with sync_playwright() as p:
        b, pg, errs = open_page(p, page_path, dsf)
        if mode == "snap":
            target.mkdir(parents=True, exist_ok=True)
            for ts in sys.argv[4:]:
                pg.evaluate(f"render({float(ts)})")
                if "--wait=0" not in sys.argv:
                    pg.wait_for_timeout(900)
                    pg.evaluate(f"render({float(ts)})")
                pg.screenshot(path=str(target / f"t{float(ts):06.2f}.png"))
            print(f"wrote {len(sys.argv) - 4} snaps to {target}")
        elif mode == "measure":
            t = float(sys.argv[3])
            pg.evaluate(f"render({t})")
            for i in sys.argv[4:]:
                r = pg.evaluate(
                    "(id)=>{const e=document.getElementById(id); if(!e) return null; const r=e.getBoundingClientRect();"
                    "return [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom),getComputedStyle(e).opacity]}", i)
                print(i, r)
        elif mode == "video":
            rest = [r for r in sys.argv[4:] if not r.startswith("--")]
            fps = int(rest[0]) if rest else int(cfg["fps"])
            crf = next((r.split("=", 1)[1] for r in sys.argv if r.startswith("--crf=")), "16")
            preset = next((r.split("=", 1)[1] for r in sys.argv if r.startswith("--preset=")), "slow")
            n = int(round(float(cfg["duration"]) * fps))
            waits = footage_waits(pg, cfg)
            target.parent.mkdir(parents=True, exist_ok=True)
            scale = ["-vf", f"scale={W}:{H}:flags=lanczos"] if dsf > 1 else []
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps),
                                   "-i", "-", *scale, "-c:v", "libx264", "-preset", preset, "-crf", crf,
                                   "-profile:v", "high", "-level", "4.2", "-g", str(fps * 2),
                                   "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target)],
                                  stdin=subprocess.PIPE)
            for i in range(n):
                t = i / fps
                pg.evaluate(f"render({t})")
                wait_footage(pg, t, waits)  # lazy <img> pools (footage projects) must be decoded before the shot
                ff.stdin.write(pg.screenshot(type="png"))
                if i % 30 == 0:
                    print(f"frame {i}/{n}", flush=True)
            ff.stdin.close(); ff.wait()
            if ff.returncode:
                raise SystemExit("ffmpeg failed")
            print(f"done {n} frames -> {target}")
        else:
            raise SystemExit("mode must be snap | video | measure")
        if errs:
            raise SystemExit("PAGE ERRORS during render:\n" + "\n".join(errs))
        b.close()


if __name__ == "__main__":
    main()
