import sys, os
from PIL import Image, ImageDraw, ImageFont
src, out, step, cols, tw = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
files = sorted(os.listdir(src))
idx = list(range(0, len(files), step))
try: f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", max(14, tw//16))
except Exception: f = ImageFont.load_default()
ims = []
for n in idx:
    im = Image.open(os.path.join(src, files[n])).convert("RGB")
    h = int(im.height * tw / im.width)
    im = im.resize((tw, h), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    lbl = str(n+1)
    d.rectangle([0,0, d.textlength(lbl, font=f)+10, 8+ f.size], fill=(0,0,0))
    d.text((5, 2), lbl, font=f, fill=(255,255,0))
    ims.append(im)
h = ims[0].height; rows = (len(ims)+cols-1)//cols
sheet = Image.new("RGB", (cols*tw, rows*h), (30,30,30))
for k, im in enumerate(ims):
    sheet.paste(im, ((k%cols)*tw, (k//cols)*h))
sheet.save(out, quality=88)
print(out, sheet.size, len(ims), "tiles")
