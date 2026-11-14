const DUR = __DUR__;
const WORDS = __WORDS__;
const $ = id => document.getElementById(id);
const clamp = (x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const P = (t,a,d)=>clamp((t-a)/d);
const eo = x=>1-Math.pow(1-x,3);
const eio = x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back = x=>{const c=1.70158*1.1,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const lerp=(a,b,x)=>a+(b-a)*x;
function st(el,o){for(const k in o) el.style[k]=o[k];}
function pop(el,t,a,{d=.32,out=1e9,od=.22,rot=0,from=.6,dy=0}={}){
  const pi=P(t,a,d), po=P(t,out,od);
  const s = lerp(from,1,back(pi)) * lerp(1,.85,eo(po));
  st(el,{opacity:clamp(pi*3)*(1-eo(po)),transform:`translateY(${lerp(dy,0,eo(pi))-po*30}px) rotate(${rot}deg) scale(${s})`});
}
function head(el,t,a,b,dy0=50){
  const pi = a<=0?1:P(t,a,.34), po=P(t,b,.22);
  st(el,{opacity:eo(pi)*(1-po),transform:`translateY(${lerp(dy0,0,eo(pi))-60*eo(po)}px)`});
}
/* scene windows */
const SC=[0,4.40,8.62,17.08,24.42,29.90,38.10,40.38]; // 8 scenes: 0 hook,1 multi,2 web,3 dev mode,4 3rd party,5 form,6 ready,7 CTA
const HL_AT=[[0,4.30],[4.40,8.50],[8.62,16.96],[17.08,24.32],[24.42,29.78],[29.90,37.98],[38.10,40.30],[40.38,1e9]];
const WIPE={a:39.98,m:40.38,b:40.78};

const MODELS=["Fable 5","Fable 5.1","Fable 5.2","Haiku 5.5","Opus 5.5","Sonnet 5.5"];
const rowsEl=$('rows');
MODELS.forEach((m,i)=>{
  const r=document.createElement('div'); r.className='row'; r.id='r'+i;
  r.innerHTML=`<div class="n">${m}</div><div class="d">Claude ${m} by Anthropic, through the Model API.</div><div class="k" data-qa-ignore>${i+1}</div>`+
   (m==="Opus 5.5"?`<svg style="position:absolute;right:150px;top:26px" width="26" height="26" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#5B9BF0" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`:'')+
   `<div class="free" id="f${i}">FREE</div>`;
  rowsEl.appendChild(r);
});
const spark=c=>`<svg width="42" height="42" viewBox="-32 -32 64 64">${Array.from({length:10},(_,i)=>`<line x1="0" y1="0" x2="0" y2="-26" stroke="${c}" stroke-width="8" stroke-linecap="round" transform="rotate(${i*36+(i%2?8:0)})"/>`).join('')}</svg>`;
$('spk1').innerHTML=spark('#D97757'); $('spk2').innerHTML=spark('#D97757'); $('spk3').innerHTML=spark('#D97757');
const TM=["Opus 5.5","Sonnet 5.5","Haiku 5.5","Fable 5.2"], TX=[28,214,400,586];
const tilesEl=$('mtiles');
TM.forEach((m,i)=>{
  const d=document.createElement('div'); d.className='mt'; d.id='t'+i; d.style.left=TX[i]+'px';
  d.innerHTML=spark('#D97757')+`<div class="tn">${m}</div><div class="st" data-qa-ignore><span class="dot" id="td${i}"></span><span id="tl${i}">IDLE</span></div>`;
  tilesEl.appendChild(d);
});
/* captions */
const chunks=[]; {let cur=[];
  WORDS.forEach((w,i)=>{cur.push(w); const nx=WORDS[i+1];
    const brk=!nx || /[,!?]$/.test(w.w) || cur.length>=4 || (nx.s-w.e)>.22 || nx.line!==w.line;
    if(brk){chunks.push(cur);cur=[];}});
}
const KEYW=/FREE|API|key|DM|link|ready|Setup/i;

/* wipe */
const wctx=$('wipe').getContext('2d');
function drawWipe(t){
  wctx.clearRect(0,0,1080,1920);
  const a=WIPE.a,m=WIPE.m,b=WIPE.b; if(t<a||t>b) return;
  const S=96,R=70; wctx.fillStyle='#D97757';
  for(let y=-S/2;y<1920+S;y+=S) for(let x=-S/2;x<1080+S;x+=S){
    const d=(x/1080*.45+(1920-y)/1920*.55); let k;
    if(t<=m){const p=(t-a)/(m-a); k=clamp((p*1.5-d)/.5);} else {const p=(t-m)/(b-m); k=1-clamp((p*1.5-d)/.5);}
    if(k<=0) continue; wctx.beginPath(); wctx.arc(x,y,R*eio(k),0,Math.PI*2); wctx.fill();
  }
}

window.render=function(t){
  st($('g1'),{left:(-120+Math.sin(t*.35)*60)+'px',top:(1150+Math.cos(t*.3)*40)+'px'});
  st($('g2'),{left:(560+Math.cos(t*.4)*50)+'px',top:(1250+Math.sin(t*.33)*50)+'px'});
  let si=0; for(let i=0;i<SC.length;i++) if(t>=SC[i]) si=i;
  const local=t-SC[si];
  const pv=x=>0.03*eo(clamp(x/4.5));
  const prevEnd=si>0?pv(SC[si]-SC[si-1]):0;
  let push=1.04+lerp(prevEnd,pv(local),si>0?eio(clamp(local/.35)):1);
  const KICK=[1.16,3.58,5.26,7.32,10.30,11.52,13.06,14.70,15.98,19.36,20.12,20.94,23.50,26.36,28.56,30.54,35.28,37.04,39.48,41.98,42.62,44.12];
  let kick=0; for(const a of KICK){const x=(t-a)/.4; if(x>0&&x<1) kick+=Math.sin(Math.PI*x)*(1-x)*0.05;}
  push+=kick; window.WS=push;
  $('world').style.transform=`scale(${push})`;

  const crumbs=["// 01 — CLAUDE · FREE","// 02 — MULTIPLE MODELS","// 03 — WEBSITE + KEY","// 04 — DEVELOPER MODE","// 05 — 3RD-PARTY","// 06 — PASTE KEY","// 07 — READY","// 08 — COMMENT"];
  const cN=["01","02","03","04","05","06","07","08"];
  $('crumb').textContent=crumbs[si]; $('count').textContent=`${cN[si]} / 08`;
  $('pfill').style.width=(clamp(t/DUR)*100)+'%';

  HL_AT.forEach((w,i)=>head($('h'+i),t,w[0],w[1]));
  const hlS=[[1.16],[5.26],[11.52],[22.76],[28.56],[33.76],[39.48],[42.38]];
  hlS.forEach((at,i)=>{ const el=$('hl'+i); if(el) el.style.setProperty('--s',eo(P(t,at[0],.3))); });

  /* --- S0 picker --- */
  const pi0=P(t,.30,.55), po0=P(t,4.30,.32);
  st($('picker'),{opacity:clamp(pi0*1.6)*(1-eo(po0)),transform:`translateY(${lerp(90,0,eo(pi0))-160*eio(po0)}px) scale(${lerp(.94,1,back(pi0))})`});
  st($('plabel'),{opacity:1-P(t,4.28,.2)});
  MODELS.forEach((m,i)=>{
    const r=$('r'+i);
    const hov=(t>1.0&&t<4.3)?clamp(1-Math.abs(hoverRow(t)-i)):0;
    r.style.background=`rgba(255,255,255,${0.09*hov})`;
    pop($('f'+i),t,1.16+i*.05,{d:.26,from:.3});
  });
  pop($('s0'),t,3.58,{rot:-5,out:4.30,from:.4});

  /* --- S1 chat --- */
  const in1=P(t,4.45,.42), out1=P(t,8.50,.32);
  st($('chat'),{opacity:clamp(in1*1.6)*(1-eo(out1)),transform:`translateY(${lerp(80,0,eo(in1))-220*eio(out1)}px) scale(${lerp(.9,1,back(in1))})`});
  const CYC=[["Opus 5.5",5.26],["Sonnet 5.5",5.90],["Haiku 5.5",6.52],["Fable 5.2",7.12]];
  let cur=CYC[0][0]; CYC.forEach(c=>{if(t>=c[1])cur=c[0];});
  $('chipT').textContent=cur; $('repT').textContent=`Main ${cur} hoon.`;
  const cycK=P(t,5.26,.2)*0; // reserved
  $('chip').style.transform=`scale(${1-0.08*Math.max(...CYC.map(c=>Math.max(0,1-Math.abs(t-c[1])/.16)))})`;
  TM.forEach((m,i)=>{
    const a=6.85+i*.12; const dr=eo(P(t,a,.36));
    const on=t>=7.05+i*.14;
    const tile=$('t'+i);
    pop(tile,t,5.62+i*.10,{d:.3,from:.6,dy:24});
    tile.style.borderColor=on?'#D97757':'#3a3a38';
    $('td'+i).style.background=on?'#22A35A':'#555';
    $('tl'+i).textContent=on?'FREE':'IDLE'; $('tl'+i).style.color=on?'#22A35A':'#888';
    tile.style.opacity=dr;
  });
  pop($('s1'),t,7.32,{rot:4,out:8.42,from:.4});

  /* --- S2 browser --- */
  const in2=P(t,8.66,.42), out2=P(t,16.96,.30);
  st($('brow'),{opacity:clamp(in2*1.6)*(1-eo(out2)),transform:`translateY(${lerp(80,0,eo(in2))-200*eio(out2)}px) scale(${lerp(.92,1,back(in2))})`});
  const sw=P(t,9.62,.34);
  st($('pgA'),{opacity:1-eo(sw)}); st($('pgB'),{opacity:eo(sw)});
  pop($('s2'),t,10.30,{rot:-4,out:11.30,from:.4});
  pop($('sgn'),t,1e9,{from:.4});
  const ki=P(t,12.86,.36), ko=P(t,16.96,.28);
  st($('keyc'),{opacity:clamp(ki*1.7)*(1-eo(ko)),transform:`translateY(${lerp(70,0,eo(ki))-180*eio(ko)}px) scale(${lerp(.9,1,back(ki))})`});
  const K1="sk-cr••••••••••••7f2a", K2="https://api.████████.ai/v1";
  const n1=Math.floor(clamp((t-13.22)/.62)*K1.length), n2=Math.floor(clamp((t-15.30)/.55)*K2.length);
  $('k1').textContent=K1.slice(0,n1); $('k2').textContent=K2.slice(0,n2);
  const copied1=t>=14.70, copied2=t>=15.98;
  $('c1').textContent=copied1?'Copied':'Copy'; $('c1').style.background=copied1?'#22A35A':'#3a3a38';
  $('c2').textContent=copied2?'Copied':'Copy'; $('c2').style.background=copied2?'#22A35A':'#3a3a38';

  /* --- S3/S4 desktop menu --- */
  const in3=P(t,17.12,.42), out3=P(t,29.78,.30);
  st($('desk'),{opacity:clamp(in3*1.6)*(1-eo(out3)),transform:`translateY(${lerp(80,0,eo(in3))-200*eio(out3)}px) scale(${lerp(.92,1,back(in3))})`});
  const mi=P(t,18.70,.3);
  st($('menu'),{opacity:eo(mi)*(1-P(t,24.30,.22)),transform:`translateY(${lerp(-16,0,eo(mi))}px) scale(${lerp(.96,1,back(mi))})`});
  const LV=[[0,18.70,19.30],[1,19.42,20.06],[2,20.16,22.30]];
  const lv = (t>=20.16&&t<24.3)?2:(t>=19.42&&t<20.16)?1:(t>=18.70&&t<19.42)?0:-1;
  ['ml0','ml1','ml2','ml3','ml4'].forEach((id,i)=>{$(id).style.display=(i===lv)?'block':'none';});
  $('mpath').textContent=['HELP','HELP › TROUBLESHOOTING','HELP › TROUBLESHOOTING','MENU','DEVELOPER'][Math.max(lv,0)];
  const hl3=P(t,20.06,.25), hl2=P(t,19.30,.25);
  $('mi3').style.background=hl3>0&&hl3<1?'rgba(255,255,255,.12)':'transparent';
  $('mt').style.background=hl2>0&&hl2<1?'rgba(255,255,255,.12)':'transparent';
  const onTog=t>=23.50;
  $('tg').style.background=onTog?'#22A35A':'#555';
  $('tgk').style.left=onTog?'34px':'4px';
  pop($('s5'),t,37.04,{rot:3,from:.4});
  /* restart overlay + menu returns with Developer entry */
  const inR=P(t,24.42,.3), outR=P(t,25.20,.3);
  st($('rst'),{opacity:eo(inR)*(1-eo(outR))});
  $('rsp').style.transform=`rotate(${(t-24.42)*360*1.6}deg)`;
  const lvB=(t>=26.14&&t<28.40)?3:(t>=28.40&&t<29.80)?4:-1;
  ['ml0','ml1','ml2','ml3','ml4'].forEach((id,i)=>{ if(t>=25.3) $(id).style.display=(i===lvB)?'block':'none'; });
  if(t>=25.3) $('mpath').textContent=lvB===4?'DEVELOPER':'MENU';
  const hl4=P(t,26.14,.25), hl5=P(t,28.40,.25);
  $('md').style.background=hl4>0&&hl4<1?'rgba(255,255,255,.12)':'transparent';
  $('cfg').style.background=hl5>0&&hl5<1?'rgba(255,255,255,.12)':'transparent';
  pop($('s4'),t,26.36,{rot:-4,out:28.30,from:.4});

  /* --- S5 form --- */
  const in5=P(t,29.94,.42), out5=P(t,37.98,.30);
  st($('form'),{opacity:clamp(in5*1.6)*(1-eo(out5)),transform:`translateY(${lerp(80,0,eo(in5))-200*eio(out5)}px) scale(${lerp(.92,1,back(in5))})`});
  const ddDone=t>=30.96;
  $('ddT').textContent=ddDone?'Static API Key':'Select…'; $('ddT').style.color=ddDone?'var(--ink)':'#999';
  $('dd').style.borderColor=(t>=30.54&&t<30.96)?'#3897F0':'#E6E1D8';
  const BU="https://api.████████.ai/v1", AK="sk-cr••••••••••••7f2a";
  const nb=Math.floor(clamp((t-32.76)/.50)*BU.length), nk=Math.floor(clamp((t-33.76)/.46)*AK.length);
  $('fbT').textContent=BU.slice(0,nb); $('fkT').textContent=AK.slice(0,nk);
  $('fb').style.borderColor=(t>=32.76&&t<33.60)?'#3897F0':'#E6E1D8';
  $('fk').style.borderColor=(t>=33.76&&t<34.60)?'#3897F0':'#E6E1D8';
  const saved=t>=35.28;
  $('svT').textContent=saved?'Saved':'Save'; $('sv').style.background=saved?'#22A35A':'var(--ink)';

  /* --- S6 picker returns --- */
  const in6=P(t,38.14,.44);
  st($('picker'),{opacity:clamp(in6*1.6)*(1-P(t,40.30,.3)),transform:`translateY(${lerp(80,0,eo(in6))}px) scale(${lerp(.92,1,back(in6))})`});
  MODELS.forEach((m,i)=>{
    const hov=(t>38.10&&t<40.3)?clamp(1-Math.abs(hoverRow6(t)-i)):0;
    $('r'+i).style.background=`rgba(255,255,255,${0.09*hov})`;
    pop($('f'+i),t,38.20+i*.04,{d:.24,from:.4});
  });
  pop($('s6'),t,39.48,{rot:6,from:1.7,out:40.28});

  /* hide scene 0-6 bodies at wipe peak */
  if(t>=WIPE.m){ ['picker','chat','brow','keyc','desk','form','s0','s1','s2','s4','s5','s6','plabel'].forEach(id=>{$(id).style.opacity=0;}); }

  /* --- S7 CTA --- */
  const s7=t>=WIPE.m;
  st($('cbox'),{opacity:s7?1:0,transform:`translateY(${s7?lerp(40,0,eo(P(t,WIPE.m,.35))):0}px)`});
  const W="link pls"; const nT=Math.floor(clamp((t-41.98)/.52)*W.length); const posted=t>=42.62;
  $('ftxt').textContent=posted?'':W.slice(0,nT);
  $('fph').style.display=(nT>0&&!posted)?'none':'inline';
  $('posted').style.height=(eo(P(t,42.62,.25))*104)+'px';
  $('post').style.opacity=(nT>=W.length&&!posted)?1:.35;
  const foc=t>=41.72&&!posted;
  $('field').style.borderColor=foc?'#3897F0':'#E6E1D8';
  $('field').style.boxShadow=foc?'0 0 0 5px rgba(56,151,240,.15)':'none';
  pop($('dm'),t,43.86,{d:.34,dy:60,from:.7});
  pop($('sent'),t,44.12,{d:.26,from:.4,rot:3});

  /* camera/cursor */
  cursorAt(t);

  /* end card */
  const pa=P(t,44.30,.34), ha=P(t,44.42,.3);
  st($('pres'),{opacity:clamp(pa*3),transform:`translateY(${lerp(50,0,eo(pa))}px) scale(${lerp(.6,1,back(pa))})`});
  st($('handle'),{opacity:clamp(ha*3),transform:`translateX(${lerp(-30,0,eo(ha))}px)`});
  const fol=t>=44.95;
  $('follow').textContent=fol?'Following':'Follow';
  $('follow').style.background=fol?'#EFEFEF':'#3897F0';
  $('follow').style.color=fol?'#141414':'#fff';
  $('follow').style.transform=`scale(${1-0.12*Math.max(0,1-Math.abs(t-44.95)/.1)})`;

  /* captions */
  let ch=null; for(const c of chunks){ if(t>=c[0].s-.06) ch=c; }
  const capEl=$('capin');
  if(!ch||t>ch[ch.length-1].e+.35){ capEl.style.opacity=0; }
  else{
    capEl.style.opacity=1;
    const k=P(t,ch[0].s-.06,.18);
    capEl.style.transform=`translateY(${(1-eo(k))*18}px) scale(${lerp(.88,1,back(k))})`;
    capEl.innerHTML=ch.map(w=>{const on=t>=w.s; const cls=on?'on':''; const sc2=on?lerp(1.12,1,eo(P(t,w.s,.16))):1;
      const kw=KEYW.test(w.w);
      return `<span class="${cls}" style="transform:scale(${sc2})${(kw&&on)?';color:#D97757':''}">${w.w}</span>`}).join(' ');
  }
  drawWipe(t);
};

const ROW0=540+18+46+40;
function curS0(t){ const k=eio(P(t,.8,1.0)); return {x:lerp(900,780,k), y:lerp(1080,ROW0+4*80,k)}; }
function hoverRow(t){ return (curS0(t).y-ROW0)/80; }
function hoverRow6(t){ const k=eio(P(t,38.2,.9)); return lerp(5,4,k); }
function cursorAt(t){
  const c=$('cursor'); let x,y,o=1,press=0;
  const m=(px,py)=>[540+(px-540)*window.WS,700+(py-700)*window.WS];
  const FXX=742, FYY=1459;
  if(t<4.3){ const q=curS0(t); [x,y]=m(q.x-4,q.y-6); o=clamp((t-.6)/.2)*(1-P(t,4.15,.15)); }
  else if(t<8.6){ o=0;x=0;y=0; }
  else if(t<16.96){
    if(t<10.30){ const k=eio(P(t,9.0,.7)); [x,y]=m(lerp(880,946,k),lerp(1000,606,k)); press=Math.max(0,1-Math.abs(t-10.30)/.08); }
    else if(t<11.52){ const k=eio(P(t,10.6,.55)); [x,y]=m(lerp(946,388,k),lerp(606,860,k)); }
    else if(t<13.06){ const k=eio(P(t,11.60,.55)); [x,y]=m(lerp(388,420,k),lerp(860,858,k)); }
    else if(t<14.70){ const k=eio(P(t,13.30,.5)); [x,y]=m(lerp(420,700,k),lerp(858,656,k)); }
    else if(t<15.98){ const k=eio(P(t,14.80,.5)); [x,y]=m(lerp(700,706,k),lerp(656,972,k)); }
    else { [x,y]=m(706,972); }
    press+=Math.max(0,1-Math.abs(t-10.30)/.08)+Math.max(0,1-Math.abs(t-11.52)/.08)+Math.max(0,1-Math.abs(t-13.06)/.08);
    press+=Math.max(0,1-Math.abs(t-14.70)/.08)+Math.max(0,1-Math.abs(t-15.98)/.08);
    o=clamp((t-8.9)/.2)*(1-P(t,16.85,.15));
  }
  else if(t<29.8){
    if(t<19.36){ const k=eio(P(t,17.2,.6)); [x,y]=m(lerp(900,66,k),lerp(1000,572,k)); }
    else if(t<20.12){ [x,y]=m(66,572); }
    else if(t<20.94){ const k=eio(P(t,20.16,.4)); [x,y]=m(lerp(66,250,k),lerp(572,668,k)); }
    else if(t<23.50){ [x,y]=m(250,668); }
    else if(t<26.10){ const k=eio(P(t,23.55,.5)); [x,y]=m(lerp(250,470,k),lerp(668,860,k)); }
    else if(t<26.36){ [x,y]=m(470,860); }
    else if(t<28.20){ [x,y]=m(470,860); }
    else if(t<28.56){ const k=eio(P(t,28.20,.36)); [x,y]=m(lerp(470,120,k),lerp(860,700,k)); }
    else { [x,y]=m(120,700); }
    press+=Math.max(0,1-Math.abs(t-19.36)/.08)+Math.max(0,1-Math.abs(t-20.12)/.08)+Math.max(0,1-Math.abs(t-20.94)/.08);
    press+=Math.max(0,1-Math.abs(t-23.50)/.08)+Math.max(0,1-Math.abs(t-26.36)/.08)+Math.max(0,1-Math.abs(t-28.56)/.08);
    o=clamp((t-17.3)/.2)*(1-P(t,29.7,.15));
  }
  else if(t<37.9){
    if(t<30.54){ const k=eio(P(t,30.0,.45)); [x,y]=m(lerp(860,400,k),lerp(760,742,k)); }
    else if(t<31.60){ [x,y]=m(400,742); }
    else if(t<32.76){ const k=eio(P(t,31.62,.5)); [x,y]=m(lerp(400,430,k),lerp(742,912,k)); }
    else if(t<34.42){ const k=eio(P(t,34.0,.42)); [x,y]=m(lerp(430,430,k),lerp(912,1040,k)); }
    else if(t<35.28){ const k=eio(P(t,34.6,.4)); [x,y]=m(lerp(430,930,k),lerp(1040,1088,k)); }
    else { [x,y]=m(930,1088); }
    press+=Math.max(0,1-Math.abs(t-30.54)/.08)+Math.max(0,1-Math.abs(t-30.96)/.08)+Math.max(0,1-Math.abs(t-35.28)/.08);
    o=clamp((t-30.0)/.2)*(1-P(t,37.8,.15));
  }
  else if(t<40.3){ const k=eio(P(t,40.3,.02)); o=0; x=0;y=0; }
  else if(t<45.0){
    if(t<41.72){ const k=eio(P(t,40.5,.55)); [x,y]=m(lerp(940,470,k),lerp(1050,668,k)); }
    else if(t<42.62){ const k=eio(P(t,42.0,.42)); [x,y]=m(lerp(470,858,k),lerp(668,662,k)); }
    else if(t<43.9){ [x,y]=m(858,662); }
    else { const k=eio(P(t,43.9,.42)); [x,y]=m(lerp(858,FXX,k),lerp(662,FYY,k)); }
    press=Math.max(0,1-Math.abs(t-41.72)/.08)+Math.max(0,1-Math.abs(t-42.62)/.08)+Math.max(0,1-Math.abs(t-44.95)/.08);
    o=clamp((t-40.45)/.2)*(1-P(t,44.98,.2));
  } else { o=0; x=0; y=0; }
  st(c,{opacity:o,transform:`translate(${x}px,${y}px) scale(${1-press*.18})`});
}
window.render(0);
