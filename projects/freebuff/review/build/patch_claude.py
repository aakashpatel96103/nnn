"""One-time patch: make the S0 card look like the real Claude app (dark theme) and use the real logo."""
import pathlib, re, sys

here = pathlib.Path(__file__).parent
w = (here / "world.html").read_text(encoding="utf-8")
a = w.index("  <!-- ===== S0 hook")
b = w.index('  <div class="abs stk o" id="s0"')
LOGO = '<svg {a} viewBox="0 0 24 24"><path fill="#D97757" d="@@CLPATH@@"/></svg>'
s0 = '''  <!-- ===== S0 hook: everyone asking Claude (real app look, dark theme) ===== -->
  <div class="abs sc" id="c0" style="left:150px;top:520px;width:780px;height:600px;padding:26px 30px;background:#262624;border-color:#3B3A36;color:#FAF9F5"><div class="sheen" id="sh0"></div>
    <div style="display:flex;align-items:center;gap:14px">''' + LOGO.format(a='width="44" height="44"') + '''<span style="font:500 42px var(--serif);letter-spacing:-.5px">Claude</span><span id="c0paid" style="margin-left:auto;font:600 22px var(--sans);color:#C2C0B6;border:2px solid #4A4944;border-radius:12px;padding:6px 16px">Pro plan</span></div>
    <div style="height:2px;background:#3B3A36;margin:20px -30px 10px"></div>
    <div class="bb" id="b00">Claude, ek reel bana do</div>
    <div class="bb" id="b01">Claude, video edit kar do</div>
    <div class="bb" id="b02">Ek aur reel… please!</div>
    <div style="display:flex;align-items:center;gap:14px;margin-top:24px">''' + LOGO.format(a='id="c0sp" width="40" height="40"') + '''<span id="c0d" style="font:italic 400 28px var(--serif);color:#A6A39A">Thinking</span><span id="c0n" style="display:none">0</span></div>
    <div style="position:absolute;left:26px;right:26px;bottom:24px;height:128px;background:#30302E;border:2px solid #4A4944;border-radius:26px">
      <div style="position:absolute;left:24px;top:18px;font:400 28px var(--sans);color:#8F8D85">Reply to Claude…</div>
      <div style="position:absolute;left:18px;right:16px;bottom:14px;display:flex;align-items:center;gap:14px">
        <span style="width:44px;height:44px;border:2px solid #4A4944;border-radius:12px;display:flex;align-items:center;justify-content:center"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="#C2C0B6" stroke-width="2.2" stroke-linecap="round"/></svg></span>
        <span style="margin-left:auto;font:500 23px var(--sans);color:#C2C0B6">Sonnet 4.5</span><svg width="18" height="18" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" fill="none" stroke="#C2C0B6" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span style="width:46px;height:46px;border-radius:13px;background:#D97757;display:flex;align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </div>
    </div>
  </div>
'''
w = w[:a] + s0 + w[b:]
old = '<span class="cc" style="font:800 30px var(--sans)">Claude</span>'
if old not in w:
    sys.exit("S3 anchor missing")
w = w.replace(old, '<span class="cc" style="font:500 32px var(--serif);gap:10px">' + LOGO.format(a='width="32" height="32"') + 'Claude</span>', 1)
(here / "world.html").write_text(w, encoding="utf-8")

j = (here / "script.js").read_text(encoding="utf-8")
o1 = "$('c0d').textContent='typing'+'.'.repeat(1+Math.floor(t*4)%3);"
o2 = "st($('c0paid'),{transform:`scale(${1+.1*Math.max(0,1-Math.abs(t-1.7)/.18)})`});"
if o1 not in j or o2 not in j:
    sys.exit("script anchor missing")
j = j.replace(o1, "$('c0d').textContent='Thinking'+'.'.repeat(1+Math.floor(t*4)%3); $('c0sp').style.transform=`rotate(${Math.floor(t*6)*30}deg) scale(${1+.08*Math.sin(t*9)})`;")
j = j.replace(o2, "")
(here / "script.js").write_text(j, encoding="utf-8")

bp = (here / "build.py").read_text(encoding="utf-8")
o3 = ".bb{margin:16px 0 0 auto;width:max-content;max-width:640px;background:#262A3A;border:2px solid #343A4E;border-radius:26px 26px 6px 26px;padding:16px 26px;font:600 30px var(--sans);color:#E8EAF0;opacity:0}"
if o3 not in bp:
    sys.exit("css anchor missing")
bp = bp.replace(o3, ".bb{margin:14px 0 0 auto;width:max-content;max-width:640px;background:#141413;border-radius:18px;padding:14px 22px;font:400 29px var(--sans);color:#FAF9F5;opacity:0}")
o4 = 'js = (here / "script.js").read_text(encoding="utf-8")'
bp = bp.replace(o4, o4 + '\nworld = world.replace("@@CLPATH@@", re.search(r\' d="([^"]+)"\', (proj / "review/dl/claude.svg").read_text(encoding="utf-8")).group(1))', 1)
(here / "build.py").write_text(bp, encoding="utf-8")
print("patched")
