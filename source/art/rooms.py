"""The rooms of The World of Stronkie II, chapter 1, painted (320 x 168).

The people are not painted in: they walk about as sprites. Things that change
(the open hatch, the Moonflower in bloom, a sky crystal on the floor) are
painted in a variant of the room; build.py cuts the difference out as an
object picture."""
import sys
import os
import numpy as np
import props                                     # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint import Canvas, rgb, mix, W, H            # noqa: E402
from kit import *                                   # noqa: E402,F401,F403
from scenes1 import starraven                       # noqa: E402
from scenes3 import alien_tree, hut                 # noqa: E402

FONT = None


def font():
    global FONT
    if FONT is None:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        from wosdata import font_glyphs
        FONT = font_glyphs('/home/claude/tools/font8x8/font8x8_basic.h')
    return FONT


def text_mask(cv, x, y, text, scale=1.0, centre=False):
    """the game font as a mask on the canvas"""
    g = font()
    w = sum(g[ord(c) - 32][0] + 1 for c in text) * scale
    if centre:
        x -= w / 2
    m = np.zeros((cv.h, cv.w), np.float32)
    px = x
    for ch in text:
        wd, rows = g[ord(ch) - 32]
        for r, bits in enumerate(rows):
            for c in range(8):
                if bits & (0x80 >> c):
                    x0 = int((px + c * scale) * 2)
                    y0 = int((y + r * scale) * 2)
                    m[y0:y0 + int(2 * scale + 0.5), x0:x0 + int(2 * scale + 0.5)] = 1
        px += (wd + 1) * scale
    return m


# ---------------------------------------------------------------- shared pieces
def stronkie_sky(cv, horizon=100, top='#2a1a5a', mid='#9a4a90', low='#f0a0b0', moons=True, seed=3, night=False):
    m = cv.rect(0, 0, W, horizon + 2)
    cv.fill(m, cv.vgrad([(0, top), (horizon * 0.65, mid), (horizon, low)]))
    if night:
        star_field(cv, 0, 0, W, horizon, 140, seed=seed, twinkle=False)
    if moons:
        for x, y, r, c, a in ((236, 30, 14, '#fff4d8', 0.9 if night else 0.55), (276, 48, 9, '#d8e8ff', 0.8 if night else 0.45)):
            mm = cv.ellipse(x, y, r, r)
            cv.glow(mm, c, r * 2.2, 0.5 * a)
            cv.fill(mm, c, a)
            cv.shade_sphere(x, y, r, mm, light=(-0.4, -0.3), amb=0.7)
    if not night:
        clouds(cv, m, 8, horizon * 0.55, '#7a4a90', '#f0b0d0', seed=seed + 2, cover=0.35, scale=26)
    return m


def meadow_ground(cv, top=104, seed=4, c0='#3a1458', c1='#9a4ab8'):
    g = hills(cv, top, 5, '#6a2a8a', '#2a1040', seed)
    n = cv.noise(2.5, 3, seed + 1, sx=cv.X * 2.5, sy=cv.Y * 0.6)
    cv.fill(g, mix(rgb(c0), rgb(c1), n), 0.85)
    blades = (cv.noise(0.6, 2, seed + 7, sx=cv.X * 3, sy=cv.Y * 0.3) > 0.62) & (cv.Y > top + 6)
    cv.fill(blades * 1.0, '#c070e0', 0.45)
    return g


def flowers(cv, n, x0, x1, y0, y1, seed=9, cols=('#ffe070', '#ff80c0', '#80e0ff', '#ffffff')):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = 1.0 + (y - y0) / max(1, (y1 - y0)) * 1.4
        cv.fill(cv.line([(x, y), (x, y + r * 2.5)], 0.6), '#305020')
        f = cv.ellipse(x, y, r, r * 0.8)
        cv.fill(f, cols[i % len(cols)])
        cv.fill(cv.ellipse(x, y, r * 0.35, r * 0.35), '#ffa020')


def path(cv, pts, width, col=('#6a5070', '#9a80a0')):
    m = cv.line(pts, width)
    cv.fill(m, cv.texture(col[0], col[1], 1.5, 3, 21, 1.6), 0.9)
    return m


def lantern_string(cv, x0, y0, x1, y1, sag=10, n=8, night=False, seed=5):
    pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * np.sin(np.pi * t)) for t in np.linspace(0, 1, 24)]
    cv.fill(cv.line(pts, 0.6), '#2a1a2a')
    cols = ['#ff6080', '#ffd040', '#60d0ff', '#a0ff80']
    for i in range(n):
        t = (i + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + sag * np.sin(np.pi * t) + 2
        if night:
            l = cv.ellipse(x, y + 2, 2.2, 3)
            cv.glow(l, cols[i % 4], 8, 0.6)
            cv.fill(l, cols[i % 4])
        else:
            fl = cv.poly([(x - 3, y), (x + 3, y), (x, y + 6)])
            cv.fill(fl, cols[i % 4])


# ---------------------------------------------------------------- 1 the landing meadow
def meadow(hatch_open=False):
    cv = Canvas()
    stronkie_sky(cv, 98, seed=11)
    mountains(cv, 92, 26, '#5a3a8a', snow='#e0d0ff', seed=13, shade='#3a2060', snowline=0.6)
    meadow_ground(cv, 100, 4)
    for x, h, s in ((300, 70, 3), (14, 60, 5), (190, 34, 7)):
        alien_tree(cv, x, 112, h, s)
    path(cv, [(170, 168), (230, 140), (320, 132)], 14)
    path(cv, [(236, 140), (232, 120), (226, 106)], 8)
    sh = cv.ellipse(84, 140, 46, 8)
    cv.tint(sh, 0.55)
    starraven(cv, 84, 140, 0.85)
    if hatch_open:
        hatch = cv.poly([(78, 118), (90, 118), (90, 136), (78, 136)])
        cv.fill(hatch, '#14101c')
        cv.add(cv.rect(79, 119, 89, 121), '#ffe0a0', 0.4)
        ramp = cv.poly([(78, 136), (90, 136), (98, 142), (70, 142)])
        cv.fill(ramp, '#8088a0')
        cv.bevel(ramp, 1, 0.5)
    else:
        hatch = cv.rect(78, 118, 90, 136)
        cv.fill(hatch * (1 - cv.rect(79, 119, 89, 135)), '#30343c')
        cv.fill(cv.rect(87, 126, 88.5, 128), '#ffd040')
    flowers(cv, 70, 0, 320, 142, 166, seed=3)
    bush(cv, 300, 160, 16, c=('#3a1050', '#8a40b0'), seed=5)
    props.mushroom(cv, 30, 134)
    cv.vignette(0.3)
    return cv


# ---------------------------------------------------------------- 2 the village square
def square(night=False, bunting=True, watch=False):
    cv = Canvas()
    props.gta_poster(cv, 175, 88, 16, 18)            # Grand Theft Glider VI
    if night:
        stronkie_sky(cv, 96, top='#05061a', mid='#1a1a4a', low='#3a2a6a', seed=17, night=True)
    else:
        stronkie_sky(cv, 96, seed=17)
    meadow_ground(cv, 98, 11, '#3a1458', '#8a40a8')
    hut(cv, 160, 108, 70, 36, roof='#7a3a2a', wall='#b08050')         # Elder's hut (north)
    door = cv.rect(150, 86, 170, 108)
    cv.fill(door, '#2a140a')
    cv.fill(cv.ellipse(160, 86, 10, 6) * (cv.Y < 86), '#2a140a')
    hut(cv, 46, 112, 50, 28, roof='#5a3a6a', wall='#9a7a50')
    hut(cv, 270, 106, 40, 22, roof='#6a3a1a', wall='#a07040')
    # the garden gate (east)
    for x in (302, 318):
        cv.fill(cv.rect(x, 96, x + 3, 136), '#4a2c18')
    arch = cv.line([(303, 98), (310, 90), (319, 98)], 3)
    cv.fill(arch, '#3a7a2a')
    flowers(cv, 12, 300, 320, 88, 100, seed=12)
    pave = cv.ellipse(160, 168, 175, 44)
    cv.fill(pave, blocks(cv, cv.X, cv.Y * 2, '#6a5a7a', '#9a88aa', 14, 8, '#3a2a4a'))
    # the fountain
    fb = cv.ellipse(170, 150, 34, 9)
    cv.fill(fb, '#6a6080')
    cv.bevel(fb, 1.5, 0.6)
    wt = cv.ellipse(170, 149, 29, 6.5)
    cv.fill(wt, cv.texture('#2050a0', '#60b0f0', 2, 3, 8))
    col = cv.rect(166, 118, 174, 148)
    cv.fill(col, '#8a80a0')
    cv.bevel(col, 1.5, 0.6)
    for s in (-1, 1):
        jet = cv.line([(170, 118), (170 + s * 10, 112), (170 + s * 20, 146)], 1.0)
        cv.fill(jet, '#a0e0ff', 0.8)
        props.flick(cv, 'jet', jet, ['#ffffff', '#a0e0ff', '#5080c0', '#a0e0ff'], speed=3, phase=(cv.Y / 6) % 1)
    # the old well (left)
    wl = cv.ellipse(52, 146, 18, 6)
    ring = cv.rect(34, 130, 70, 146)
    cv.fill(ring, blocks(cv, cv.X, cv.Y, '#6a6070', '#9a90a0', 9, 5, '#2a2430'))
    cv.bevel(ring, 1.5, 0.5)
    cv.fill(cv.ellipse(52, 130, 18, 5), '#100c14')
    for x in (36, 66):
        cv.fill(cv.rect(x, 104, x + 3, 130), '#4a2c18')
    rf = cv.poly([(30, 106), (74, 106), (52, 94)])
    cv.fill(rf, cv.texture('#6a3a1a', '#9a5a2a', 1.2, 3, 4, 1.6))
    cv.bevel(rf, 1.5, 0.5)
    cv.fill(cv.rect(38, 111, 66, 113), '#3a2010')
    # Gobbo's stall (right)
    st = cv.rect(226, 112, 290, 140)
    cv.fill(st, planks(cv, cv.X, cv.Y, '#5a3418', '#8a5a2a', 6))
    cv.bevel(st, 2, 0.5)
    aw = cv.poly([(220, 96), (296, 96), (290, 112), (226, 112)])
    stp = ((cv.X / 7).astype(int) % 2 == 0)
    cv.fill(aw * stp, '#e04080')
    cv.fill(aw * ~stp, '#f0f0f0')
    cv.bevel(aw, 1.5, 0.5)
    for p in (222, 292):
        cv.fill(cv.rect(p, 96, p + 3, 140), '#4a2c18')
    rng = np.random.default_rng(2)
    for k in range(8):
        fx, fy = 232 + k * 7.5, 108 + rng.uniform(-1, 1)
        r = cv.poly([(fx - 2, fy - 4), (fx + 2, fy - 4), (fx + 3, fy + 3), (fx - 3, fy + 3)])
        cv.fill(r, ['#ff6080', '#ffd040', '#60d0ff', '#a0ff80'][k % 4])
    # festival bunting
    if bunting:
        lantern_string(cv, 0, 66, 140, 74, 10, 9, night, 1)
        lantern_string(cv, 180, 74, 320, 64, 10, 9, night, 2)
    if watch:                                   # the White Rabbit's pocket watch
        w = cv.ellipse(102, 156, 4, 3.4)
        cv.fill(w, cv.rgrad(101, 155, 5, '#fff0a0', '#c08010'))
        cv.fill(cv.ellipse(102, 156, 2.6, 2.2), '#f8f4e8')
        cv.fill(cv.line([(102, 156), (102, 154.5)], 0.4), '#202020')
        cv.fill(cv.line([(105, 154), (110, 158), (108, 161)], 0.5), '#e0c040')
    props.flick(cv, 'water', wt, ['#2050a0', '#3070c0', '#60b0f0', '#3070c0'] if not night else
                ['#102850', '#183870', '#305888', '#183870'], speed=4, regs=2, phase=(cv.X / 8 + cv.Y / 3) % 1)
    props.fireflies(cv, 20, 100, 300, 140, 10, 4, '#ffd080', '#604020') if night else None
    if night:
        cv.tint(cv.everywhere(), 0.7)
        for x, y in ((52, 120), (258, 106), (160, 98)):
            cv.glow(cv.ellipse(x, y, 8, 8), '#ffb060', 20, 0.25)
    cv.vignette(0.3)
    return cv


# ---------------------------------------------------------------- 3 Bix's workshop
def workshop():
    cv = Canvas(bg='#100808')
    wall = cv.rect(0, 0, W, 116)
    cv.fill(wall, planks(cv, cv.X, cv.Y, '#3a2010', '#6a4024', 10, along='v'))
    cv.tint(wall, cv.vgrad([(0, '#909090'), (116, '#ffffff')])[..., 0])
    floor = cv.poly([(0, 116), (W, 116), (W, H), (0, H)])
    cv.fill(floor, planks(cv, cv.X + cv.Y * 0.4, cv.Y, '#4a2a14', '#7a4a24', 12))
    cv.fill(cv.rect(0, 114, W, 117), '#2a160a')
    for x, y, r in ((60, 30, 14), (88, 22, 8), (250, 34, 18), (276, 60, 9)):
        g = cv.ellipse(x, y, r, r)
        teeth = (np.sin(np.arctan2(cv.Y - y, cv.X - x) * 10) > 0) & (cv.ellipse(x, y, r + 3, r + 3) > 0.5)
        cv.fill(np.maximum(g, teeth * 1.0), '#c09040')
        cv.fill(cv.ellipse(x, y, r * 0.35, r * 0.35), '#3a2010')
        cv.bevel(g, 1.5, 0.6)
    # window
    win = cv.rect(130, 20, 190, 64)
    cv.fill(win, cv.vgrad([(20, '#6a3a9a'), (64, '#f0a0c0')]))
    window_frame(cv, 130, 20, 190, 64, frame='#3a2010', bars=(2, 2))
    # the workbench
    table(cv, 30, 150, 120, 22, 8, top='#6a4020', leg='#3a2010')
    for i, (x, c) in enumerate(((46, '#c0c8d8'), (70, '#d0a040'), (100, '#80a0c0'), (130, '#c04040'))):
        t = cv.rect(x, 108, x + 12, 118)
        cv.fill(t, c)
        cv.bevel(t, 1, 0.5)
    lamp_glow(cv, 90, 96, 30, '#ffd080', 0.25)
    # the junk pile (right)
    rng = np.random.default_rng(7)
    for i in range(24):
        x, y = rng.uniform(222, 300), rng.uniform(112, 146)
        w, h = rng.uniform(6, 16), rng.uniform(4, 10)
        j = cv.poly([(x - w, y + h), (x + w, y + h), (x + w * 0.7, y - h), (x - w * 0.6, y - h * 0.8)])
        cv.fill(j, ['#707888', '#a08050', '#506070', '#8a6a4a', '#9aa0aa', '#604a3a'][i % 6])
        cv.bevel(j, 1, 0.6)
    pile = cv.ellipse(262, 146, 46, 10)
    cv.tint(pile, 0.8)
    # the door (back to the square)
    door(cv, 10, 56, 38, 116, c0='#4a2a12', c1='#7a4a24')
    props.tetro_crates(cv, 158, 118, 6)
    props.gold_ring(cv, 176, 146)
    cv.vignette(0.35)
    return cv


# ---------------------------------------------------------------- 4 the Elder's hut
def elder():
    cv = Canvas(bg='#100808')
    m = cv.rect(0, 0, W, H)
    cv.fill(m, cv.rgrad(160, 90, 210, '#8a5a30', '#1a0c06'))
    weave = ((np.sin(cv.X * 0.5 + cv.Y * 0.2) * np.sin(cv.Y * 0.8)) > 0)
    cv.tint(m, np.where(weave, 1.08, 0.88))
    for i in range(9):
        cv.fill(cv.line([(i * 40, 168), (160, -10)], 2), '#3a1c0c', 0.6)
    fl = cv.ellipse(160, 186, 230, 64)
    cv.fill(fl, cv.texture('#4a2a14', '#6a4022', 3, 3, 4))
    rug = cv.ellipse(170, 150, 70, 12)
    cv.fill(rug, cv.texture('#7a1a4a', '#b04070', 2, 3, 5))
    cv.fill(rug * (np.abs(cv.Y - 150) > 7), '#e0b040', 0.6)
    # the ancient tablet with the Guru Meditation
    tab = cv.poly([(184, 24), (312, 24), (314, 90), (182, 90)])
    cv.fill(tab, cv.texture('#3a3540', '#5a5460', 2, 4, 12, 1.6))
    cv.bevel(tab, 2, 0.6)
    box = cv.rect(190, 32, 306, 82) * (1 - cv.rect(193, 35, 303, 79))
    cv.fill(box, '#ff2010')
    cv.glow(box, '#ff3010', 6, 0.4)
    cv.fill(text_mask(cv, 248, 42, 'GURU MEDITATION', 1.0, True), '#ff3020')
    cv.fill(text_mask(cv, 248, 60, '#00000004', 1.0, True), '#ff3020')
    props.blink(cv, box, '#ff3010', '#300400', 14, 'guru')
    # candles
    cand = np.zeros((cv.h, cv.w), np.float32)
    for x in (186, 314):
        cv.fill(cv.rect(x - 2, 104, x + 2, 122), '#e0e0c0')
        cand = np.maximum(cand, cv.ellipse(x, 101, 2, 3.5))
    cv.glow(cand, '#ffa040', 34, 0.4)
    cv.fill(cand, '#fff0a0')
    props.flame(cv, cand)
    # shelves with pots
    cv.fill(cv.rect(96, 64, 150, 67), '#3a2010')
    for i, x in enumerate((102, 116, 130, 142)):
        p = cv.ellipse(x, 58, 5, 6)
        cv.fill(p, ['#a05030', '#5070a0', '#70a050', '#c0a040'][i])
        cv.shade_sphere(x, 58, 6, p, amb=0.5)
    # the arch to the library (west)
    ar = cv.rect(14, 48, 62, 132)
    cv.fill(np.maximum(ar, cv.ellipse(38, 48, 24, 16)), '#120804')
    cv.add(cv.rect(18, 70, 58, 132), '#6a4020', 0.15)
    bookshelf(cv, 20, 76, 56, 128, 3, seed=4)
    cv.tint(cv.rect(14, 40, 62, 132), 0.55)
    # the way out (south): light from outside at the bottom
    cv.glow(cv.rect(130, 164, 210, 168), '#ffc080', 18, 0.35)
    props.pipe_puzzle(cv, 104, 74)
    cv.vignette(0.35)
    return cv


# ---------------------------------------------------------------- 5 the library
def monkey_painting(cv, x0, y0, x1, y1):
    fr = cv.rect(x0 - 4, y0 - 4, x1 + 4, y1 + 4)
    cv.fill(fr, '#c09030')
    cv.bevel(fr, 2, 0.6)
    pic = cv.rect(x0, y0, x1, y1)
    cv.fill(pic, cv.vgrad([(y0, '#6aa0d0'), (y1, '#d0e0a0')]))
    cx = (x0 + x1) / 2
    body = cv.ellipse(cx, y1 - 10, 12, 10)
    cv.fill(body, '#7a4a24')
    for k, dx in enumerate((-12, 0, 12)):
        hx, hy = cx + dx, y1 - 26 - (4 if dx == 0 else 0)
        hd = cv.ellipse(hx, hy, 6, 6)
        cv.fill(hd, '#7a4a24')
        cv.fill(cv.ellipse(hx, hy + 1.5, 4, 3.5), '#e0b080')
        for s in (-1, 1):
            cv.fill(cv.ellipse(hx + s * 1.6, hy, 0.9, 1.1), '#101010')
            cv.fill(cv.ellipse(hx + s * 6, hy - 1, 1.8, 2), '#7a4a24')
    cv.fill(cv.line([(cx + 10, y1 - 6), (cx + 18, y1 - 14), (cx + 16, y1 - 22)], 1.4), '#7a4a24')


def library(book_taken=False):
    cv = Canvas(bg='#100808')
    m = cv.rect(0, 0, W, 120)
    cv.fill(m, cv.texture('#3a2416', '#5a3a22', 4, 3, 8))
    for i, x in enumerate((0, 74, 214, 270)):
        bookshelf(cv, x + 4, 14, x + 48 if x < 200 else x + 46, 116, 5, seed=i + 3)
    monkey_painting(cv, 134, 22, 186, 72)
    fl = cv.poly([(0, 118), (W, 118), (W, H), (0, H)])
    cv.fill(fl, planks(cv, cv.X + cv.Y * 0.5, cv.Y, '#3a2010', '#5a3418', 14))
    cv.fill(cv.rect(0, 116, W, 119), '#1a0c06')
    # the reading desk with the insult book
    table(cv, 104, 176, 134, 20, 8, top='#6a4020', leg='#3a2010')
    bk = cv.poly([(124, 122), (156, 122), (158, 128), (122, 128)])
    cv.fill(bk, '#a02020')
    cv.fill(cv.rect(126, 120, 154, 123), '#f0e8d0')
    cv.bevel(bk, 1, 0.5)
    # the lectern with Garden Lore
    lec = cv.poly([(226, 150), (246, 150), (240, 122), (232, 122)])
    cv.fill(lec, '#5a3418')
    cv.bevel(lec, 1, 0.5)
    lb = cv.poly([(222, 120), (250, 120), (246, 112), (226, 112)])
    cv.fill(lb, '#2a7a3a')
    cv.fill(cv.rect(228, 113, 244, 116), '#f0e8d0')
    lamp_glow(cv, 140, 110, 40, '#ffd080', 0.25)
    # the way back (east): an arch
    ar = cv.rect(286, 60, 320, 118)
    cv.fill(ar, '#1a0c06')
    cv.add(ar, '#ffa040', 0.15)
    cv.vignette(0.4)
    return cv


# ---------------------------------------------------------------- 6 the Moonflower garden
def moonflower(cv, x, y, bloom):
    stem = cv.line([(x, y), (x - 3, y - 30), (x + 2, y - 58)], 3)
    cv.fill(stem, '#2a7a3a')
    cv.bevel(stem, 1, 0.5)
    for s in (-1, 1):
        lf = cv.poly([(x, y - 20), (x + s * 24, y - 32), (x + s * 30, y - 24), (x + s * 8, y - 16)])
        cv.fill(lf, cv.texture('#1a5a2a', '#4aa04a', 1.5, 3, 3 + s))
        cv.bevel(lf, 1, 0.5)
    if bloom:
        glow = cv.ellipse(x + 2, y - 66, 26, 20)
        cv.glow(glow, '#c0e0ff', 26, 0.6)
        for i in range(10):
            a = i / 10 * 2 * np.pi
            px, py = x + 2 + np.cos(a) * 14, y - 66 + np.sin(a) * 9
            p = cv.ellipse(px, py, 9, 5)
            cv.fill(p, cv.rgrad(x + 2, y - 66, 24, '#ffffff', '#a0b8ff'))
            cv.bevel(p, 1, 0.4)
        c = cv.ellipse(x + 2, y - 66, 6, 4)
        cv.fill(c, '#ffe060')
        cv.glow(c, '#ffffa0', 10, 0.5)
    else:
        bud = cv.ellipse(x + 2, y - 66, 8, 12)
        cv.fill(bud, cv.texture('#3a6a8a', '#7aa0c0', 1.5, 3, 7))
        cv.bevel(bud, 1.5, 0.6)
        cv.fill(cv.line([(x + 2, y - 78), (x + 2, y - 56)], 0.8), '#20405a')


def garden(bloom=False):
    cv = Canvas()
    stronkie_sky(cv, 92, seed=23)
    meadow_ground(cv, 94, 21, '#2a3a58', '#5a7ab0')
    for x, h, s in ((20, 80, 2), (296, 74, 6)):
        alien_tree(cv, x, 110, h, s, leaves=('#3a1a6a', '#a070e0'))
    # the garden wall and the path north to the gorge
    wall = cv.rect(0, 96, 320, 110) * (1 - cv.rect(236, 90, 266, 112))
    cv.fill(wall, blocks(cv, cv.X, cv.Y, '#6a6070', '#9a90a0', 10, 5, '#2a2430'))
    cv.bevel(wall, 1, 0.5)
    path(cv, [(250, 112), (252, 100), (256, 90)], 14)
    # flower beds
    for x0, x1 in ((20, 110), (200, 300)):
        bed = cv.ellipse((x0 + x1) / 2, 128, (x1 - x0) / 2, 9)
        cv.fill(bed, cv.texture('#3a2010', '#5a3418', 1.5, 3, 4))
        flowers(cv, 24, x0 + 6, x1 - 6, 120, 134, seed=x0, cols=('#e0e8ff', '#a0c0ff', '#ffd0f0'))
    # the Great Moonflower in its round bed
    bed = cv.ellipse(160, 140, 30, 7)
    cv.fill(bed, blocks(cv, cv.X, cv.Y, '#7a7088', '#aaa0b8', 8, 4, '#3a3048'))
    cv.bevel(bed, 1.2, 0.5)
    moonflower(cv, 160, 138, bloom)
    flowers(cv, 30, 0, 320, 148, 166, seed=31, cols=('#e0e8ff', '#ffd0f0', '#ffffff'))
    props.gnome(cv, 124, 116)
    props.fireflies(cv, 20, 100, 300, 135, 10, 5, '#ffd0f0', '#503050')
    cv.vignette(0.3)
    return cv


# ---------------------------------------------------------------- 7 the gorge
def gorge():
    cv = Canvas()
    stronkie_sky(cv, 70, seed=29)
    # far side cliffs with the cave
    far = cv.poly([(170, 168), (176, 72), (220, 62), (320, 58), (320, 168)])
    cv.fill(far, cv.texture('#4a2a5a', '#7a5a8a', 3, 4, 7, 1.5))
    cv.bevel(far, 3, 0.5)
    cave = cv.ellipse(276, 96, 18, 22) * (cv.Y < 110)
    cv.fill(cave, '#0c0612')
    cv.glow(cave, '#60e0ff', 10, 0.25)
    # the chasm
    ch = cv.poly([(110, 168), (130, 80), (176, 72), (172, 168)])
    cv.fill(ch, cv.vgrad([(70, '#3a2a5a'), (168, '#05030a')]))
    # near side (where you stand)
    near = cv.poly([(0, 168), (0, 100), (90, 104), (132, 112), (124, 168)])
    cv.fill(near, cv.texture('#5a3a6a', '#8a6a9a', 3, 4, 9, 1.5))
    cv.bevel(near, 3, 0.5)
    top = cv.poly([(0, 112), (126, 116), (122, 168), (0, 168)])
    cv.fill(top, cv.texture('#5a2a7a', '#9a5ab8', 2, 3, 3), 0.9)
    # the zip line: posts and the cable
    cv.fill(cv.rect(100, 70, 104, 120), '#4a2c18')
    cv.fill(cv.rect(250, 66, 254, 92), '#4a2c18')
    cv.fill(cv.line([(102, 74), (176, 77), (252, 70)], 0.7), '#c8c8d0')
    cv.fill(cv.rect(84, 112, 98, 118), '#6a4a2a')          # the broken trolley
    cv.fill(cv.line([(86, 112), (92, 106), (98, 108)], 1), '#808890')
    flowers(cv, 16, 0, 110, 140, 166, seed=5)
    cv.vignette(0.3)
    return cv


# ---------------------------------------------------------------- 8 the crystal cave
def pixel_drawing(cv, x0, y0, x1, y1):
    """the unfinished pixel picture on the cave wall: a sunset, half done, with a palette"""
    cell = 3
    rng = np.random.default_rng(91)
    cols = ['#1a1a4a', '#4a2a8a', '#c04080', '#ff8040', '#ffd060', '#ffffff', '#40a060', '#2a6a3a']
    nx, ny = int((x1 - x0) / cell), int((y1 - y0 - 8) / cell)
    for j in range(ny):
        for i in range(nx):
            if i > nx * 0.62 + rng.integers(-2, 2):
                if (i + j) % 2 == 0:
                    cv.fill(cv.rect(x0 + i * cell, y0 + j * cell, x0 + i * cell + 0.6, y0 + j * cell + 0.6), '#6a6a7a')
                continue
            t = j / ny
            c = cols[min(4, int(t * 5))] if t < 0.7 else cols[6 + (i % 2)]
            dx, dy = i - nx * 0.35, j - ny * 0.62
            if dx * dx + dy * dy * 2 < 18:
                c = cols[4]
            cv.fill(cv.rect(x0 + i * cell, y0 + j * cell, x0 + (i + 1) * cell, y0 + (j + 1) * cell), c)
    for k, c in enumerate(cols):
        cv.fill(cv.rect(x0 + k * 7, y1 - 6, x0 + k * 7 + 6, y1), c)


def cave(has_crystal=True):
    cv = Canvas(bg='#08040c')
    m = cv.rect(0, 0, W, H)
    cv.fill(m, cv.texture('#1a0e2a', '#3a2a4a', 5, 4, 3, 1.4))
    for i in range(7):
        r = cv.ellipse(20 + i * 50, 0, 30, 30 + (i % 3) * 8)
        cv.fill(r, cv.texture('#2a1a3a', '#4a3a5a', 3, 3, i), 0.9)
    fl = cv.poly([(0, 120), (W, 112), (W, H), (0, H)])
    cv.fill(fl, cv.texture('#2a1a3a', '#4a3a5a', 3, 3, 11))
    # the wall drawing
    wallp = cv.rect(120, 28, 214, 92)
    cv.fill(wallp, '#3a3448')
    pixel_drawing(cv, 124, 32, 210, 90)
    rng = np.random.default_rng(5)
    for i in range(16):
        x = rng.uniform(10, 310)
        if 110 < x < 224:
            continue
        y = rng.uniform(112, 160)
        h = rng.uniform(10, 34)
        crystal(cv, x, y, h, h * 0.3, col=['#60e0ff', '#ff80e0', '#a0ff80'][i % 3],
                dark=['#104060', '#501040', '#204010'][i % 3], lean=rng.uniform(-0.4, 0.4), seed=i)
    if has_crystal:
        crystal(cv, 232, 152, 12, 4, col='#80f0ff', dark='#105070', seed=99)
    # the zip line back (west): light from the gorge
    cv.glow(cv.rect(0, 70, 8, 130), '#f0a0c0', 20, 0.4)
    cv.vignette(0.35)
    return cv


# ---------------------------------------------------------------- 9 the forest path
def sword_stone(cv, x, y):
    st = cv.poly([(x - 18, y), (x + 18, y), (x + 14, y - 16), (x - 12, y - 18)])
    cv.fill(st, cv.texture('#6a6470', '#9a94a0', 2, 4, 3, 1.5))
    cv.bevel(st, 2, 0.6)
    bl = cv.rect(x - 1.2, y - 40, x + 1.2, y - 16)
    cv.fill(bl, cv.hgrad([(x - 1.2, '#c0c8d8'), (x + 1.2, '#606878')]))
    cv.fill(cv.rect(x - 7, y - 42, x + 7, y - 40), '#c09030')
    cv.fill(cv.rect(x - 1.5, y - 50, x + 1.5, y - 42), '#5a3418')
    cv.fill(cv.ellipse(x, y - 51, 2.2, 2.2), '#c09030')
    cv.glow(cv.ellipse(x, y - 30, 4, 16), '#e0f0ff', 10, 0.25)


def forest_path():
    cv = Canvas()
    m = cv.rect(0, 0, W, H)
    cv.fill(m, cv.vgrad([(0, '#3a1a5a'), (100, '#8a4a90')]))
    for i, (x, h, s) in enumerate(((20, 150, 1), (80, 130, 2), (250, 140, 3), (300, 160, 4), (140, 110, 5), (200, 120, 6))):
        alien_tree(cv, x, 118 + (i % 2) * 6, h, s, leaves=('#2a1050', '#8040b0'))
    meadow_ground(cv, 112, 33, '#2a1048', '#6a3098')
    path(cv, [(160, 168), (170, 134), (180, 110)], 18)
    sword_stone(cv, 92, 140)
    flowers(cv, 20, 0, 320, 144, 166, seed=8)
    props.wood_sign(cv, 50, 100, 34, 14, ["IT'S DANGEROUS", 'TO GO ALONE!'])
    props.fireflies(cv, 0, 60, 320, 130, 8, 3)
    cv.vignette(0.35)
    return cv


# ---------------------------------------------------------------- 10 the deep forest
def deep_forest():
    cv = Canvas()
    m = cv.rect(0, 0, W, H)
    cv.fill(m, cv.vgrad([(0, '#0a1a3a'), (120, '#2a6a6a')]))
    cv.glow(cv.ellipse(160, 40, 60, 40), '#c0ffe0', 60, 0.35)
    for i, (x, h, s) in enumerate(((10, 168, 1), (60, 150, 2), (110, 140, 3), (210, 145, 4), (260, 160, 5), (310, 170, 6))):
        alien_tree(cv, x, 126, h, s, trunk='#1a3a3a', leaves=('#0a3a3a', '#40c0a0'))
    meadow_ground(cv, 118, 41, '#0a2a2a', '#2a8a7a')
    rng = np.random.default_rng(3)
    for i in range(14):               # glowing mushrooms
        x, y = rng.uniform(10, 310), rng.uniform(130, 162)
        r = rng.uniform(3, 6)
        cv.fill(cv.rect(x - r * 0.25, y - r, x + r * 0.25, y), '#e0e0c0')
        cap = cv.ellipse(x, y - r, r, r * 0.55) * (cv.Y < y - r + 1)
        col = ['#ff80e0', '#80e0ff', '#ffe080'][i % 3]
        cv.fill(cap, col)
        cv.glow(cap, col, 8, 0.35)
    for i in range(30):               # fireflies
        x, y = rng.uniform(0, 320), rng.uniform(20, 120)
        f = cv.ellipse(x, y, 0.8, 0.8)
        cv.glow(f, '#ffff80', 4, 0.6)
        cv.fill(f, '#ffffc0')
    flowers(cv, 30, 0, 320, 140, 166, seed=13, cols=('#a0ffe0', '#ffffff', '#ffc0f0'))
    props.fireflies(cv, 0, 20, 320, 120, 16, 7)
    cv.vignette(0.4)
    return cv


# ---------------------------------------------------------------- the title picture
def title():
    cv = Canvas()
    stronkie_sky(cv, 120, top='#05061a', mid='#2a1a5a', low='#8a4a90', seed=41, night=True)
    meadow_ground(cv, 124, 3, '#1a0a30', '#4a2068')
    hut(cv, 60, 138, 46, 24, roof='#3a1a3a', wall='#5a4040')
    hut(cv, 268, 136, 40, 22, roof='#3a1a3a', wall='#5a4040')
    starraven(cv, 170, 150, 0.55)
    for x in (60, 268):
        cv.glow(cv.ellipse(x, 128, 4, 4), '#ffb060', 14, 0.5)
    t1 = text_mask(cv, 160, 10, 'THE WORLD OF', 1.0, True)
    cv.glow(t1, '#80a0ff', 6, 0.5)
    cv.fill(t1, '#c0d0ff')
    t2 = text_mask(cv, 160, 24, 'STRONKIE II', 2.5, True)
    cv.fill(cv.blur(t2, 0.6), '#200a30', 0.9)
    cv.fill(t2, cv.vgrad([(24, '#fff0a0'), (44, '#ff8040')]))
    cv.glow(t2, '#ff8040', 8, 0.35)
    t3 = text_mask(cv, 160, 50, 'A Love on Stronkie', 1.0, True)
    cv.fill(t3, '#ffc0e0')
    ch = int(os.environ.get('WOS2_CHAPTER', '1'))
    if ch > 1:
        sub = ['', '', 'Chapter Two: The Star Shard', 'Chapter Three: The Red Door',
               'Chapter Four: The Other World', 'Chapter Five: Two Moons, One Heart'][ch]
        t6 = text_mask(cv, 160, 64, sub, 1.0, True)
        cv.fill(cv.blur(t6, 0.6), '#200a30', 0.9)
        cv.fill(t6, '#fff0a0')
    t5 = text_mask(cv, 160, 156, 'Press a key   -   F5: menu', 1.0, True)
    cv.fill(cv.blur(t5, 0.6), '#100518', 0.9)
    cv.fill(t5, '#e0d0ff')
    if os.environ.get('WOS2_DEMO'):
        t4 = text_mask(cv, 160, 64, 'DEMO', 1.6, True)
        cv.fill(cv.blur(t4, 0.6), '#200a30', 0.9)
        cv.fill(t4, '#ff6060')
    return cv


ROOM_ART = {
    'meadow': meadow, 'square': square, 'workshop': workshop, 'elder': elder,
    'library': library, 'garden': garden, 'gorge': gorge, 'cave': cave,
    'forest': forest_path, 'deep': deep_forest, 'night': lambda: square(True), 'title': title,
}
