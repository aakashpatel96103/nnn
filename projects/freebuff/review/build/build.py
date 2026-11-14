"""Assemble projects/freebuff/src/reel.html from the sparrowcodes v3 base + this reel's parts."""
import re, sys, pathlib

here = pathlib.Path(__file__).parent
proj = here.parent.parent
base = (proj / "review/t/base.html").read_text(encoding="utf-8")
world = (here / "world.html").read_text(encoding="utf-8")
js = (here / "script.js").read_text(encoding="utf-8")
world = world.replace("@@CLPATH@@", re.search(r' d="([^"]+)"', (proj / "review/dl/claude.svg").read_text(encoding="utf-8")).group(1))
parts = dict(re.findall(r"//@@(\w+)\n(.*?)(?=//@@|\Z)", js, flags=re.S))


def cut(src, start, end, new):
    a = src.index(start)
    b = src.index(end, a)
    return src[:a] + new + src[b:]


out = base
out = cut(out, '<div id="world">', '<div id="vig"', world)
out = cut(out, "/* =================== CONFIG", "/* =================== HELPERS", parts["CONFIG"])
out = cut(out, "/* =================== BUILD DYNAMIC DOM", "/* captions:", parts["BUILD"])
out = cut(out, "/* =================== SCENE FX", "/* =================== DRAWING", parts["FX"])

css = """
/* ===== this reel ===== */
.bb{margin:14px 0 0 auto;width:max-content;max-width:640px;background:#141413;border-radius:18px;padding:14px 22px;font:400 29px var(--sans);color:#FAF9F5;opacity:0}
.mt{width:112px;height:199px;border-radius:16px;overflow:hidden;border:4px solid #000;box-shadow:0 14px 28px rgba(0,0,0,.4);opacity:0;flex:none}
.mt img{width:100%;height:100%;object-fit:cover;display:block}
.nb{display:inline-block;height:26px;border-radius:7px;background:repeating-linear-gradient(90deg,#9AA0B4 0 16px,#5C6275 16px 25px,#B9BED0 25px 44px,#4A4F60 44px 52px);filter:blur(6px)}
.cr{display:flex;align-items:center;height:146px;border-bottom:2px solid #262A36;position:relative}
.cr .cl{flex:1;font:600 32px var(--sans)}
.cr .cc{width:206px;display:flex;align-items:center;justify-content:center;flex:none}
.cr .cc:last-child{margin-right:-8px}
.ck3{width:58px;height:58px;border-radius:50%;border:3px solid #3A4052;display:flex;align-items:center;justify-content:center;flex:none}
.fr{left:150px;width:780px;height:164px;padding:0 32px;display:flex;align-items:center;gap:26px;border-radius:26px}
.fi{width:92px;height:92px;border-radius:24px;display:flex;align-items:center;justify-content:center;flex:none}
.ft{display:block;font:800 42px var(--sans);letter-spacing:-1px}
.fs{display:block;font:600 21px var(--mono);letter-spacing:1px;color:#8E93A6;margin-top:6px}
"""
out = out.replace("\n/* wipe canvas */", css + "\n/* wipe canvas */", 1)

reps = [
    ("cursorAt(t); dockAt(t,si); drawFx(t);", "cursorAt(t); drawFx(t);"),
    ("const AU=[.2,.34,.16,.34,.34,.38,.38,0];", "const AU=[.30,.36,.34,.36,.30,0];"),
    ("['pc','s5','s6','upi'].forEach(id=>$(id).style.opacity=0);", "['r40','r41','r42','j4','s4'].forEach(id=>$(id).style.opacity=0);"),
    ("const BURSTS=[[2.36,790,850],[8.46,800,520],[15.12,770,500],[23.5,790,505],[25.9,300,770],[31.74,740,715],[38.55,770,845]];",
     "const BURSTS=[[2.38,770,505],[4.24,760,505],[8.0,766,800],[11.44,800,735],[18.22,540,1120],[23.82,770,845]];"),
    ("border:5px solid #7C7FF2;opacity:0;pointer-events:none;z-index:49", "border:5px solid #D97757;opacity:0;pointer-events:none;z-index:49"),
]
reps += [
    ("/* ===== SparrowCodes UI (rebuilt from the recording) ===== */", "/* ===== app UI ===== */"),
    ("  if(w.w==='U'&&b&&b.w==='P'&&c&&c.w==='I'){ CW.push(Object.assign({},w,{w:'UPI',e:c.e})); i+=2; } else CW.push(w); }", "  CW.push(w); }"),
    ('<div class="abs" id="dock" data-qa-ignore>', '<div class="abs" id="dock" data-qa-ignore style="display:none">'),
]
for a, b in reps:
    if a not in out:
        sys.exit("missing anchor: " + a[:50])
    out = out.replace(a, b, 1)

low = out.lower()
for bad in ("freebuff", "sparrow"):
    if bad in low:
        sys.exit("forbidden word in output: " + bad)
(proj / "src/reel.html").write_text(out, encoding="utf-8")
print("ok", len(out))
