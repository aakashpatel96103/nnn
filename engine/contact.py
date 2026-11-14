"""Contact sheet: many frames of a video (or a folder of PNG snaps) in ONE image.

Why: most AI APIs reject requests with more than ~8 images. Review a reel by looking at
ONE contact sheet per message, never dozens of separate frames.

usage:
  python engine/contact.py <video.mp4 | snaps_dir> <out.jpg> [--every 0.5] [--cols 6] [--start 0] [--end 999]
"""
import argparse, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def frames_from_video(video: Path, every: float, start: float, end: float, tmp: Path):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(video)]).decode().strip())
    end = min(end, dur - 0.01)
    out, t = [], start
    while t <= end + 1e-6:
        p = tmp / f"f{t:07.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=270:-1", str(p)], check=True)
        if p.exists():
            out.append((t, p))
        t += every
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--every", type=float, default=0.5)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=999.0)
    a = ap.parse_args()
    src = Path(a.src)
    with tempfile.TemporaryDirectory() as td:
        if src.is_dir():
            items = []
            for p in sorted(src.glob("*.png")):
                try:
                    t = float(p.stem.lstrip("tf"))
                except ValueError:
                    t = len(items)
                items.append((t, p))
        else:
            items = frames_from_video(src, a.every, a.start, a.end, Path(td))
        if not items:
            raise SystemExit("no frames")
        tw = 270
        th = int(tw * 1920 / 1080)
        cols = min(a.cols, len(items))
        rows = (len(items) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw + (cols + 1) * 6, rows * (th + 30) + 6), "white")
        d = ImageDraw.Draw(sheet)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except OSError:
            font = ImageFont.load_default()
        for i, (t, p) in enumerate(items):
            im = Image.open(p).convert("RGB").resize((tw, th))
            x = 6 + (i % cols) * (tw + 6)
            y = 6 + (i // cols) * (th + 30)
            sheet.paste(im, (x, y + 24))
            d.text((x + 2, y), f"{t:.2f}s", fill="black", font=font)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        sheet.save(a.out, quality=85)
        print(f"contact sheet {len(items)} frames -> {a.out}")


if __name__ == "__main__":
    main()
