"""Mix sound effects (src/cues.json) under the voice-over and mux with the silent render.

usage:
  python engine/mix.py <project_dir> [--silent review/silent.mp4] [--out export/<slug>.mp4] [--no-voice]
  python engine/mix.py <project_dir> check     # sync strips per cue -> review/strips/ (look at a few, one per message)

Wraps skills/edit-video/scripts/sfx-sync.mjs (node, built-ins only).
cues.json: {"fps":30, "total":<seconds>, "cues":[{"frame":62, "sound":"curated/ui-pop.wav", "gain":0, "label":"..."}]}
  - total is in SECONDS (not frames). frame wins over t.
  - sound = pack id / pack-relative file (see skills/edit-video/assets/sfx/manifest.json) or a path relative to cues.json
Defaults: duck 6 dB under voice, -14 LUFS, true peak -2.5 dBTP.
"""
import argparse, json, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SYNC = KIT / "skills" / "edit-video" / "scripts" / "sfx-sync.mjs"


def find_voice(proj: Path):
    for ext in (".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"):
        p = proj / "inputs" / f"vo{ext}"
        if p.exists():
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("mode", nargs="?", default="mix")
    ap.add_argument("--silent", default="review/silent.mp4")
    ap.add_argument("--out")
    ap.add_argument("--no-voice", action="store_true")
    ap.add_argument("--duck", default="6")
    ap.add_argument("--lufs", default="-14")
    ap.add_argument("--true-peak", default="-2.5")
    a = ap.parse_args()
    proj = Path(a.project).resolve()
    cfg = json.loads((proj / "project.json").read_text(encoding="utf-8"))
    cues = proj / "src" / "cues.json"
    c = json.loads(cues.read_text(encoding="utf-8"))
    if abs(float(c.get("total", 0)) - float(cfg["duration"])) > 0.01:
        c["total"] = float(cfg["duration"])
        cues.write_text(json.dumps(c, indent=1), encoding="utf-8")
        print(f"cues.json total set to {c['total']}s (seconds, = project duration)")
    mixwav = proj / "review" / "mix.wav"
    silent = proj / a.silent
    if a.mode == "check":
        final = Path(a.out) if a.out else proj / "export" / f"{cfg['slug']}.mp4"
        cmd = ["node", str(SYNC), "check", str(final), "--mix", str(mixwav), "--cues", str(cues), "--strips", str(proj / "review" / "strips")]
    else:
        out = Path(a.out).resolve() if a.out else proj / "export" / f"{cfg['slug']}.mp4"
        if out.exists():
            n = 2
            while out.with_name(f"{out.stem}-v{n}{out.suffix}").exists():
                n += 1
            out = out.with_name(f"{out.stem}-v{n}{out.suffix}")
            print(f"export exists, writing new version {out.name} (never overwrite)")
        cmd = ["node", str(SYNC), "mix", str(cues), "--out", str(mixwav), "--duck", a.duck, "--lufs", a.lufs,
               "--true-peak", a.true_peak, "--seconds", str(cfg["duration"]), "--video", str(silent), "--mux", str(out)]
        voice = find_voice(proj)
        if voice and not a.no_voice:
            cmd[cmd.index("--duck"):cmd.index("--duck")] = ["--voice", str(voice)]
        elif not a.no_voice:
            sys.exit("no inputs/vo.* found - pass --no-voice for an SFX-only reel")
    print(" ".join(cmd))
    sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()
