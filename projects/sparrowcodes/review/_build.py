"""One-off builder: turns the template copy in src/reel.html into the SparrowCodes reel.
Run from the project folder: python review/_build.py"""
import json

p = 'src/reel.html'
s = open(p, encoding='utf-8').read()
assert 'id="ph0"' not in s, 'already built'


def cut(s, start, end, new, keep_end=True):
    a = s.index(start)
    b = s.index(end, a)
    return s[:a] + new + (s[b:] if keep_end else s[b + len(end):])


# ---------- CSS ----------
css = r'''
/* ===== SparrowCodes UI (rebuilt from the recording) ===== */
.sc{background:#0F1117;border:2px solid #262A36;border-radius:28px;box-shadow:0 30px 70px rgba(10,12,30,.30);color:#E8EAF0;opacity:0}
.sc .mut{color:#8E93A6}
.pu{color:#8B8EFF}
.chip{display:inline-flex;align-items:center;gap:10px;height:58px;padding:0 20px;border:2px solid #2B3040;border-radius:12px;font:600 25px var(--sans);color:#E8EAF0;background:#12141C}
.chip .k{color:#8E93A6;font-weight:500}
.beta{font:800 18px var(--mono);letter-spacing:1px;color:#A9ABFF;border:2px solid #3A3D7A;background:#1B1D3A;border-radius:8px;padding:4px 10px}
.btn{display:inline-flex;align-items:center;justify-content:center;height:66px;padding:0 30px;border-radius:12px;background:#7C7FF2;color:#fff;font:700 28px var(--sans)}
.vid{background:radial-gradient(circle at 30% 18%,rgba(150,40,200,.85),transparent 55%),radial-gradient(circle at 85% 62%,rgba(30,170,200,.75),transparent 55%),radial-gradient(circle at 40% 98%,rgba(110,140,40,.7),transparent 42%),#050507;border-radius:22px;overflow:hidden;border:3px solid #111;box-shadow:0 24px 50px rgba(0,0,0,.28);opacity:0}
.vid .vt{position:absolute;left:0;right:0;text-align:center;font:800 34px var(--sans);color:#fff;letter-spacing:-.5px}
.vid .wm{position:absolute;right:10px;bottom:10px;font:700 9px var(--mono);letter-spacing:1px;color:rgba(255,255,255,.75)}
.vid .bar{position:absolute;left:14px;right:14px;bottom:30px;height:5px;border-radius:3px;background:rgba(255,255,255,.25)}
.vid .bar b{display:block;height:100%;background:#fff;border-radius:3px;width:0}
.tl{font:500 26px var(--mono);line-height:1.0;height:52px;display:flex;align-items:center;white-space:pre;opacity:0}
.prow{display:flex;align-items:center;gap:18px;font:500 30px var(--sans);height:74px;opacity:0}
.prow svg{flex:none}
.gchip{font:800 20px var(--mono);letter-spacing:1px;color:#fff;background:var(--green);padding:6px 12px;border-radius:8px;opacity:0}
.uav{width:62px;height:62px;border-radius:50%;background:#D9D5CE;flex:none;position:relative;overflow:hidden}
.uav::after{content:"";position:absolute;left:19px;top:12px;width:24px;height:24px;border-radius:50%;background:#fff;opacity:.9}
.uav::before{content:"";position:absolute;left:10px;top:40px;width:42px;height:40px;border-radius:50%;background:#fff;opacity:.9}
.crow{display:flex;align-items:center;gap:18px;margin-top:20px}
#posted{height:0;overflow:hidden}
#dm{left:150px;top:850px;width:780px;background:#fff;border:2px solid var(--line);border-radius:28px;box-shadow:0 30px 70px rgba(0,0,0,.14);padding:24px 28px;opacity:0}
#dm .hd{display:flex;align-items:center;gap:16px}
#dm .hd img{width:66px;height:66px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 2px var(--clay)}
#dm .bub{margin-top:18px;background:#EFEFEF;border-radius:26px;padding:18px 24px;font:500 28px var(--sans);line-height:1.3;width:640px}
#dm .lnk{margin-top:12px;display:inline-flex;align-items:center;gap:12px;background:var(--ink);color:#fff;border-radius:999px;padding:12px 24px;font:700 26px var(--mono)}
'''
assert '/* wipe canvas */' in s
s = s.replace('/* wipe canvas */', css + '\n/* wipe canvas */', 1)

# ---------- BODY (world) ----------
CK = '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#3DDC84" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PILLCK = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
world = '''<div id="world">
  <!-- ===== HEADLINES ===== -->
  <div class="abs head" id="h0" data-qa-text style="font-size:96px"><span class="l">Ye video bas</span><span class="l"><i><span class="hl" id="hl0">ek sentence</span> se.</i></span></div>
  <div class="abs head" id="h1" data-qa-text style="font-size:96px"><span class="l">Sentence <i>type karo,</i></span><span class="l"><span class="hl" id="hl1">video ready.</span></span></div>
  <div class="abs head" id="h2" data-qa-text style="font-size:100px"><span class="l">Free mein</span><span class="l"><i><span class="hl" id="hl2">3 videos.</span></i></span></div>
  <div class="abs head" id="h3" data-qa-text style="font-size:96px"><span class="l">Voiceover bhi</span><span class="l"><i><span class="hl" id="hl3">roz free.</span></i></span></div>
  <div class="abs head" id="h4" data-qa-text style="font-size:96px"><span class="l">Terminal mein</span><span class="l"><i><span class="hl" id="hl4">coding agent.</span></i></span></div>
  <div class="abs head" id="h5" data-qa-text style="font-size:96px"><span class="l"><span class="hl" id="hl5">$10 se</span></span><span class="l"><i>30 din ka plan.</i></span></div>
  <div class="abs head" id="h6" data-qa-text style="font-size:100px"><span class="l">Auto-renew</span><span class="l"><i><span class="hl" id="hl6">nahi hota.</span></i></span></div>
  <div class="abs head" id="h7" data-qa-text style="font-size:96px"><span class="l">Comment</span><span class="l"><i class="hl" id="hl7">“SPARROW”</i></span></div>

  <!-- ===== S0 hook: finished 9:16 video + the one sentence ===== -->
  <div class="abs vid" id="ph0" style="left:405px;top:508px;width:270px;height:480px">
    <div class="vt" id="ph0t" style="top:200px">Code to Video</div><div class="bar"><b id="ph0b"></b></div><div class="wm">SPARROWCODES</div>
  </div>
  <div class="abs sc" id="pr0" style="left:150px;top:1012px;width:780px;height:118px;padding:0 30px;display:flex;align-items:center;font:500 29px var(--mono)">
    <span class="pu" style="margin-right:14px">›</span><span id="pr0t"></span><span id="pr0c" style="display:inline-block;width:4px;height:36px;background:#8B8EFF;margin-left:4px"></span>
  </div>
  <div class="abs stk" id="s0a" data-qa-text style="left:120px;top:640px">1 SENTENCE</div>
  <div class="abs stk g" id="s0" data-qa-text style="left:720px;top:820px;font-size:40px">FREE!</div>

  <!-- ===== S1 Video page ===== -->
  <div class="abs sc" id="v1" style="left:150px;top:520px;width:780px;height:616px;padding:30px 34px">
    <div style="display:flex;align-items:center;gap:16px"><img src="../assets/sparrow-mark.png" style="height:46px"><span style="font:800 42px var(--sans);letter-spacing:-1px">Video</span><span class="beta">BETA</span></div>
    <div style="margin-top:22px;height:150px;border:2px solid #2B3040;border-radius:14px;background:#0B0D12;padding:18px 22px;font:500 29px var(--sans);line-height:1.35"><span id="v1t"></span><span id="v1c" style="display:inline-block;width:3px;height:32px;background:#8B8EFF;margin-left:3px;vertical-align:-5px"></span><span id="v1ph" class="mut">What should the video say?</span></div>
    <div style="display:flex;gap:14px;margin-top:20px"><div class="chip" id="v1f"><span class="k">Format</span><span id="v1fv">9:16</span></div><div class="chip"><span class="k">Length</span>15 s</div><div class="chip"><span class="k">Voice</span>Aria</div></div>
    <div style="display:flex;align-items:center;gap:20px;margin-top:22px"><div class="btn" id="v1b">▶&nbsp; Create video</div><span class="mut" id="v1ff" style="font:600 20px var(--mono);letter-spacing:1px;opacity:0">FAST-FORWARD · A FEW MINUTES</span></div>
    <div id="v1p" style="margin-top:24px;opacity:0">
      <div style="display:flex;justify-content:space-between;font:600 25px var(--sans)"><span id="v1s">Planning scenes and copy</span><span id="v1n" class="pu" style="font-family:var(--mono)">0%</span></div>
      <div style="margin-top:12px;height:12px;border-radius:6px;background:#22263A;overflow:hidden"><div id="v1pb" style="height:100%;width:0;background:#7C7FF2;border-radius:6px"></div></div>
    </div>
  </div>
  <div class="abs pill" id="ok1" style="left:700px;top:498px">@PILLCK@VIDEO READY</div>

  <!-- ===== S2 three free videos + the small mark ===== -->
  <div id="tiles2"></div>
  <svg class="abs" id="ring2" width="170" height="170" style="left:805px;top:838px;opacity:0" data-qa-ignore><circle cx="85" cy="85" r="76" fill="none" stroke="#D97757" stroke-width="7" stroke-dasharray="14 10"/></svg>
  <div class="abs sc" id="mk2" style="left:330px;top:1010px;height:96px;padding:0 30px;display:flex;align-items:center;gap:16px;border-radius:20px"><img src="../assets/sparrow-mark.png" style="height:52px"><span style="font:700 34px var(--mono);letter-spacing:3px">SPARROWCODES</span></div>
  <div class="abs label" id="lab2" style="left:330px;top:1118px;opacity:0">// CORNER MEIN CHHOTA MARK</div>
  <div class="abs stk g" id="s2" data-qa-text style="left:690px;top:470px">3 FREE</div>

  <!-- ===== S3 Speech ===== -->
  <div class="abs sc" id="sp" style="left:150px;top:520px;width:780px;height:610px;padding:30px 36px">
    <div style="display:flex;align-items:center;gap:16px"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M4 9.5v5h3.5L12 18.5v-13L7.5 9.5z" fill="#8B8EFF"/><path d="M15.5 9a4.5 4.5 0 010 6M18 6.5a8 8 0 010 11" fill="none" stroke="#8B8EFF" stroke-width="2" stroke-linecap="round"/></svg><span style="font:800 42px var(--sans);letter-spacing:-1px">Speech</span><span class="gchip" id="spfree" style="margin-left:auto">FREE</span></div>
    <div style="margin-top:22px;height:76px;border-radius:999px;background:#2A2C35;display:flex;align-items:center;padding:0 26px;gap:18px"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M6 4l14 8-14 8z" fill="#fff"/></svg><span style="font:600 24px var(--mono)" id="sptm">0:00 / 1:02</span><div style="flex:1;height:6px;border-radius:3px;background:#555A66"><div id="sppb" style="height:100%;width:0;background:#fff;border-radius:3px"></div></div></div>
    <div style="margin-top:26px;display:flex;align-items:baseline;gap:18px"><span id="spnum" style="font:800 124px var(--sans);letter-spacing:-4px;line-height:1">0</span><span class="mut" style="font:600 28px var(--sans);line-height:1.2">characters<br>free, every day</span></div>
    <div style="display:flex;gap:14px;margin-top:26px"><div class="chip" id="splang" style="opacity:0"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8B8EFF" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>31 languages</div></div>
    <div id="spcl" style="margin-top:20px;height:92px;border:2px solid #7C7FF2;border-radius:14px;display:flex;align-items:center;padding:0 22px;gap:18px;opacity:0"><span style="font:700 29px var(--sans)">Clone your own voice</span><div id="spwv" style="flex:1;display:flex;align-items:center;gap:5px;height:56px"></div><span class="beta" id="spvc" style="opacity:0">Voice cloning</span></div>
  </div>
  <div class="abs stk o" id="s3" data-qa-text style="left:670px;top:476px">ROZ FREE</div>

  <!-- ===== S4 terminal (session from sparrowcodes.com/cli) ===== -->
  <div class="abs sc" id="tm" style="left:130px;top:520px;width:820px;height:600px;background:#0B0D12;overflow:hidden">
    <div style="height:64px;background:#161922;display:flex;align-items:center;padding:0 24px;gap:10px"><i style="width:16px;height:16px;border-radius:50%;background:#FF5F57"></i><i style="width:16px;height:16px;border-radius:50%;background:#FEBC2E"></i><i style="width:16px;height:16px;border-radius:50%;background:#28C840"></i><span class="mut" style="font:600 22px var(--mono);margin-left:14px">~/invoice-app</span></div>
    <div style="padding:22px 32px" id="tml"></div>
  </div>
  <div class="abs pill" id="ok4" style="left:660px;top:1090px">@PILLCK@TESTS PASSED</div>
  <div class="abs stk o" id="s4" data-qa-text style="left:680px;top:478px">BUG FIXED!</div>

  <!-- ===== S5 + S6 pricing card (Developer plan) ===== -->
  <div class="abs sc" id="pc" style="left:170px;top:520px;width:740px;height:612px;padding:34px 40px;border-color:#7C7FF2">
    <div style="display:flex;align-items:center"><span style="font:800 42px var(--sans);letter-spacing:-1px">Developer</span>
      <div id="cur" style="margin-left:auto;display:flex;border:2px solid #2B3040;border-radius:12px;overflow:hidden;font:700 24px var(--sans)"><span id="curI" style="padding:9px 16px">₹ INR</span><span id="curU" style="padding:9px 16px">$ USD</span></div></div>
    <div class="mut" style="font:500 25px var(--sans);margin-top:6px">For everyday coding on fast models</div>
    <div style="display:flex;align-items:baseline;gap:14px;margin-top:18px;height:120px"><span id="pcp" style="font:800 116px var(--sans);letter-spacing:-4px;line-height:1;display:inline-block;transform-origin:left bottom">$10</span><span id="pcd" class="mut" style="font:600 34px var(--sans)">/ 30 days</span></div>
    <div class="mut" style="font:500 22px var(--sans);margin-top:4px">Plus 18% GST in India</div>
    <div style="height:2px;background:#262A36;margin:20px 0 10px"></div>
    <div class="prow" id="pr1">@CK@Coding agent in your terminal</div>
    <div class="prow" id="pr2">@CK@Fast AI models: DeepSeek, Claude Haiku…</div>
    <div class="prow" id="pr3">@CK@10 watermark-free videos / 30 days</div>
    <div id="pcn" class="mut" style="font:600 22px var(--mono);letter-spacing:.5px;margin-top:14px;opacity:0">PLANS LAST 30 DAYS · NEVER RENEW BY THEMSELVES</div>
  </div>
  <div class="abs stk g" id="s5" data-qa-text style="left:650px;top:474px">NO WATERMARK</div>
  <div class="abs stk o" id="s6" data-qa-text style="left:560px;top:690px;font-size:38px">NO AUTO-RENEW</div>
  <div class="abs pill" id="upi" style="left:640px;top:1098px;font-size:26px;padding:10px 20px">@PILLCK@UPI · ₹ RUPEES</div>

  <!-- ===== S7 comment to DM ===== -->
  <div class="abs card" id="cbox" style="left:150px;top:520px;width:780px;padding:26px 30px">
    <div style="font:700 30px var(--sans);text-align:center;padding-bottom:18px;border-bottom:1px solid #eee">Comments</div>
    <div id="posted"><div class="crow"><div class="uav"></div><div><div style="font:700 24px var(--sans)">you <span style="color:#999;font-weight:500">· now</span></div><div style="font:800 34px var(--sans);letter-spacing:1px">SPARROW</div></div>
      <svg style="margin-left:auto" width="34" height="34" viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z" fill="#ED4956"/></svg></div></div>
    <div class="crow"><div class="uav"></div><div id="field"><span id="ftxt"></span><span class="ph" id="fph">Add a comment…</span></div><div id="post">Post</div></div>
  </div>
  <div class="abs" id="dm">
    <div class="hd"><img src="../assets/avatar.png"><div><div style="font:700 28px var(--sans)">mukku.tech</div><div style="font:500 20px var(--sans);color:var(--mute)">sent you a message · now</div></div></div>
    <div class="bub">Ye lo <b>SparrowCodes</b> ka link. Free start, card nahi chahiye.</div>
    <div class="lnk"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>sparrowcodes.com</div>
  </div>
  <div class="abs pill" id="sent" style="left:690px;top:826px">@PILLCK@DM SENT</div>
  <div class="abs stk g" id="s7" data-qa-text style="left:120px;top:470px">NO CARD</div>
</div>

'''.replace('@PILLCK@', PILLCK).replace('@CK@', CK)
s = cut(s, '<div id="world">', '<div id="vig"', world)

# ---------- CONFIG ----------
cfg = r'''const DUR = __DUR__;
const WORDS = __WORDS__;
const HANDLE = "@mukku.tech";
const SC = [0, 3.22, 9.06, 12.80, 18.84, 24.42, 31.10, 34.86];
const CRUMBS = ["// 01 — 1 SENTENCE","// 02 — VIDEO","// 03 — 3 FREE","// 04 — VOICE","// 05 — CODING AGENT","// 06 — PLAN","// 07 — NO AUTO-RENEW","// 08 — COMMENT “SPARROW”"];
const HL_T = [0.94, 8.14, 9.52, 13.86, 20.34, 25.90, 31.74, 37.08];
const KICK = [2.36, 8.46, 9.84, 15.02, 23.9, 25.9, 31.74, 37.75, 38.55];
const WIPE = {a: SC[7]-.34, m: SC[7], b: SC[7]+.34};
const KEYW = /^["“]?(free|sentence|Sparrow|Codes|ready|teen|voiceover|clone|agent|fix|dollar|plan|watermark-free|Auto-renew|rupees|Comment|DM)["”]?[,!.?]*$/i;
const END_T = 39.05;
const CURSOR = [
  [5.7, 900, 1060], [6.6, 245, 787, 1], [7.2, 300, 868, 1], [7.7, 300, 868], null,
  [32.9, 900, 1010], [33.75, 713, 583, 1], [34.4, 713, 583], null,
  [35.9, 980, 1000], [36.7, 470, 668, 1], [37.75, 858, 662, 1], [38.4, 858, 662], null,
];

'''
s = cut(s, 'const DUR = __DUR__;', '/* =================== HELPERS (keep)', cfg)

# ---------- BUILD DOM ----------
build = r'''/* =================== BUILD DYNAMIC DOM (per reel) =================== */
$('hname').textContent=HANDLE;
// S2 tiles
const TX2=[150,430,710], TT2=["Code to Video","App launch","Explainer"];
TX2.forEach((x,i)=>{const d=document.createElement('div'); d.className='abs vid'; d.id='t2'+i;
  st(d,{left:x+'px',top:'540px',width:'220px',height:'391px'});
  d.innerHTML=`<div class="vt" style="top:160px;font-size:27px">${TT2[i]}</div><div class="wm">SPARROWCODES</div><div class="gchip" id="t2f${i}" style="position:absolute;left:12px;top:12px">FREE</div><div style="position:absolute;right:12px;top:12px;font:800 20px var(--mono);color:#fff">${i+1}/3</div>`;
  $('tiles2').appendChild(d);});
// S3 waveform bars
for(let i=0;i<22;i++){const b=document.createElement('i'); b.id='wv'+i; st(b,{display:'block',width:'6px',borderRadius:'3px',background:'#8B8EFF',height:'10px'}); $('spwv').appendChild(b);}
// S4 terminal lines: [text, color, time, typeDur]
const TL=[
  ["$ sparrowcodes","#E8EAF0",19.86,.7],
  ["> Write tests for invoice.py, fix any bugs","#A9ABFF",21.0,1.1],
  ["  ✓ Wrote tests/test_invoice.py, 14 tests","#3DDC84",22.38,0],
  ["  $ pytest -q","#8E93A6",22.62,0],
  ["  3 failed, 11 passed","#FF6B6B",22.82,0],
  ["  ✓ Fixed apply_discount() and split_bill()","#3DDC84",23.46,0],
  ["  $ pytest -q","#8E93A6",23.72,0],
  ["  14 passed in 0.01s","#3DDC84",23.9,0],
];
TL.forEach((l,i)=>{const d=document.createElement('div'); d.className='tl'; d.id='tl'+i; d.style.color=l[1]; $('tml').appendChild(d);});
const fmt=n=>n.toLocaleString('en-US');
const c01=x=>Math.max(0,Math.min(1,x));

'''
s = cut(s, '/* =================== BUILD DYNAMIC DOM', '/* captions: chunks', build)

# ---------- SCENE FX ----------
fx = r'''const SCENE_FX = [
  t=>{ // S0 hook
    const o=SC[1]-.15;
    card($('ph0'),t,-1,o); card($('pr0'),t,-1,o);
    $('ph0b').style.width=(c01(t/3.2)*100)+'%';
    $('ph0t').style.transform=`scale(${1+.04*Math.sin(t*3)})`;
    typeText($('pr0t'),t,.25,1.5,"Ek sentence se video banao");
    $('pr0c').style.opacity=Math.floor(t*3.3)%2?1:.15;
    pop($('s0a'),t,1.34,{rot:-5,out:o-.05,from:.4});
    pop($('s0'),t,KICK[0],{rot:6,out:o-.05,from:.4});
  },
  t=>{ // S1 video page
    const o=SC[2]-.15;
    card($('v1'),t,SC[1]-.05,o);
    const TXT="Ek reel banao: SparrowCodes kya hai, 30 second mein.";
    typeText($('v1t'),t,4.6,1.4,TXT);
    $('v1ph').style.display=t>4.6?'none':'inline'; $('v1c').style.opacity=(t>4.5&&t<6.2)?(Math.floor(t*3.3)%2?1:.15):0;
    const f=t>=6.6; st($('v1f'),{borderColor:f?'#7C7FF2':'#2B3040',background:f?'#1B1D3A':'#12141C',transform:`scale(${1+.08*Math.max(0,1-Math.abs(t-6.66)/.14)})`});
    const b=t>=7.2; st($('v1b'),{transform:`scale(${1-.06*Math.max(0,1-Math.abs(t-7.2)/.1)})`,background:b?'#5E61C9':'#7C7FF2'});
    const pp=c01((t-7.3)/1.1); $('v1p').style.opacity=P(t,7.25,.15); $('v1ff').style.opacity=P(t,7.3,.15)*(1-P(t,8.4,.1));
    $('v1pb').style.width=(eio(pp)*100)+'%'; $('v1n').textContent=Math.round(eio(pp)*100)+'%';
    $('v1s').textContent=pp<.3?'Planning scenes and copy':pp<.55?'Checking layout and motion':pp<.8?'Recording the voiceover':pp<1?'Rendering the video':'Your video is ready';
    pop($('ok1'),t,KICK[1],{d:.28,from:.4,out:o});
  },
  t=>{ // S2 three free videos + mark
    const o=SC[3]-.15;
    TX2.forEach((x,i)=>{ pop($('t2'+i),t,SC[2]+.12+i*.14,{d:.34,from:.5,dy:40,out:o+i*.02}); pop($('t2f'+i),t,9.84+i*.14,{d:.24,from:.3,out:o}); });
    const r=P(t,10.98,.3); st($('ring2'),{opacity:r*(1-P(t,o,.15)),transform:`scale(${lerp(1.6,1,eo(r))}) rotate(${t*40}deg)`});
    pop($('mk2'),t,11.76,{d:.32,from:.4,dy:-60,out:o}); st($('lab2'),{opacity:P(t,11.9,.2)*(1-P(t,o,.15))});
    pop($('s2'),t,KICK[2],{rot:5,out:o,from:.4});
  },
  t=>{ // S3 speech
    const o=SC[4]-.15;
    card($('sp'),t,SC[3]-.05,o);
    const pl=c01((t-13.0)/5.6); $('sppb').style.width=(pl*100)+'%'; $('sptm').textContent=`0:${String(Math.floor(pl*62)).padStart(2,'0')} / 1:02`;
    $('spnum').textContent=fmt(Math.round(eo(P(t,13.86,1.0))*10000));
    pop($('spfree'),t,15.02,{d:.24,from:.3});
    pop($('splang'),t,15.72,{d:.3,from:.5});
    const c=P(t,17.06,.3); st($('spcl'),{opacity:c,transform:`translateY(${(1-eo(c))*24}px)`});
    for(let i=0;i<22;i++){ $('wv'+i).style.height=(10+38*Math.abs(Math.sin(t*7+i*.9)*Math.sin(i*.37+t*2.1))*c)+'px'; }
    pop($('spvc'),t,17.8,{d:.26,from:.3});
    pop($('s3'),t,KICK[3]+.1,{rot:5,out:o,from:.4});
  },
  t=>{ // S4 terminal
    const o=SC[5]-.15;
    card($('tm'),t,SC[4]-.05,o);
    TL.forEach((l,i)=>{const el=$('tl'+i); const on=t>=l[2]; el.style.opacity=on?1:0;
      if(l[3]){ el.textContent=l[0].slice(0,Math.max(1,Math.floor(c01((t-l[2])/l[3])*l[0].length))); }
      else { el.textContent=l[0]; el.style.transform=`translateX(${(1-eo(P(t,l[2],.18)))*-16}px)`; } });
    pop($('ok4'),t,KICK[4],{d:.28,from:.4,out:o});
    pop($('s4'),t,23.5,{rot:-5,out:o,from:.4});
  },
  t=>{ // S5 + S6 pricing card (stays through both scenes, leaves behind the wipe)
    card($('pc'),t,SC[5]-.05);
    const pk=P(t,25.9,.32); st($('pcp'),{opacity:c01(pk*3),transform:`scale(${lerp(.4,1,back(pk))})`});
    $('pcd').style.opacity=P(t,26.42,.2);
    [[27.28,'pr1'],[28.46,'pr2'],[29.44,'pr3']].forEach(([a,id])=>{const k=eo(P(t,a,.28)); st($(id),{opacity:k,transform:`translateX(${(1-k)*-28}px)`});});
    pop($('s5'),t,29.9,{rot:5,out:SC[6]-.15,from:.4});
    $('pcn').style.opacity=P(t,31.2,.25);
    pop($('s6'),t,KICK[6],{rot:-6,from:1.9,d:.26});
    pop($('upi'),t,33.05,{d:.28,from:.4});
    const inr=t>=33.75; st($('curI'),{background:inr?'#7C7FF2':'transparent',color:inr?'#fff':'#8E93A6'}); st($('curU'),{background:inr?'transparent':'#2B3040',color:inr?'#8E93A6':'#fff'});
  },
  t=>{},
  t=>{ // S7 comment to DM (after the wipe peak only)
    const on=t>=SC[7];
    st($('cbox'),{opacity:on?1:0,transform:`translateY(${on?lerp(40,0,eo(P(t,SC[7],.35))):0}px)`});
    pop($('s7'),t,35.84,{rot:-5,from:.4});
    const W="SPARROW", tA=36.82; const n=Math.floor(c01((t-tA)/.5)*W.length); const posted=t>=37.75;
    $('ftxt').textContent=posted?'':W.slice(0,n); $('fph').style.display=(n>0&&!posted)?'none':'inline';
    $('posted').style.height=(eo(P(t,37.75,.25))*104)+'px';
    $('post').style.opacity=(n>=W.length&&!posted)?1:.35;
    const foc=t>=36.7&&!posted; $('field').style.borderColor=foc?'#3897F0':'#E6E1D8'; $('field').style.boxShadow=foc?'0 0 0 5px rgba(56,151,240,.15)':'none';
    pop($('dm'),t,38.2,{d:.34,dy:60,from:.7});
    pop($('sent'),t,KICK[8],{d:.26,from:.4,rot:3});
  },
];

'''
s = cut(s, 'const SCENE_FX = [', '/* =================== DRAWING (keep)', fx)
old = "['card1','ok1','s1'].forEach(id=>$(id).style.opacity=0)"
assert old in s
s = s.replace(old, "['pc','s5','s6','upi'].forEach(id=>$(id).style.opacity=0)")
open(p, 'w', encoding='utf-8').write(s)

d = json.load(open('project.json', encoding='utf-8'))
d['duration'] = 40.5
d['status'] = 'build'
json.dump(d, open('project.json', 'w', encoding='utf-8'), indent=1)
print('built', len(s))
