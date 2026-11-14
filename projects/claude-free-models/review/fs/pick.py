import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
src, out, frames, cols, tw, bright = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")], int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
try: f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", max(16, tw//14))
except Exception: f = ImageFont.load_default()
ims=[]
for n in frames:
    p=os.path.join(src,"f%04d.jpg"%n)
    im=Image.open(p).convert("RGB")
    h=int(im.height*tw/im.width); im=im.resize((tw,h),Image.LANCZOS)
    if bright!=1.0: im=ImageEnhance.Brightness(im).enhance(bright)
    d=ImageDraw.Draw(im); lbl=str(n)
    d.rectangle([0,0,d.textlength(lbl,font=f)+12,10+f.size],fill=(0,0,0))
    d.text((6,3),lbl,font=f,fill=(255,255,0))
    ims.append(im)
h=ims[0].height; rows=(len(ims)+cols-1)//cols
s=Image.new("RGB",(cols*tw,rows*h),(25,25,25))
for k,im in enumerate(ims): s.paste(im,((k%cols)*tw,(k//cols)*h))
s.save(out,quality=90); print(out,s.size)
