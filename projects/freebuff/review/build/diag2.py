import sys, pathlib, json
sys.path.insert(0, "engine")
import render as R
from playwright.sync_api import sync_playwright
proj = pathlib.Path("projects/freebuff").resolve()
page = R.build(proj)
outdir = proj / "review" / "diag"
outdir.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
  b, pg, errs = R.open_page(pw, page, dsf=1)
  try:
      for t in (6.4, 9.6):
          pg.evaluate(f"render({t})")
          pg.wait_for_timeout(900)
          pg.evaluate(f"render({t})")
          pg.wait_for_timeout(300)
          pg.locator("#cv2p").screenshot(path=str(outdir / f"cv2p_{t}.png"))
          pg.locator("#cv2s").screenshot(path=str(outdir / f"cv2s_{t}.png"))
      print("ok", errs)
  finally:
      b.close()
