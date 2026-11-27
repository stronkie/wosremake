#!/usr/bin/env python3
"""Quick look at room paintings: artprev.py module room[:kw=val] ... -> one sheet"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'art'))
import importlib
mod = importlib.import_module(sys.argv[1])
out = sys.argv[2]
ims = []
for spec in sys.argv[3:]:
    name, *kw = spec.split(':')
    kws = {}
    for k in kw:
        a, b = k.split('=')
        kws[a] = eval(b)
    cv = mod.ROOM_ART[name](**kws)
    c = cv.c.reshape(cv.h // 2, 2, cv.w // 2, 2, 3).mean((1, 3))
    im = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for y in range(0, 168, 20):
        d.text((1, y), str(y), fill=(255, 255, 0))
    for x in range(0, 320, 40):
        d.text((x, 158), str(x), fill=(0, 255, 255))
    ims.append(im)
cols = 2
rows = (len(ims) + 1) // 2
sheet = Image.new('RGB', (cols * 320, rows * 168))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * 320, (i // cols) * 168))
sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out)
