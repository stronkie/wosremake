"""Little extra things painted into the rooms: something to look at, and a wink
to other games (and to the other Stronkie Soft games)."""
import numpy as np
from kit import crate, barrel, box3d                  # noqa: F401


def _txt(cv, x, y, t, scale, col):
    from rooms import text_mask
    cv.fill(text_mask(cv, x, y, t, scale, True), col)


def gta_poster(cv, x0, y0, w=18, h=20):
    """Grand Theft Glider VI: a sunset, a palm tree and a glider (pink and teal)"""
    x1, y1 = x0 + w, y0 + h
    p = cv.rect(x0, y0, x1, y1)
    cv.fill(p, cv.vgrad([(y0, '#ff4fa0'), (y0 + h * 0.55, '#ffb040'), (y1, '#20c0c0')]))
    cv.fill(cv.ellipse(x0 + w * 0.5, y0 + h * 0.55, w * 0.22, w * 0.22) * (cv.Y < y0 + h * 0.62), '#fff060')
    cv.fill(cv.rect(x0, y0 + h * 0.62, x1, y1), '#106a80')
    tx = x0 + w * 0.22
    cv.fill(cv.line([(tx, y1 - 1), (tx + 1, y0 + h * 0.35)], 0.8), '#201030')
    for s in (-1, 1):
        cv.fill(cv.line([(tx + 1, y0 + h * 0.35), (tx + 1 + s * 4, y0 + h * 0.42)], 0.7), '#201030')
        cv.fill(cv.line([(tx + 1, y0 + h * 0.35), (tx + 1 + s * 3, y0 + h * 0.28)], 0.7), '#201030')
    gx, gy = x0 + w * 0.68, y0 + h * 0.3
    cv.fill(cv.poly([(gx - 4, gy + 1), (gx, gy - 1.5), (gx + 4, gy + 1), (gx, gy)]), '#201030')
    cv.fill(cv.rect(x0, y0, x1, y0 + 4.2), '#201030')
    _txt(cv, x0 + w / 2, y0 + 0.6, 'VI', 0.36, '#ff70c0')
    cv.fill(cv.rect(x0 + 1, y1 - 3.5, x1 - 1, y1 - 0.8), '#201030')
    cv.bevel(p, 0.8, 0.4)


def mushroom(cv, x, y):
    """a red mushroom with white spots"""
    cv.fill(cv.rect(x - 2, y - 4, x + 2, y + 2), '#f0e0c8')
    cv.bevel(cv.rect(x - 2, y - 4, x + 2, y + 2), 0.6, 0.4)
    cap = cv.ellipse(x, y - 4, 6.5, 5) * (cv.Y < y - 3)
    cv.fill(cap, '#e02020')
    cv.bevel(cap, 1, 0.6)
    for dx, dy, r in ((-3, -6, 1.3), (2, -7, 1.6), (4.5, -4.5, 1)):
        cv.fill(cv.ellipse(x + dx, y + dy, r, r), '#ffffff')


def tetro_crates(cv, x0, y1, u=6):
    """crates in four odd shapes, stacked so one row is almost full"""
    cells = [((0, 0), '#40c0f0'), ((1, 0), '#40c0f0'), ((2, 0), '#40c0f0'), ((3, 0), '#40c0f0'),
             ((5, 0), '#f0d020'), ((6, 0), '#f0d020'), ((5, 1), '#f0d020'), ((6, 1), '#f0d020'),
             ((0, 1), '#c050e0'), ((1, 1), '#c050e0'), ((2, 1), '#c050e0'), ((1, 2), '#c050e0'),
             ((3, 1), '#f04040'), ((3, 2), '#f04040'), ((4, 2), '#f04040'), ((4, 3), '#f04040')]
    for (cx, cy), col in cells:
        b = cv.rect(x0 + cx * u, y1 - (cy + 1) * u, x0 + (cx + 1) * u - 0.5, y1 - cy * u - 0.5)
        cv.fill(b, col)
        cv.bevel(b, 1.2, 0.7)


def gold_ring(cv, x, y):
    r = cv.ellipse(x, y, 3.4, 2.4)
    cv.fill(r, cv.rgrad(x - 1, y - 1, 4, '#fff8a0', '#d09010'))
    cv.fill(cv.ellipse(x, y, 1.8, 1.1), '#3a2010')
    cv.glow(r, '#ffe060', 4, 0.4)


def pipe_puzzle(cv, x0, y0, n=5, u=7):
    """a framed pipe puzzle: tiles of pipe, one piece missing"""
    fr = cv.rect(x0 - 2, y0 - 2, x0 + n * u + 2, y0 + 3 * u + 2)
    cv.fill(fr, '#4a2c18')
    cv.bevel(fr, 1, 0.5)
    for i in range(n):
        for j in range(3):
            t = cv.rect(x0 + i * u, y0 + j * u, x0 + (i + 1) * u - 0.6, y0 + (j + 1) * u - 0.6)
            cv.fill(t, '#c8c0b0')
            cv.bevel(t, 0.6, 0.4)
    path = [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (4, 2)]
    pts = [(x0 + (i + 0.5) * u, y0 + (j + 0.5) * u) for i, j in path]
    cv.fill(cv.line(pts[:5], 2.2), '#30a040')
    cv.fill(cv.line(pts[5:], 2.2), '#30a040')
    cv.fill(cv.line(pts[:5], 0.8), '#80f080')


def gnome(cv, x, y):
    """a garden gnome with a red pointy hat"""
    body = cv.ellipse(x, y - 4, 3.2, 4)
    cv.fill(body, '#3050c0')
    cv.fill(cv.ellipse(x, y - 9, 2.4, 2.2), '#f0c8a0')
    cv.fill(cv.poly([(x - 3.6, y - 7), (x, y - 9.5), (x + 3.6, y - 7), (x, y - 5)]), '#f0f0f0')
    cv.fill(cv.poly([(x - 2.8, y - 10), (x + 2.8, y - 10), (x + 0.5, y - 17)]), '#e02020')
    cv.bevel(body, 0.8, 0.5)


def wood_sign(cv, x, y, w, h, lines, scale=0.42):
    cv.fill(cv.rect(x - 1, y + h / 2, x + 1, y + h / 2 + 12), '#4a2c18')
    b = cv.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    cv.fill(b, '#c8a070')
    cv.bevel(b, 1, 0.6)
    for i, t in enumerate(lines):
        _txt(cv, x, y - h / 2 + 1.5 + i * 6.2 * scale / 0.42, t, scale, '#3a2010')


def pickaxe(cv, x, y):
    """a pickaxe made of big square blocks"""
    s = 2.0
    for k in range(7):
        b = cv.rect(x + k * s * 0.7, y - k * s, x + k * s * 0.7 + s, y - k * s + s)
        cv.fill(b, '#7a5028' if k % 2 else '#5a3818')
    hx, hy = x + 6 * s * 0.7, y - 6 * s
    for dx, dy in ((-3, -1), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -1), (3, 0), (-4, 0)):
        b = cv.rect(hx + dx * s, hy + dy * s, hx + dx * s + s, hy + dy * s + s)
        cv.fill(b, '#60f0e0')
        cv.bevel(b, 0.5, 0.5)


def crowbar(cv, x, y):
    cv.fill(cv.line([(x, y), (x + 14, y - 3), (x + 16, y - 6)], 1.2), '#d02020')
    cv.fill(cv.line([(x, y), (x - 1.5, y + 1.5)], 1.2), '#d02020')


def pac_dots(cv, x0, x1, y):
    for x in np.arange(x0, x1, 8):
        cv.fill(cv.ellipse(x, y, 1.1, 0.8), '#ffe0a0')
    cv.fill(cv.ellipse(x1 + 3, y - 0.5, 1.6, 1.6), '#e02020')
    cv.fill(cv.ellipse(x1 + 6, y, 1.6, 1.6), '#e02020')
    cv.fill(cv.line([(x1 + 3, y - 2), (x1 + 5, y - 5), (x1 + 6, y - 1.5)], 0.5), '#30a030')


def medkit(cv, x, y):
    b = cv.rect(x - 7, y - 5, x + 7, y + 4)
    cv.fill(b, '#f0f0f0')
    cv.bevel(b, 1, 0.6)
    cv.fill(cv.rect(x - 1.2, y - 3.5, x + 1.2, y + 2.5), '#e02020')
    cv.fill(cv.rect(x - 4, y - 1.6, x + 4, y + 0.6), '#e02020')


def cake(cv, x, y):
    """a little cake with one candle, on a wall shelf"""
    cv.fill(cv.rect(x - 9, y + 1, x + 9, y + 2.5), '#6a6a78')
    c = cv.rect(x - 5, y - 5, x + 5, y + 1)
    cv.fill(c, '#5a2a14')
    cv.fill(cv.rect(x - 5, y - 6, x + 5, y - 4), '#f8f0f0')
    for dx in (-3, 0, 3):
        cv.fill(cv.ellipse(x + dx, y - 6.5, 1, 1), '#e02020')
    cv.fill(cv.rect(x - 0.4, y - 10, x + 0.4, y - 6.5), '#f0f0a0')
    cv.glow(cv.ellipse(x, y - 11, 0.8, 1.2), '#ffd060', 3, 0.8)


def fuzzy_dice(cv, x, y):
    cv.fill(cv.line([(x, y), (x - 2, y + 12)], 0.4), '#d0d0d0')
    cv.fill(cv.line([(x, y), (x + 3, y + 10)], 0.4), '#d0d0d0')
    for dx, dy in ((-2, 12), (3, 10)):
        d = cv.rect(x + dx - 2.4, y + dy, x + dx + 2.4, y + dy + 4.8)
        cv.fill(d, cv.texture('#ff60b0', '#ffb0e0', 1, 2, int(dx + 9)))
        for ex, ey in ((-1, 1.2), (1, 3.4), (0, 2.3)):
            cv.fill(cv.ellipse(x + dx + ex, y + dy + ey, 0.5, 0.5), '#ffffff')


def floor_message(cv, x, y):
    """a glowing orange scribble on the floor"""
    m = None
    rng = np.random.default_rng(7)
    for k in range(5):
        x0 = x + k * 7
        pts = [(x0 + i * 1.5, y + rng.uniform(-1.2, 1.2)) for i in range(4)]
        ln = cv.line(pts, 0.6)
        m = ln if m is None else np.maximum(m, ln)
    cv.glow(m, '#ff9020', 4, 0.8)
    cv.fill(m, '#ffd080')


def pink_car(cv, x, y):
    """a pink convertible with a palm tree on the door (side view, facing left)"""
    body = cv.poly([(x, y - 6), (x + 6, y - 9), (x + 18, y - 9), (x + 24, y - 14), (x + 34, y - 14),
                    (x + 40, y - 9), (x + 48, y - 8), (x + 48, y - 2), (x, y - 2)])
    cv.fill(body, cv.vgrad([(y - 14, '#ff80c8'), (y - 2, '#c02078')]))
    cv.bevel(body, 1, 0.6)
    cv.fill(cv.line([(x + 25, y - 14), (x + 28, y - 19)], 0.8), '#c0e0ff')
    cv.fill(cv.rect(x + 1, y - 6, x + 4, y - 4), '#fff8b0')
    for wx in (x + 9, x + 39):
        w = cv.ellipse(wx, y - 2, 4, 4)
        cv.fill(w, '#141418')
        cv.fill(cv.ellipse(wx, y - 2, 1.8, 1.8), '#c8c8d0')
    tx = x + 21
    cv.fill(cv.line([(tx, y - 3), (tx + 1, y - 8)], 0.6), '#106a50')
    for s in (-1, 1):
        cv.fill(cv.line([(tx + 1, y - 8), (tx + 1 + s * 2.5, y - 7)], 0.5), '#20c080')


def barrels(cv, x, y):
    barrel(cv, x, y, 5, 10)
    barrel(cv, x + 11, y, 5, 10)
    barrel(cv, x + 5.5, y - 10, 5, 10)


def lost_found(cv, x0, y1):
    """a box marked LOST + FOUND, with a green tunic and a pointy hat"""
    b = cv.rect(x0, y1 - 12, x0 + 34, y1)
    cv.fill(b, '#8a6a40')
    cv.bevel(b, 1, 0.6)
    cv.fill(cv.poly([(x0 + 6, y1 - 12), (x0 + 14, y1 - 18), (x0 + 22, y1 - 12)]), '#30a030')
    cv.fill(cv.poly([(x0 + 20, y1 - 12), (x0 + 30, y1 - 14), (x0 + 24, y1 - 22)]), '#40c040')
    cv.fill(cv.rect(x0 + 2, y1 - 9, x0 + 32, y1 - 4), '#e8e0c8')
    _txt(cv, x0 + 17, y1 - 9, 'LOST+FOUND', 0.3, '#3a2010')


def game_shelf(cv, x0, y0):
    """a shelf of game boxes: the Stronkie Soft collection (and one pink box)"""
    cv.fill(cv.rect(x0 - 2, y0 + 16, x0 + 50, y0 + 18), '#5a3418')
    cols = ['#3070e0', '#e04040', '#30a050', '#f0c020', '#8040c0', '#20b0c0', '#ff60b0']
    for k, c in enumerate(cols):
        bx = x0 + k * 7
        b = cv.rect(bx, y0 + (2 if k % 3 else 0), bx + 6, y0 + 16)
        cv.fill(b, c)
        cv.bevel(b, 0.6, 0.5)
        cv.fill(cv.rect(bx + 1, y0 + 7, bx + 5, y0 + 8), '#ffffff', 0.7)


def wanted_screen(cv, x0, y0):
    """a little screen with five stars"""
    s = cv.rect(x0, y0, x0 + 40, y0 + 12)
    cv.fill(s, '#101018')
    cv.bevel(s, 1, 0.6)
    for k in range(5):
        cx, cy = x0 + 5 + k * 7.5, y0 + 6
        pts = []
        for i in range(10):
            a = -np.pi / 2 + i * np.pi / 5
            r = 3 if i % 2 == 0 else 1.3
            pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
        cv.fill(cv.poly(pts), '#ffe040')


def ghost_poster(cv, x0, y0, w=34, h=30):
    """a poster for Ghost Zappers (another Stronkie Soft game)"""
    p = cv.rect(x0, y0, x0 + w, y0 + h)
    cv.fill(p, cv.vgrad([(y0, '#1a0a3a'), (y0 + h, '#4a1a6a')]))
    cv.bevel(p, 1, 0.5)
    gx, gy = x0 + w / 2, y0 + h * 0.52
    g = np.maximum(cv.ellipse(gx, gy, 7, 7) * (cv.Y < gy), cv.rect(gx - 7, gy, gx + 7, gy + 6))
    cv.fill(g, '#f0f0ff')
    for k in range(4):
        cv.fill(cv.poly([(gx - 7 + k * 3.5, gy + 6), (gx - 5.25 + k * 3.5, gy + 8.5), (gx - 3.5 + k * 3.5, gy + 6)]),
                '#f0f0ff')
    for dx in (-2.5, 2.5):
        cv.fill(cv.ellipse(gx + dx, gy - 1, 1.3, 1.8), '#1a0a3a')
    cv.fill(cv.line([(x0 + 3, y0 + h - 3), (gx - 8, gy + 2)], 0.8), '#60ff60')
    _txt(cv, gx, y0 + 1.5, 'GHOST', 0.34, '#60ff60')
    _txt(cv, gx, y0 + 5.5, 'ZAPPERS', 0.34, '#60ff60')


def frozen_cap(cv, x0, y0, w=24, h=20):
    """a red cap, frozen into a block of ice"""
    cap = cv.ellipse(x0 + w / 2, y0 + h * 0.6, 6, 4) * (cv.Y < y0 + h * 0.6)
    cv.fill(cap, '#e02020')
    cv.fill(cv.ellipse(x0 + w / 2 + 6, y0 + h * 0.6, 4, 1.4), '#c01818')
    cv.fill(cv.ellipse(x0 + w / 2, y0 + h * 0.6 - 2, 1.8, 1.4), '#ffffff')
    ice = cv.rect(x0, y0, x0 + w, y0 + h)
    cv.fill(ice, '#c0e8ff', 0.45)
    cv.bevel(ice, 1.2, 0.7)


def footprints(cv, x0, y0, n=5):
    """big footprints in the snow, running downhill"""
    for k in range(n):
        x, y = x0 + k * 13, y0 + (k % 2) * 6
        f = cv.ellipse(x, y, 4, 2.2)
        cv.fill(f, '#8a98c8', 0.7)
        for t in range(3):
            cv.fill(cv.ellipse(x + 3 + t * 0.2, y - 1.6 + t * 1.6, 1, 0.7), '#8a98c8', 0.7)


# ---------------------------------------------------------------- life: colour cycling
def flick(cv, key, m, cols, speed=4, regs=1, phase=None):
    """animate these pixels; things with the same key share the colour registers"""
    keys = cv.__dict__.setdefault('_akeys', {})
    sel = m > 0.35
    if not sel.any():
        return
    if key in keys:
        aid = keys[key]
        cv.anim[sel] = aid
        if phase is not None:
            cv.anims[aid - 1]['phase'][sel] = np.asarray(phase, np.float32)[sel] if np.ndim(phase) else phase
    else:
        keys[key] = cv.animate(np.where(sel, 1.0, 0.0), cols, speed=speed, regs=regs,
                               phase=None if phase is None else np.broadcast_to(
                                   np.asarray(phase, np.float32), (cv.h, cv.w)).copy())


def _dots(cv, pts, r):
    m = None
    for x, y in pts:
        e = cv.ellipse(x, y, r, r)
        m = e if m is None else np.maximum(m, e)
    return m


def twinkle(cv, x0, y0, x1, y1, n=14, seed=1):
    """extra stars that twinkle"""
    rng = np.random.default_rng(seed)
    pts = [(rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n)]
    m = _dots(cv, pts, 1.0)
    cv.fill(m, '#ffffff')
    ph = np.zeros((cv.h, cv.w), np.float32)
    for k, (x, y) in enumerate(pts):
        ph[cv.ellipse(x, y, 1.6, 1.6) > 0.2] = (k % 2) * 0.5 + 0.01
    flick(cv, 'twinkle', m, ['#ffffff', '#a0b0e0', '#404868', '#202438', '#808cc0'], speed=5, regs=2, phase=ph)


def fireflies(cv, x0, y0, x1, y1, n=12, seed=2, col='#ffff80', dim='#505020'):
    rng = np.random.default_rng(seed)
    pts = [(rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n)]
    m = _dots(cv, pts, 1.1)
    cv.glow(m, col, 4, 0.5)
    cv.fill(m, col)
    ph = np.zeros((cv.h, cv.w), np.float32)
    for k, (x, y) in enumerate(pts):
        ph[cv.ellipse(x, y, 1.8, 1.8) > 0.2] = (k % 2) * 0.5 + 0.01
    flick(cv, 'firefly', m, [col, col, dim, '#101008', dim], speed=6, regs=2, phase=ph)


def cursor(cv, x, y, w=3, h=4, col='#80ff80'):
    m = cv.rect(x, y, x + w, y + h)
    cv.fill(m, col)
    flick(cv, 'cursor', m, [col, col, '#101810', '#101810'], speed=8)


def flame(cv, m):
    flick(cv, 'flame', m, ['#fff0a0', '#ffc040', '#ff8020', '#ffd060', '#ffe080'], speed=3, regs=2,
          phase=(cv.X / 5) % 1)


def blink(cv, m, on, off, speed=10, key='blink'):
    flick(cv, key, m, [on, on, off, off], speed=speed)
