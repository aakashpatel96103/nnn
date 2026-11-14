"""Render cover.html at 2x (2160x3840) and print element boxes for safe-area QA."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).resolve().parent
out = here / "cover-2x.png"

BOX = r"""
() => {
  const out = [];
  const seen = new Set();
  const walk = (el) => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) {
        const rg = document.createRange(); rg.selectNodeContents(n);
        const r = rg.getBoundingClientRect();
        out.push({t: n.textContent.trim().slice(0, 40), l: Math.round(r.left), tp: Math.round(r.top), r: Math.round(r.right), b: Math.round(r.bottom), w: Math.round(r.width)});
      } else if (n.nodeType === 1) walk(n);
    }
  };
  walk(document.body);
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
    pg.goto(out.parent.joinpath("cover.html").as_uri())
    pg.wait_for_timeout(700)
    boxes = pg.evaluate(BOX)
    pg.screenshot(path=str(out), full_page=False)
    b.close()

bad = []
for x in boxes:
    if x["t"].startswith("//"): continue
    if x["l"] < 60 or x["r"] > 1020 or x["tp"] < 200 or x["b"] > 1700:
        bad.append(x)
print(json.dumps({"n_text": len(boxes), "outside_safe": bad}, indent=1, ensure_ascii=False))
widths = sorted(boxes, key=lambda x: -x["w"])[:6]
print("widest:", [(x["t"], x["w"]) for x in widths])
