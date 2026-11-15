"""Render this 1920x1080 project with the kit renderer, frame size patched.

engine/render.py hardcodes 1080x1920 (reels). Instead of editing the kit we import it, override
its module-level W/H and call main() with our argv.

  python src/render169.py <project> snap <out_dir> 2 8 14 ...
  python src/render169.py <project> video <out.mp4> [fps] [--crf=17] [--preset=veryfast]
  python src/render169.py <project> measure <t> id1 id2 ...
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine"))
import render  # noqa: E402

render.W, render.H = 1920, 1080
render.main()
