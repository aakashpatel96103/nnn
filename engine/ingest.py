"""Inventory everything the user dropped in inputs/ so the agent can SEE it with few images.

usage:
  python engine/ingest.py <project_dir>

For each file in inputs/:
  images  -> size printed; copied (unchanged) to assets/
  videos  -> duration/size printed; one contact sheet review/ingest_<name>.jpg (frame every 1s, max 36)
             + keyframes extracted to assets/<name>_frames/fNNN.png every 0.5s (pick from these to rebuild UI)
  audio   -> duration, loudness printed; if no vo.* yet and it is the only audio, copied to inputs/vo.<ext>
  text    -> first lines printed (script.txt, notes)
Writes review/ingest.json. Look at the contact sheets ONE per message.
"""
import json, shutil, subprocess, sys
from pathlib import Path

IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VID = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}
AUD = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".opus"}
TXT = {".txt", ".md"}


def dur(p):
    try:
        return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())
    except Exception:
        return None


def main():
    proj = Path(sys.argv[1]).resolve()
    inp, assets, review = proj / "inputs", proj / "assets", proj / "review"
    assets.mkdir(exist_ok=True); review.mkdir(exist_ok=True)
    rep = []
    for p in sorted(inp.iterdir()):
        ext = p.suffix.lower()
        if ext in IMG:
            from PIL import Image
            w, h = Image.open(p).size
            shutil.copy(p, assets / p.name)
            rep.append({"file": p.name, "kind": "image", "size": [w, h]})
            print(f"IMAGE {p.name} {w}x{h} -> assets/")
        elif ext in VID:
            d = dur(p) or 0
            fdir = assets / f"{p.stem}_frames"; fdir.mkdir(exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-vf", "fps=2", str(fdir / "f%03d.png")], check=True)
            every = max(1.0, d / 36)
            subprocess.run([sys.executable, str(Path(__file__).parent / "contact.py"), str(p), str(review / f"ingest_{p.stem}.jpg"),
                            "--every", f"{every:.2f}"], check=True)
            rep.append({"file": p.name, "kind": "video", "duration": d, "frames": str(fdir.relative_to(proj)),
                        "sheet": f"review/ingest_{p.stem}.jpg"})
            print(f"VIDEO {p.name} {d:.1f}s -> frames every 0.5s in {fdir.name}/, sheet review/ingest_{p.stem}.jpg")
        elif ext in AUD:
            d = dur(p)
            rep.append({"file": p.name, "kind": "audio", "duration": d})
            print(f"AUDIO {p.name} {d:.2f}s")
        elif ext in TXT:
            t = p.read_text(encoding="utf-8", errors="replace")
            rep.append({"file": p.name, "kind": "text", "chars": len(t)})
            print(f"TEXT  {p.name}: {t.strip()[:200]!r}")
        else:
            rep.append({"file": p.name, "kind": "other"})
            print(f"OTHER {p.name} (ask the user what it is for)")
    auds = [r for r in rep if r["kind"] == "audio"]
    if auds and not any(r["file"].startswith("vo.") for r in auds) and len(auds) == 1:
        src = inp / auds[0]["file"]
        dst = inp / ("vo" + src.suffix.lower())
        shutil.copy(src, dst)
        print(f"copied {src.name} -> {dst.name} (the voice-over)")
    (review / "ingest.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
