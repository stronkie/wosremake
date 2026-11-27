"""The loading screen of World of Stronkie remake (from WoS II's loading.py).

It is the loading screen of part 1 (the blue frame, the title bar, the
loading panel) with a new title, a new picture (the STARRAVEN back on
Stronkie, the Pilot and Lyra, Pip) and the Stronkie Soft logo.

    make() -> (rgb 256 x 320 x 3 uint8, chunky 256 x 320, palette 32 x 3 floats,
               bar dict)
"""
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import people                                       # noqa: E402
from paint import Canvas                            # noqa: E402

IMAGES = os.path.join(HERE, '..', 'images')
FONT8 = os.path.join(HERE, '..', 'font8x8_basic.h')

BG = (0, 43, 105)            # the panel blue of the frame
NAVY = (0, 0, 56)
SCENE = (11, 56, 307, 191)   # x0, y0, x1, y1 of the picture inside the frame
BAR = (24, 206, 297, 217)    # the progress bar (outline included)


def font8():
    src = open(FONT8).read()
    import re
    rows = re.findall(r'\{\s*((?:0x[0-9A-Fa-f]{2},?\s*){8})\}', src)
    glyphs = []
    for r in rows[:128]:
        glyphs.append([int(v, 16) for v in re.findall(r'0x[0-9A-Fa-f]{2}', r)])
    return glyphs


F8 = font8()


def text8(img, x, y, s, col, shadow=None):
    """the 8 x 8 font (bit 0 = left), one cell a letter"""
    for i, ch in enumerate(s):
        g = F8[ord(ch)]
        for r in range(8):
            for b in range(8):
                if g[r] >> b & 1:
                    if shadow is not None:
                        img[y + r + 1, x + i * 8 + b + 1] = shadow
                    img[y + r, x + i * 8 + b] = col


def prop_text(img, x, y, s, col, outline):
    """the game's proportional font, with an outline"""
    import wosdata as WD
    glyphs = WD.font_glyphs(FONT8)
    cells = []
    cx = 0
    for ch in s:
        w, rows = glyphs[ord(ch) - 32]
        for r in range(8):
            for b in range(8):
                if rows[r] >> (7 - b) & 1:
                    cells.append((cx + b, r))
        cx += w + 1
    width = cx - 1
    x0 = x - width // 2 if x is not None else 0
    pts = {(x0 + a, y + b) for a, b in cells}
    for px, py in pts:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (px + dx, py + dy) not in pts:
                    img[py + dy, px + dx] = outline
    for px, py in pts:
        img[py, px] = col
    return width


def letters(a, y0, y1, x0, x1, bg):
    """the letters of a line of the old title: (x, picture) for each"""
    seg = a[y0:y1, x0:x1]
    ink = (np.abs(seg.astype(int) - bg).sum(2) > 0)
    core = ink.any(0)
    out = []
    x = 0
    while x < seg.shape[1]:
        if core[x]:
            s = x
            while x < seg.shape[1] and core[x]:
                x += 1
            out.append((x0 + s, seg[:, s:x].copy(), ink[:, s:x].copy()))
        x += 1
    return out


def big_sprite(fn, *args, **kw):
    """a people frame drawn twice as big (with the same 4x4 drawing scale)"""
    old_k, old_finish = people.K, people.Pen.finish
    people.K = 8

    def finish(self, outline=True):
        B = 4
        h, w = self.h * 2, self.w * 2
        a = np.asarray(self.im, np.int16).reshape(h, B, w, B).transpose(0, 2, 1, 3).reshape(h, w, B * B)
        out = np.zeros((h, w), np.int16)
        for y in range(h):
            for x in range(w):
                v = a[y, x]
                nz = v[v > 0]
                if len(nz) * 2 >= B * B * 0.75:
                    vals, cnt = np.unique(nz, return_counts=True)
                    out[y, x] = vals[cnt.argmax()]
        body = out > 0
        ring = np.zeros_like(body)
        ring[1:] |= body[:-1]
        ring[:-1] |= body[1:]
        ring[:, 1:] |= body[:, :-1]
        ring[:, :-1] |= body[:, 1:]
        out[ring & ~body] = people.BLACK
        out[out == 0] = -1
        return out
    people.Pen.finish = finish
    try:
        return fn(*args, **kw)
    finally:
        people.K, people.Pen.finish = old_k, old_finish


def paste_sprite(rgb, spr, x, y):
    """spr: palette indices 16-31 (-1 clear), (x, y) = between the feet"""
    pal = np.array([[int(c[i], 16) * 17 for i in (1, 2, 3)] for c in people.FIXED], np.uint8)
    h, w = spr.shape
    x0, y0 = x - w // 2, y - h + 1
    for yy in range(h):
        for xx in range(w):
            v = spr[yy, xx]
            if v >= 0 and 0 <= y0 + yy < rgb.shape[0] and 0 <= x0 + xx < rgb.shape[1]:
                rgb[y0 + yy, x0 + xx] = pal[v - 16]


def scene():
    """the new picture: back on Stronkie, two moons, a heart"""
    W, H = SCENE[2] - SCENE[0], SCENE[3] - SCENE[1]
    cv = Canvas('#05061a', h=H)
    stronkie_sky(cv, 92, top='#05061a', mid='#2a1a5a', low='#9a4a90', seed=57, night=True)
    meadow_ground(cv, 96, 7, '#1a0a30', '#5a2878')
    alien_tree(cv, 300, 104, 70, 3, leaves=('#3a1a6a', '#a070e0'))
    hut(cv, 258, 104, 40, 20, roof='#3a1a3a', wall='#6a4848')
    cv.glow(cv.ellipse(258, 96, 4, 4), '#ffb060', 12, 0.5)
    hut(cv, 222, 100, 30, 15, roof='#3a1a3a', wall='#5a4040')
    starraven(cv, 46, 122, 0.78)
    hut(cv, 196, 106, 34, 17, roof='#3a1a3a', wall='#5a4040')
    cv.glow(cv.ellipse(196, 100, 3, 3), '#ffb060', 10, 0.5)
    flowers(cv, 60, 0, 320, 110, 134, seed=17, cols=('#ffe070', '#ff80c0', '#80e0ff', '#ffffff'))
    cv.vignette(0.25)
    c = cv.c.reshape(H, 2, cv.w // 2, 2, 3).mean((1, 3))
    rgb = (np.clip(c, 0, 1) * 255).astype(np.uint8)[:, :W].copy()
    painted = rgb.copy()
    # the people
    pilot = big_sprite(people.human, people.PILOT, 'side', None)
    lyra = people.mirror(big_sprite(people.human, people.LYRA, 'side', None))
    pip = big_sprite(people.stronkie, 'front', pose='jump')
    paste_sprite(rgb, pilot, 112, 122)
    paste_sprite(rgb, lyra, 150, 122)
    paste_sprite(rgb, pip, 186, 124)
    # a little heart between them
    heart = ['.##.##.', '#######', '#######', '.#####.', '..###..', '...#...']
    hx, hy = 128, 22
    for r, row in enumerate(heart):
        for k, ch in enumerate(row):
            if ch == '#':
                for dy in (0, 1):
                    for dx in (0, 1):
                        rgb[hy + r * 2 + dy, hx + k * 2 + dx] = (255, 64, 128)
    exact = (rgb != painted).any(2)
    return rgb, exact


def logo(rgb, x, y):
    im = Image.open(os.path.join(IMAGES, 'stronkiesoft_logo.png')).convert('RGBA')
    im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)
    a = np.asarray(im)
    for yy in range(a.shape[0]):
        for xx in range(a.shape[1]):
            if a[yy, xx, 3] > 128:
                rgb[y + yy, x + xx] = a[yy, xx, :3]


LOAD_LINES = {
    1: ('>> THE PROLOGUE: RAVENMOOR MANOR', '>> NOW WITH A MOUSE. NO TYPING!'),
    2: ('>> CHAPTER TWO: INTO SPACE', '>> THE STARRAVEN AND STATION KX-9'),
    3: ('>> CHAPTER THREE: ASTEROID 42', '>> THE SCUMM BAR AND THE PIRATES'),
    4: ('>> CHAPTER FOUR: LANDFALL', '>> THE JUNGLE AND THE VILLAGE'),
    5: ('>> CHAPTER FIVE: THE CRYSTAL MOUNTAINS', '>> THE ICE CAVES AND THE SKY TEMPLE'),
    6: ('>> CHAPTER SIX: THE STAR HEART', '>> THE TEMPLE HEART AND THE REPAIRS'),
    7: ('>> CHAPTER SEVEN: VEX\'S FLAGSHIP', '>> THE PRISON DECK, THE BRIDGE, HOME'),
}


def make(ch=1):
    """the loading screen of the original World of Stronkie (V2.3), as a remake:
    the same title and picture, REMAKE under the title, the Stronkie Soft logo"""
    old = Image.open(os.path.join(IMAGES, 'loading_wos1.png')).convert('RGB')
    a = np.asarray(old.resize((320, 256), Image.NEAREST)).copy()
    # ---- the line under the title
    a[30:42, 60:262] = BG
    prop_text(a, 160, 32, 'REMAKE', (236, 197, 59), NAVY)
    soft = np.zeros(a.shape[:2], bool)           # the painted picture: dithered
    soft[SCENE[1]:SCENE[3], SCENE[0]:SCENE[2]] = True
    before_logo = a.copy()
    logo(a, SCENE[0] + 5, SCENE[1] + 5)
    soft &= ~(a != before_logo).any(2)
    # ---- the loading panel
    a[196:205, 20:300] = BG
    text8(a, 24, 197, 'LOADING ADVENTURE...', (89, 197, 43))
    a[218:235, 20:300] = BG
    text8(a, 24, 218, LOAD_LINES[ch][0], (123, 178, 236))
    text8(a, 24, 226, LOAD_LINES[ch][1], (236, 197, 59))
    a[238:248, 14:306] = NAVY
    line = 'STRONKIE SOFT (C) 2026 - AMIGA 500'
    text8(a, 160 - len(line) * 4, 239, line, (236, 197, 59))
    x0, y0, x1, y1 = BAR
    a[y0 + 2:y1 - 2, x0 + 2:x1 - 1] = BG
    full = a.copy()
    for sx in range(x0 + 2, x1 - 2, 6):
        a[y0 + 2:y1 - 3, sx:sx + 5] = NAVY
        full[y0 + 2:y1 - 3, sx:sx + 5] = (89, 197, 43)
    return a, full, soft


TINY = {   # 3 x 5 letters, row by row
    'A': ['.#.', '#.#', '###', '#.#', '#.#'], 'E': ['###', '#..', '##.', '#..', '###'],
    'H': ['#.#', '#.#', '###', '#.#', '#.#'], 'I': ['###', '.#.', '.#.', '.#.', '###'],
    'L': ['#..', '#..', '#..', '#..', '###'], 'O': ['###', '#.#', '#.#', '#.#', '###'],
    'P': ['##.', '#.#', '##.', '#..', '#..'], 'R': ['##.', '#.#', '##.', '#.#', '#.#'],
    'T': ['###', '.#.', '.#.', '.#.', '.#.'], 'Y': ['#.#', '#.#', '.#.', '.#.', '.#.'],
    ' ': ['...'] * 5,
}


def tiny(a, x, y, s, col):
    for i, ch in enumerate(s):
        for r, row in enumerate(TINY[ch]):
            for k, c in enumerate(row):
                if c == '#':
                    a[y + r, x + i * 4 + k] = col


BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16 - 0.47


def quantize32(a, full, soft):
    """32 colours for the whole screen: the frame, the people and the logo
    exactly (they weigh more), the painted picture dithered"""
    px = a.reshape(-1, 3).astype(np.float32) / 255
    w = np.where(soft.reshape(-1), 1.0, 12.0)
    cols, inv = np.unique(np.round(px * 15).astype(np.int16), axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    wt = np.bincount(inv, weights=w)
    cols = cols.astype(np.float32) / 15
    order = np.argsort(-wt)
    cent = cols[order[:32]].copy()
    for _ in range(40):
        d = ((cols[:, None] - cent[None]) ** 2).sum(2)
        lab = d.argmin(1)
        for k in range(32):
            m = lab == k
            if m.any():
                cent[k] = (cols[m] * wt[m, None]).sum(0) / wt[m].sum()
    pal = np.round(cent * 15) / 15
    pal[pal.sum(1).argmin()] = 0                      # colour 0: black (the border)

    def idx(img, dith):
        f = img.astype(np.float32) / 255
        if dith is not None:
            h, w_ = img.shape[:2]
            thr = BAYER[np.arange(h)[:, None] % 4, np.arange(w_)[None, :] % 4]
            f = f + (thr * 0.05)[..., None] * dith[..., None]
        d = ((f[:, :, None, :] - pal[None, None]) ** 2).sum(3)
        return d.argmin(2)
    ci = idx(a, soft)
    cf = idx(full, soft)
    # colour 0 first (the border and the empty screen)
    z = int(np.where(pal.sum(1) == 0)[0][0])
    perm = [z] + [k for k in range(32) if k != z]
    pal = pal[perm]
    back = np.argsort(perm)
    return back[ci], back[cf], pal


if __name__ == '__main__':
    a, full, soft = make()
    ca, cf, pal = quantize32(a, full, soft)
    out = (pal[ca] * 255).astype(np.uint8)
    Image.fromarray(out).resize((640, 512), Image.NEAREST).save(sys.argv[1] if len(sys.argv) > 1 else 'loading.png')
