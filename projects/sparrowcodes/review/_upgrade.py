"""One-off v3 visual/motion upgrade of src/reel.html (run once on the v2 source)."""
import io, sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
assert 'id="aura"' not in s, "already upgraded"


def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, f"anchor missing: {old[:70]!r}"
    if count:
        assert s.count(old) == count, f"anchor count {s.count(old)} != {count}: {old[:70]!r}"
    s = s.replace(old, new)


# ---------- CSS ----------
rep("/* wipe canvas */", r"""/* ===== v3 upgrades ===== */
.sc{background:linear-gradient(180deg,#181B29 0%,#0F1117 42%,#0B0D12 100%);overflow:hidden}
.sheen{position:absolute;top:-20%;left:0;width:200px;height:140%;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.14),rgba(255,255,255,0));opacity:0;pointer-events:none}
.vid .bl{position:absolute;left:-30%;top:-5%;width:160%;height:60%;border-radius:50%;background:radial-gradient(circle,rgba(255,130,230,.5),rgba(255,130,230,0) 62%);pointer-events:none}
.vid .vc{position:absolute;left:0;right:0;text-align:center;font:800 19px var(--sans);color:#141414}
.vid .vc b{background:#fff;border-radius:8px;padding:5px 12px}
#dock{left:0;width:1080px;top:1452px;display:flex;justify-content:center;gap:14px;opacity:0}
.dk{display:flex;align-items:center;gap:10px;height:64px;padding:0 20px 0 12px;border-radius:999px;background:rgba(255,255,255,.78);border:2px solid var(--line);font:700 23px var(--mono);letter-spacing:1px;color:#A49E93;box-shadow:0 8px 20px rgba(0,0,0,.05)}
.dk em{width:38px;height:38px;border-radius:50%;border:2px solid #DDD6CB;background:#fff;display:flex;align-items:center;justify-content:center;font-style:normal}
#rip{left:0;top:0;width:90px;height:90px;border-radius:50%;border:5px solid #7C7FF2;opacity:0;pointer-events:none;z-index:49}
#fxc{position:absolute;inset:0;pointer-events:none}
#fs{left:150px;top:850px;width:780px;padding:14px 36px;opacity:0}
.sk{height:18px;border-radius:9px;background:#ECE8E1}
#tst{position:absolute;left:0;right:0;bottom:0;height:54px;background:#161922;display:flex;align-items:center;padding:0 26px;gap:14px;font:600 21px var(--mono);color:#8E93A6}

/* wipe canvas */""")
rep(".tl{font:500 26px var(--mono)", ".tl{font:500 27px var(--mono)")

# ---------- HTML ----------
rep('<div id="world">\n', '<div id="world">\n  <div class="glow" id="aura" data-qa-ignore style="left:90px;top:400px;width:900px;height:820px;background:#8E84FF;opacity:0"></div>\n')
rep('<div class="vt" id="ph0t" style="top:200px">Code to Video</div>',
    '<div class="bl" id="ph0bl"></div><div class="vt" id="ph0t" style="top:190px">Code to Video</div><div class="vc" style="top:262px"><b id="ph0cw">Sentence</b></div>')
rep('style="left:150px;top:520px;width:780px;height:616px;padding:30px 34px">\n',
    'style="left:150px;top:520px;width:780px;height:616px;padding:30px 34px"><div class="sheen" id="sh1"></div>\n')
rep('VIDEO READY</div>\n',
    'VIDEO READY</div>\n  <div class="abs vid" id="v1r" style="left:704px;top:824px;width:186px;height:331px"><div class="bl"></div><div class="vt" style="top:126px;font-size:23px">SparrowCodes</div><div class="bar"><b style="width:38%"></b></div><div class="wm">SPARROWCODES</div></div>\n')
rep('style="left:150px;top:520px;width:780px;height:610px;padding:30px 36px">\n',
    'style="left:150px;top:520px;width:780px;height:610px;padding:30px 36px"><div class="sheen" id="sh3"></div>\n')
rep('    <div style="padding:22px 32px" id="tml"></div>\n',
    '    <div style="padding:22px 32px" id="tml"></div>\n    <div id="tst"><i id="tsd" style="width:13px;height:13px;border-radius:50%;background:#FEBC2E"></i><span id="tstx">waiting for prompt</span></div>\n    <div class="sheen" id="sh4"></div>\n')
rep('padding:34px 40px;border-color:#7C7FF2">\n', 'padding:34px 40px;border-color:#7C7FF2"><div class="sheen" id="sh5"></div>\n')
rep('    <div class="crow"><div class="uav"></div><div id="field">',
    '    <div class="crow" id="skrow" style="height:62px;overflow:hidden"><div class="uav"></div><div style="flex:1"><div class="sk" style="width:36%"></div><div class="sk" style="width:70%;margin-top:12px"></div></div></div>\n'
    '    <div class="crow"><div class="uav"></div><div id="field">')
rep('  <div class="abs" id="dm">',
    '  <div class="abs card" id="fs">\n'
    '    <div class="step"><span class="num">1</span>3 videos free<span class="ck" id="fk0"></span></div>\n'
    '    <div class="step"><span class="num">2</span>Roz 10,000 characters voiceover<span class="ck" id="fk1"></span></div>\n'
    '    <div class="step"><span class="num">3</span>Card nahi chahiye<span class="ck" id="fk2"></span></div>\n'
    '  </div>\n'
    '  <div class="abs" id="dm">')
rep('<canvas id="wipe" width="1080" height="1920" data-qa-ignore></canvas>',
    '<canvas id="fxc" width="1080" height="1920" data-qa-ignore></canvas>\n<canvas id="wipe" width="1080" height="1920" data-qa-ignore></canvas>')
rep('<!-- captions -->',
    '<!-- feature tracker -->\n<div class="abs" id="dock" data-qa-ignore>'
    + ''.join(f'<div class="dk" id="dk{i}"><em id="dke{i}"></em><span>{n}</span></div>' for i, n in enumerate(["VIDEO", "VOICE", "AGENT", "$10 PLAN"]))
    + '</div>\n\n<!-- captions -->')
rep('<!-- cursor -->', '<!-- cursor -->\n<div class="abs" id="rip" data-qa-ignore></div>')

# ---------- CONFIG ----------
rep("[35.9, 980, 1000], [36.7, 470, 668, 1], [37.75, 858, 662, 1], [38.4, 858, 662], null,",
    "[35.9, 980, 1000], [36.7, 470, 750, 1], [37.75, 858, 744, 1], [38.4, 858, 744], null,")
rep("Auto-renew|rupees|Comment|DM)", "Auto-renew|rupees|UPI|Comment|DM)")

# ---------- HELPERS ----------
rep("""function card(el,t,a,b=1e9,{dy=60}={}){
  const pi=a<=0?1:P(t,a,.36), po=P(t,b,.32);
  st(el,{opacity:clamp(pi*2)*(1-eo(po)),transform:`translateY(${lerp(dy,0,eo(pi))-220*eio(po)}px) scale(${lerp(.82,1,back(pi))*lerp(1,.7,eio(po))})`});
}""", """function card(el,t,a,b=1e9,{dy=70,fl=6,ph=0}={}){
  const pi=a<=0?1:P(t,a,.44), po=P(t,b,.32);
  const f=fl*Math.sin(t*1.25+ph)*eo(pi)*(1-po);
  st(el,{opacity:clamp(pi*2)*(1-eo(po)),transform:`perspective(1500px) translateY(${lerp(dy,0,eo(pi))-220*eio(po)+f}px) rotateX(${lerp(18,0,eo(pi))-12*eio(po)}deg) scale(${lerp(.82,1,back(pi))*lerp(1,.7,eio(po))})`});
}
// light sweep across a card: starts at each time in ts
function sheen(id,t,ts,w){ let k=0; for(const a of ts){const x=P(t,a,.8); if(x>0&&x<1) k=x;}
  st($(id),{opacity:k>0?1:0,transform:`translateX(${lerp(-260,w+60,eio(k))}px) skewX(-18deg)`}); }""")
rep("""function head(el,t,a,b){
  const pi = a<=0?1:P(t,a,.34), po=P(t,b,.22);
  st(el,{opacity:eo(pi)*(1-po),transform:`translateY(${lerp(50,0,eo(pi))-60*eo(po)}px)`});
}""", """function head(el,t,a,b){
  const po=P(t,b,.22), ls=el.children;
  for(let i=0;i<ls.length;i++){ const pi=a<=0?1:P(t,a+i*.1,.38);
    st(ls[i],{opacity:eo(pi),transform:`translateY(${lerp(70,0,eo(pi))}px) scale(${lerp(.92,1,back(pi))})`,filter:pi<1?`blur(${(1-eo(pi))*10}px)`:'none'}); }
  st(el,{opacity:(t>=a-.001?1:0)*(1-po),transform:`translateY(${-14*eo(po)}px) scale(${lerp(1,.95,eo(po))})`,filter:po>0?`blur(${po*8}px)`:'none'});
}""")

# ---------- DYNAMIC DOM ----------
rep('d.innerHTML=`<div class="vt" style="top:160px;font-size:27px">', 'd.innerHTML=`<div class="bl" id="t2b${i}"></div><div class="vt" style="top:160px;font-size:27px">')
rep("""const chunks=[]; {let cur=[];
  WORDS.forEach((w,i)=>{cur.push(w); const nx=WORDS[i+1];""", """const CW=[]; for(let i=0;i<WORDS.length;i++){ const w=WORDS[i], b=WORDS[i+1], c=WORDS[i+2];
  if(w.w==='U'&&b&&b.w==='P'&&c&&c.w==='I'){ CW.push(Object.assign({},w,{w:'UPI',e:c.e})); i+=2; } else CW.push(w); }
const chunks=[]; {let cur=[];
  CW.forEach((w,i)=>{cur.push(w); const nx=CW[i+1];""")

# ---------- SCENE FX ----------
# S0
rep("""    typeText($('pr0t'),t,.25,1.5,"Ek sentence se video banao");""",
    """    typeText($('pr0t'),t,.25,1.5,"Ek sentence se video banao");
    $('ph0bl').style.transform=`translate(${Math.sin(t*1.1)*40}px,${Math.cos(t*.9)*60+40}px)`;
    $('ph0cw').textContent=["Sentence","Scenes","Voiceover","Video"][Math.floor(t*1.6)%4];""")
# S1
rep("card($('v1'),t,SC[1]-.05,o);", "card($('v1'),t,SC[1]-.05,o,{fl:0}); sheen('sh1',t,[7.22],780);")
rep("const pp=c01((t-7.3)/1.1);", "const pp=c01((t-7.3)/.8);")
rep("(1-P(t,8.4,.1));", "(1-P(t,8.1,.1));")
rep("    pop($('ok1'),t,KICK[1],{d:.28,from:.4,out:o});",
    "    pop($('ok1'),t,KICK[1],{d:.28,from:.4,out:o});\n    pop($('v1r'),t,8.14,{d:.36,from:.3,dy:60,rot:5,out:o});")
# S2
rep("pop($('t2f'+i),t,9.84+i*.14,{d:.24,from:.3,out:o}); });",
    "pop($('t2f'+i),t,9.84+i*.14,{d:.24,from:.3,out:o});\n      $('t2b'+i).style.transform=`translate(${Math.sin(t*1.2+i*2)*30}px,${Math.cos(t+i)*50+30}px)`; });")
# S3
rep("card($('sp'),t,SC[3]-.05,o);", "card($('sp'),t,SC[3]-.05,o,{ph:1}); sheen('sh3',t,[14.86],780);")
rep("    pop($('spfree'),t,15.02,{d:.24,from:.3});",
    "    { const nb=Math.max(0,1-Math.abs(t-14.9)/.2), gl=P(t,14.5,.4); st($('spnum'),{display:'inline-block',transformOrigin:'left bottom',transform:`scale(${1+.07*nb})`,textShadow:`0 0 ${34*gl}px rgba(139,142,255,${.6*gl})`}); }\n"
    "    pop($('spfree'),t,15.02,{d:.24,from:.3});")
# S4
rep("card($('tm'),t,SC[4]-.05,o);", "card($('tm'),t,SC[4]-.05,o,{ph:2}); sheen('sh4',t,[23.9],820);")
rep("""    TL.forEach((l,i)=>{const el=$('tl'+i); const on=t>=l[2]; el.style.opacity=on?1:0;
      if(l[3]){ el.textContent=l[0].slice(0,Math.max(1,Math.floor(c01((t-l[2])/l[3])*l[0].length))); }""",
    """    const blk=Math.floor(t*3.3)%2?'\\u2588':' ';
    TL.forEach((l,i)=>{const el=$('tl'+i); const on=i===0?t>=SC[4]+.3:t>=l[2]; el.style.opacity=on?1:0;
      if(l[3]){ const nx=TL[i+1][2], n=t<l[2]?2:Math.max(2,Math.floor(c01((t-l[2])/l[3])*l[0].length));
        el.textContent=l[0].slice(0,n)+(t<nx?blk:''); }""")
rep("    pop($('ok4'),t,KICK[4],{d:.28,from:.4,out:o});",
    "    { const dn=t>=23.9, wk=t>=21.0; $('tstx').textContent=dn?'done \\u00b7 14 passed':wk?'agent working'+'.'.repeat(1+Math.floor(t*4)%3):'waiting for prompt';\n"
    "      $('tsd').style.background=dn?'#28C840':'#FEBC2E'; $('tsd').style.opacity=dn?1:(.45+.55*Math.abs(Math.sin(t*5)));\n"
    "      st($('tl7'),{background:`rgba(61,220,132,${.2*P(t,23.9,.15)})`,borderRadius:'8px'}); }\n"
    "    pop($('ok4'),t,KICK[4],{d:.28,from:.4,out:o});")
# S5
rep("card($('pc'),t,SC[5]-.05);",
    "card($('pc'),t,SC[5]-.05,1e9,{ph:3}); sheen('sh5',t,[25.9,31.74],740);\n"
    "    $('pc').style.boxShadow=`0 30px 70px rgba(10,12,30,.30), 0 0 ${46+22*Math.sin(t*2.2)}px rgba(124,127,242,${.30+.12*Math.sin(t*2.2)})`;")
# S7
rep("    pop($('s7'),t,35.84,{rot:-5,from:.4});",
    "    pop($('s7'),t,35.84,{rot:-5,from:.4});\n"
    "    pop($('fs'),on?t:-1,35.0,{d:.36,dy:50,from:.8,out:38.0,od:.18}); check($('fk0'),t,35.1); check($('fk1'),t,35.45); check($('fk2'),t,35.84);\n"
    "    { const kq=eo(P(t,37.75,.25)); st($('skrow'),{height:(62*(1-kq))+'px',marginTop:(20*(1-kq))+'px',opacity:1-kq}); }")

# ---------- DRAWING ----------
rep("function cursorAt(t){\n  const c=$('cursor'); const m=(x,y)=>[540+(x-540)*window.WS, 700+(y-700)*window.WS];",
    """const fctx=$('fxc').getContext('2d'); const PAL=['#D97757','#22A35A','#7C7FF2','#FFB84D','#141414'];
const BURSTS=[[2.36,790,850],[8.46,800,520],[15.12,770,500],[23.5,790,505],[25.9,300,770],[31.74,740,715],[38.55,770,845]];
function drawFx(t){
  fctx.clearRect(0,0,1080,1920);
  for(const [a,x0,y0] of BURSTS){ const k=(t-a)/.75; if(k<=0||k>=1) continue;
    const cx=540+(x0-540)*window.WS, cy=700+(y0-700)*window.WS;
    for(let i=0;i<16;i++){ const ang=i/16*Math.PI*2+a*1.7+Math.sin(i*12.9898)*.35, sp=150+110*Math.abs(Math.sin(i*78.233+a));
      const r=sp*eo(k), x=cx+Math.cos(ang)*r, y=cy+Math.sin(ang)*r+140*k*k;
      fctx.save(); fctx.translate(x,y); fctx.rotate(ang+k*5*(i%2?1:-1)); fctx.globalAlpha=1-k*k; fctx.fillStyle=PAL[i%5];
      const w=(i%3?18:11)*(1-.4*k), h=(i%3?8:11)*(1-.4*k);
      if(i%3===2){fctx.beginPath();fctx.arc(0,0,w*.5,0,6.283);fctx.fill();} else fctx.fillRect(-w/2,-h/2,w,h);
      fctx.restore(); } }
}
const DK_T=[8.46,15.02,23.9,29.9], DK_S=[[1,2],[3,3],[4,4],[5,6]];
const DK_CK=`<svg width="24" height="24" viewBox="0 0 24 24"><path d="M6 12.5l4 4L18 8" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
function dockAt(t,si){
  const o=P(t,SC[1]+.2,.3)*(1-P(t,SC[7]-.5,.2));
  st($('dock'),{opacity:o,transform:`translateY(${(1-eo(P(t,SC[1]+.2,.3)))*30}px)`});
  for(let i=0;i<4;i++){ const dn=t>=DK_T[i], ac=si>=DK_S[i][0]&&si<=DK_S[i][1], k=P(t,DK_T[i],.28), e=$('dke'+i);
    st($('dk'+i),{borderColor:ac?'#D97757':'#E4DED3',color:(dn||ac)?'#141414':'#A49E93',transform:`scale(${1+.1*Math.sin(Math.PI*k)*(k<1?1:0)})`});
    st(e,{background:dn?'#22A35A':'#fff',borderColor:dn?'#22A35A':(ac?'#D97757':'#DDD6CB'),transform:`scale(${dn?back(k):1})`}); e.innerHTML=dn?DK_CK:''; }
}
function cursorAt(t){
  const c=$('cursor'); const m=(x,y)=>[540+(x-540)*window.WS, 700+(y-700)*window.WS];
  { let ro=0,rx=0,ry=0,rs=1; for(const p of CURSOR) if(p&&p[3]){ const k=(t-p[0])/.45; if(k>0&&k<1){ [rx,ry]=m(p[1],p[2]); ro=(1-k)*.9; rs=.3+1.3*eo(k); } }
    st($('rip'),{opacity:ro,transform:`translate(${rx-45}px,${ry-45}px) scale(${rs})`}); }""")

# ---------- MAIN RENDER ----------
rep("  window.WS=push; $('world').style.transform=`scale(${push})`;",
    "  window.WS=push; $('world').style.transform=`scale(${push})`;\n"
    "  { const AU=[.2,.34,.16,.34,.34,.38,.38,0]; const au=lerp(si?AU[si-1]:AU[0],AU[si],eio(clamp(local/.4)));\n"
    "    st($('aura'),{opacity:au*(.85+.15*Math.sin(t*1.7)),transform:`translate(${Math.sin(t*.5)*40}px,${Math.cos(t*.43)*30}px)`}); }")
rep("if(WIPE && t>=WIPE.m) ['pc','s5','s6','upi'].forEach(id=>$(id).style.opacity=0);\n  cursorAt(t);",
    "if(WIPE && t>=WIPE.m) ['pc','s5','s6','upi'].forEach(id=>$(id).style.opacity=0);\n  cursorAt(t); dockAt(t,si); drawFx(t);")

p.write_text(s, encoding="utf-8", newline="\n")
print("upgraded", len(s))
