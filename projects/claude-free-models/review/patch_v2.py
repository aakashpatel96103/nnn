from pathlib import Path
import json
p=Path('src/reel.html');s=p.read_text(encoding='utf-8')
s=s.replace('</style>', '''#proof{left:180px;top:535px;width:720px;height:620px;overflow:hidden;border-radius:18px;background:#fff;box-shadow:0 22px 55px #0003;display:none}#proof img{position:absolute;max-width:none}#proofnote{left:180px;top:1170px;font:500 18px var(--mono);color:var(--mute)}
</style>''')
s=s.replace('  <!-- stickers -->','  <div class="abs" id="proof"><img id="proofimg"></div><div class="abs" id="proofnote"></div>\n  <!-- stickers -->')
s=s.replace('https://••••••••.ai','coarena.ai').replace('https://api.████████.ai/v1','https://coarena.ai/api').replace('sk-cr••••••••••••7f2a','coa_••••••••').replace('background:#262624','background:#181818')
s=s.replace('through the Model API.','through the Coarena Model API.')
s=s.replace('const KICK=[1.16,3.58,5.26,7.32,10.30,11.52,13.06,14.70,15.98,19.36,20.12,20.94,23.50,26.36,28.56,30.54,35.28,37.04,39.48,41.98,42.62,44.12];','const KICK=[23.50,35.28,42.62];')
s=s.replace('const mi=P(t,18.70,.3)','const mi=P(t,19.36,.18)')
s=s.replace('const lv = (t>=20.16&&t<24.3)?2:(t>=19.42&&t<20.16)?1:(t>=18.70&&t<19.42)?0:-1;','const lv = (t>=20.94&&t<24.3)?2:(t>=20.12&&t<20.94)?1:(t>=19.36&&t<20.12)?0:-1;')
s=s.replace('const lvB=(t>=26.14&&t<28.40)?3:(t>=28.40&&t<29.80)?4:-1;','const lvB=(t>=25.30&&t<26.36)?3:(t>=26.36&&t<29.80)?4:-1;')
s=s.replace('P(t,28.42,.36)','P(t,27.90,.36)')
s=s.replace('const pa=P(t,44.30,.34), ha=P(t,44.42,.3);','const pa=P(t,43.75,.28), ha=P(t,43.85,.28);')
s=s.replace('const ki=P(t,13.10,.36)','const ki=P(t,14.20,.18)')
s=s.replace('(t-13.50)/.62','(t-14.20)/.22')
s=s.replace('  drawWipe(t);','  recordedProof(t);\n  drawWipe(t);')
insert='''
let expectedProof='';
window.footageReady=()=>!expectedProof||($('proofimg').complete&&$('proofimg').naturalWidth>0&&$('proofimg').getAttribute('src')===expectedProof);
function recordedProof(t){
  const panel=$('proof'),img=$('proofimg'); let spec=null;
  if(t<4.30) spec=['pick',1+Math.min(128,Math.floor(t*30)),[0,0,520,565],720,630];
  else if(t>=4.40&&t<8.50) spec=['pick',15+Math.min(120,Math.floor((t-4.4)*30)),[0,0,520,565],720,630];
  else if(t>=8.62&&t<10.70) spec=['webl',Math.min(121,1+Math.floor((t-8.62)*58)),[450,150,1000,660],840,555];
  else if(t>=10.70&&t<12.65) spec=['usage',1+Math.min(110,Math.floor((t-10.70)*30)),[590,110,1100,680],840,555];
  else if(t>=12.65&&t<14.20) spec=['keymk',Math.min(141,51+Math.floor((t-12.65)*60)),[470,120,930,660],840,555];
  else if(t>=38.10&&t<40.30) spec=['pick',15+Math.min(120,Math.floor((t-38.10)*50)),[0,0,520,565],720,630];
  for(const id of ['picker','chat','brow','plabel']) $(id).style.display='none';
  $('s0').style.display='none';$('s1').style.display='none';$('s2').style.display='none';
  panel.style.display=spec?'block':'none';$('proofnote').textContent=spec?'SCREEN RECORDING':'';
  if(spec){
    const [pool,n,crop,w,h]=spec; const [x,y,cw,ch]=crop; const scale=Math.max(w/cw,h/ch);
    expectedProof='../assets/'+pool+'/f'+String(n).padStart(4,'0')+'.jpg';
    if(img.getAttribute('src')!==expectedProof) img.setAttribute('src',expectedProof);
    st(panel,{left:((1080-w)/2)+'px',width:w+'px',height:h+'px',top:'535px'});
    st(img,{width:((pool==='pick'?520:1726)*scale)+'px',height:'auto',left:(-x*scale)+'px',top:(-y*scale)+'px'});
    $('cursor').style.opacity=0;
  } else expectedProof='';
}
'''
s=s.replace('window.render(0);',insert+'\nwindow.render(0);')
p.write_text(s,encoding='utf-8')
c=json.loads(Path('project.json').read_text());c['status']='building';c['footage_wait']=[{'from':-1,'to':45.61,'start':0,'fps':30,'count':1368,'require':"typeof window.footageReady==='function'",'expr':'()=>window.footageReady()'}];Path('project.json').write_text(json.dumps(c,indent=2))
