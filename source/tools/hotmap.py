#!/usr/bin/env python3
"""Room paintings with the hotspots (red), walk points (yellow) and walk areas (green):
    WOS2_CHAPTER=n python3 tools/hotmap.py outdir [room ...]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'art'))
import game, build
G = game.G
out = sys.argv[1]
want = sys.argv[2:]
for r, R in G.rooms.items():
    if want and r not in want:
        continue
    try:
        fn, _ = build.room_art(R['art'])
    except KeyError:
        continue
    cv = fn()
    c = cv.c.reshape(cv.h // 2, 2, cv.w // 2, 2, 3).mean((1, 3))
    im = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8)).resize((640, 336), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for poly in R['walk'] or []:
        d.polygon([(x * 2, y * 2) for x, y in poly], outline=(0, 255, 0))
    for o in R['objects']:
        ob = G.objects[o]
        if ob['box']:
            x0, y0, x1, y1 = ob['box']
            d.rectangle((x0 * 2, y0 * 2, x1 * 2, y1 * 2), outline=(255, 40, 40))
            d.text((x0 * 2 + 2, y0 * 2 + 1), o, fill=(255, 255, 255))
        if ob['walk']:
            wx, wy = ob['walk']
            d.ellipse((wx * 2 - 2, wy * 2 - 2, wx * 2 + 2, wy * 2 + 2), fill=(255, 255, 0))
    for y in range(0, 168, 20):
        d.text((1, y * 2), str(y), fill=(255, 255, 0))
    for x in range(0, 320, 20):
        d.text((x * 2, 326), str(x), fill=(0, 255, 255))
    im.save(os.path.join(out, f'c{game.CH}_{r}.png'))
    print(r, R['art'])
