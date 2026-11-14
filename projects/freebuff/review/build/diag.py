import sys, pathlib, json
sys.path.insert(0, "engine")
import render as R
from playwright.sync_api import sync_playwright
proj = pathlib.Path("projects/freebuff").resolve()
page = R.build(proj)
with sync_playwright() as pw:
  b, pg, errs = R.open_page(pw, page, dsf=1)
  try:
      pg.evaluate("render(6.4)")
      pg.wait_for_timeout(1500)
      pg.evaluate("render(6.4)")
      pg.wait_for_timeout(300)
      out = pg.evaluate("""(() => {
        const r = [];
        for (let i=34;i<46;i++){ const a=FSH[i], b=FP[i];
          r.push([i, a? [a.complete,a.naturalWidth,a.currentSrc.slice(-12)]:null, b? [b.complete,b.naturalWidth]:null]); }
        const g=id=>{const c=document.getElementById(id); const s=getComputedStyle(c); const r=c.getBoundingClientRect();
          return {w:r.width,h:r.height,x:Math.round(r.left),y:Math.round(r.top),op:s.opacity,vis:s.visibility,z:s.zIndex,bg:s.backgroundColor};};
        return {imgs:r, p:g('cv2p'), s:g('cv2s'), p2:g('p2'), fi:Math.floor((6.4-5.74)*60)};
      })()""")
      print(json.dumps(out))
  finally:
      b.close()
