"""16:9 contact sheet (engine/contact.py assumes 1080x1920 thumbs)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
d, out = Path(sys.argv[1]), Path(sys.argv[2])
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
files = sorted(p for p in d.iterdir() if p.suffix.lower() in (".png", ".jpg"))
if not files: raise SystemExit("no frames")
tw = 560; th = tw * 9 // 16
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), "white")
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    x, y = (i % cols) * tw, (i // cols) * (th + 22)
    sheet.paste(im, (x, y + 22)); dr.text((x + 6, y + 5), f.stem, fill="#333")
sheet.save(out, quality=88); print(f"{len(files)} frames -> {out}")
