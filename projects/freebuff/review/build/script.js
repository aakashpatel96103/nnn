//@@CONFIG
/* =================== CONFIG (edit per reel) =================== */
const DUR = __DUR__;
const WORDS = __WORDS__;
const HANDLE = "@mukku.tech";
const SC = [0, 3.38, 5.78, 10.06, 15.24, 19.66];
const CRUMBS = ["// 01 — SAB PAGAL","// 02 — FREE MEIN","// 03 — REAL PROOF","// 04 — ALTERNATIVE","// 05 — SAB EK JAGAH","// 06 — COMMENT “ALTERNATIVE”"];
const HL_T = [2.38, 4.24, 8.36, 11.40, 18.22, 21.54];
const KICK = [2.38, 4.24, 8.0, 11.44, 14.14, 18.22, 22.6, 23.82];
const WIPE = {a: SC[5]-.34, m: SC[5], b: SC[5]+.34};
const KEYW = /^["“]?(free|Claude|pagal|reels?|software|alternative|interesting|comment|link|DM)["”]?[,!.?]*$/i;
const END_T = 24.3;
const CURSOR = [
  [20.7, 980, 1000], [21.4, 470, 750, 1], [22.0, 600, 800], [22.6, 858, 744, 1], [23.1, 858, 744], null,
];

//@@BUILD
/* =================== BUILD DYNAMIC DOM (per reel) =================== */
$('hname').textContent=HANDLE;
const c01=x=>Math.max(0,Math.min(1,x));
const fmt=n=>n.toLocaleString('en-US');
// S2 footage: pre-extracted frames (name-safe crops), drawn to canvas = pure function of t
const NF=270, FP=new Array(NF), FSH=new Array(NF), FAH=24, FBH=6;
function fsLoad(i){ if(i<0||i>=NF||FP[i]) return; const n=String(i+1).padStart(4,'0');
  const a=new Image(); a.src='../assets/prev60/'+n+'.jpg'; FP[i]=a;
  const b=new Image(); b.src='../assets/shell60/'+n+'.jpg'; FSH[i]=b; }
function fsWin(fi){ const lo=Math.max(0,fi-2), hi=Math.min(NF-1,lo+FAH);
  for(let i=lo;i<=hi;i++) fsLoad(i);
  for(let i=0;i<lo-FBH;i++) if(FP[i]){ FP[i].src=''; FSH[i].src=''; FP[i]=null; FSH[i]=null; } }
fsWin(0);
const cxp=$('cv2p').getContext('2d'), cxs=$('cv2s').getContext('2d');
const K3=`<svg width="34" height="34" viewBox="0 0 24 24"><path d="M6 12.5l4 4L18 8" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
function ck3(id,t,a){ const el=$(id), on=P(t,a,.22); st(el,{background:on>0?'#22A35A':'transparent',borderColor:on>0?'#22A35A':'#3A4052',transform:`scale(${on>0?back(on):1})`}); el.innerHTML=on>0?K3:''; }

//@@FX
/* =================== SCENE FX (per reel): fx(t) for each scene =================== */
const SCENE_FX = [
  t=>{ // S0 hook: everyone asks Claude
    const o=SC[1]-.15;
    card($('c0'),t,-1,o); sheen('sh0',t,[2.38],780);
    [[.30,'b00'],[1.10,'b01'],[1.90,'b02']].forEach(([a,id],i)=>{ const k=P(t,a,.3); st($(id),{opacity:c01(k*3),transform:`translateX(${(1-eo(k))*60}px) scale(${lerp(.8,1,back(k))})`}); });
    $('c0n').textContent=fmt(Math.round(240+eio(c01(t/3.2))*12240));
    $('c0d').textContent='Thinking'+'.'.repeat(1+Math.floor(t*4)%3); $('c0sp').style.transform=`rotate(${Math.floor(t*6)*30}deg) scale(${1+.08*Math.sin(t*9)})`;
    
    pop($('s0'),t,KICK[0],{rot:6,out:o-.05,from:1.8,d:.26});
  },
  t=>{ // S1 me: free
    const o=SC[2]-.15;
    card($('c1'),t,SC[1]-.05,o,{ph:1}); sheen('sh1',t,[4.24],740);
    $('c1').style.boxShadow=`0 30px 70px rgba(10,12,30,.30), 0 0 ${46+22*Math.sin(t*2.2)}px rgba(217,119,87,${.30+.12*Math.sin(t*2.2)})`;
    const pk=P(t,3.62,.34); st($('c1p'),{opacity:c01(pk*3),transform:`scale(${lerp(.4,1,back(pk))*(1+.06*Math.max(0,1-Math.abs(t-4.3)/.2))})`});
    pop($('c1f'),t,4.24,{d:.26,from:.3});
    ['m10','m11','m12'].forEach((id,i)=>pop($(id),t,4.70+i*.16,{d:.32,from:.4,dy:40,rot:[-4,0,4][i]}));
    $('c1c').textContent=String(Math.max(0,Math.min(3,Math.floor((t-4.62)/.16))));
    pop($('s1'),t,KICK[1]+.06,{rot:5,out:o,from:.4});
  },
  t=>{ // S2 real recording (name hidden: crop + blur)
    const o=SC[3]-.15;
    card($('w2'),t,SC[2]-.05,o,{fl:4,ph:2}); sheen('sh2',t,[8.0],820);
    const fi=Math.max(0,Math.min(NF-1,Math.floor((t-5.74)*60)));
    if(t>SC[2]-.3&&t<SC[3]+.3){ fsWin(fi); const A=FSH[fi], B=FP[fi];
      if(A&&A.complete&&A.naturalWidth) cxs.drawImage(A,0,0,1640,692); if(B&&B.complete&&B.naturalWidth) cxp.drawImage(B,0,0,656,1166); }
    pop($('p2'),t,SC[2]+.14,{d:.4,from:.5,dy:80,rot:3,out:o});
    $('p2').style.boxShadow=`0 30px 60px rgba(0,0,0,.34), 0 0 0 ${6*Math.max(0,1-Math.abs(t-8.0)/.3)}px rgba(217,119,87,.9)`;
    $('w2r').style.opacity=Math.floor(t*2.5)%2?1:.25;
    pop($('s2'),t,7.10,{rot:-5,out:o,from:.4});
    pop($('n2'),t,8.64,{d:.32,from:.5,dy:40,out:o});
  },
  t=>{ // S3 compare
    const o=SC[4]-.15;
    card($('c3'),t,SC[3]-.05,o,{ph:3}); sheen('sh3',t,[11.44,14.14],780);
    const h=P(t,11.5,.4); st($('c3hi'),{opacity:P(t,10.5,.3),boxShadow:`0 0 ${40*h+14*Math.sin(t*2.4)*h}px rgba(217,119,87,${.55*h})`});
    [[10.5,'c3r0'],[12.5,'c3r1'],[13.2,'c3r2']].forEach(([a,id])=>{const k=eo(P(t,a,.3)); st($(id),{opacity:k,transform:`translateX(${(1-k)*-30}px)`});});
    pop($('c3f'),t,11.44,{d:.28,from:.3});
    ck3('k30',t,12.72); ck3('k31',t,12.90); ck3('k32',t,13.42); ck3('k33',t,13.60);
    pop($('s3'),t,KICK[4],{rot:-5,out:o,from:.4});
  },
  t=>{ // S4 three in one
    const sq=eio(P(t,18.22,.36));
    [[15.2,'r40',520,548],[16.34,'r41',712,712],[17.12,'r42',904,876]].forEach(([a,id,y0,y1],i)=>{ const k=P(t,a,.4);
      st($(id),{opacity:c01(k*2.5),top:lerp(y0,y1,sq)+'px',transform:`perspective(1500px) translateX(${(1-eo(k))*(i%2?120:-120)}px) rotateY(${(1-eo(k))*(i%2?-22:22)}deg) scale(${lerp(.86,1,back(k))})`,borderColor:sq>0?`rgba(217,119,87,${sq})`:'#262A36'}); });
    ck3('k40',t,15.72); ck3('k41',t,16.62); ck3('k42',t,17.46);
    pop($('j4'),t,18.22,{d:.3,from:.4,dy:-30});
    pop($('s4'),t,18.74,{rot:5,from:.4});
  },
  t=>{ // S5 comment to DM (after the wipe peak only)
    const on=t>=SC[5];
    st($('cbox'),{opacity:on?1:0,transform:`translateY(${on?lerp(40,0,eo(P(t,SC[5],.35))):0}px)`});
    pop($('s5'),t,20.14,{rot:-5,from:.4});
    const TP=22.6;
    { const kq=eo(P(t,TP,.25)); st($('skrow'),{height:(62*(1-kq))+'px',marginTop:(20*(1-kq))+'px',opacity:1-kq}); }
    const W="ALTERNATIVE", tA=21.54; const n=Math.floor(c01((t-tA)/.72)*W.length); const posted=t>=TP;
    $('ftxt').textContent=posted?'':W.slice(0,n); $('fph').style.display=(n>0&&!posted)?'none':'inline';
    $('posted').style.height=(eo(P(t,TP,.25))*104)+'px';
    $('post').style.opacity=(n>=W.length&&!posted)?1:.35;
    const foc=t>=21.4&&!posted; $('field').style.borderColor=foc?'#3897F0':'#E6E1D8'; $('field').style.boxShadow=foc?'0 0 0 5px rgba(56,151,240,.15)':'none';
    pop($('dm'),t,23.2,{d:.34,dy:60,from:.7});
    pop($('sent'),t,KICK[7],{d:.26,from:.4,rot:3});
  },
];

