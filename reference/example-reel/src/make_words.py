import json
raw=json.load(open('src/words_raw.json',encoding='utf-8'))
L1=[("Claude",.26,.58),("ke",.58,.84),("saare",.84,1.18),("AI",1.18,1.42),("models",1.42,1.78),("main",1.78,2.04),("FREE",2.04,2.32),("mein",2.32,2.5),("use",2.5,2.64),("karta",2.64,2.85),("hoon,",2.85,3.09),("aur",3.33,3.48),("tum",3.62,3.76),("bhi",3.76,3.86),("kar",3.86,3.98),("sakte",3.98,4.2),("ho!",4.2,4.37)]
def remap(ws,a,b,A,B): return [(w,round(A+(s-a)*(B-A)/(b-a),3),round(A+(e-a)*(B-A)/(b-a),3)) for w,s,e in ws]
r=[(x['w'].strip(),x['s'],x['e']) for x in raw]
l2=r[0:17]; l3=r[17:40]; l4=r[40:]
# merge "set up" and fix spellings to the script
def merge(ws):
    out=[]
    for w,s,e in ws:
        if w=='up' and out and out[-1][0]=='set': out[-1]=('setup',out[-1][1],e)
        else: out.append((w,s,e))
    return out
l3=merge(l3)
fix3="Agar tum bhi ye setup karna chahte ho, toh main tumhe API key aur complete setup guide share kar dunga!".split()
fix4='Toh comment karo "CLAUDE" aur main tumhe API key ka link DM kar dunga!'.split()
fix2="Bas ek API key chahiye aur tum bhi Claude ke different models ko access kar sakte ho!".split()
# whisper splits "dunga" as doon+ga -> merge last two
def mergelast(ws): return ws[:-2]+[(ws[-2][0]+ws[-1][0],ws[-2][1],ws[-1][2])]
l3=mergelast(l3); l4=mergelast(l4)
assert len(l2)==len(fix2) and len(l3)==len(fix3) and len(l4)==len(fix4),(len(l3),len(fix3),len(l4),len(fix4))
l2=[(f,s,e) for f,(w,s,e) in zip(fix2,l2)]; l3=[(f,s,e) for f,(w,s,e) in zip(fix3,l3)]; l4=[(f,s,e) for f,(w,s,e) in zip(fix4,l4)]
l2=remap(l2,4.32,8.68,4.72,8.74); l3=remap(l3,9.08,13.78,9.28,13.80); l4=remap(l4,14.2,17.58,14.22,17.59)
words=[{"w":w,"s":s,"e":e,"line":i} for i,L in enumerate([L1,l2,l3,l4]) for (w,s,e) in L]
json.dump(words,open('src/words.json','w'),indent=0)
for x in words: print(x)
