import pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).resolve().parent
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
    pg.goto((here/"cover.html").as_uri()); pg.wait_for_timeout(500)
    res = pg.evaluate("""() => {
      const g = s => { const e = document.querySelector(s); if(!e) return null; const r = e.getBoundingClientRect();
        return {l:Math.round(r.left),t:Math.round(r.top),r:Math.round(r.right),b:Math.round(r.bottom)}; };
      return {card:g('.card'), body:g('.body'), left:g('.left'), sub:g('.sub'), price:g('.price'),
              pnum:g('.pnum'), pm:g('.pm'), checks:g('.checks'), ck3:g('.checks .ck:last-child')};
    }""")
    b.close()
for k,v in res.items(): print(k, v)
