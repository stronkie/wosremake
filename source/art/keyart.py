"""Key art for World of Stronkie remake: the loading screen and the title screen.

Painted (rendered) in full colour at 4x (1280 x 1024), with light, glow, haze,
fractal clouds and chrome letters, then scaled down to 320 x 256 and shown in
HAM6 (4096 colours) by the game.

    loading_art(ch) -> rgb float (256, 320, 3), panel info
    title_art(ch)   -> rgb float (256, 320, 3)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = '/usr/share/fonts/truetype/google-fonts/ofl'
F_BLACK = os.path.join(FONTS, 'archivoblack', 'ArchivoBlack-Regular.ttf')
F_ANTON = os.path.join(FONTS, 'anton', 'Anton-Regular.ttf')
K = 4                                   # supersampling
W, H = 320 * K, 256 * K


def rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def grid():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    return xs / K, ys / K               # in 320 x 256 units


X, Y = grid()


def over(c, col, a):
    a = np.clip(a, 0, 1)[..., None]
    return c * (1 - a) + np.asarray(col, np.float32) * a


def add(c, col, a):
    return c + np.asarray(col, np.float32) * np.clip(a, 0, None)[..., None]


def screen(c, col, a):
    col = np.asarray(col, np.float32) * np.clip(a, 0, None)[..., None]
    return 1 - (1 - c) * (1 - np.clip(col, 0, 1))


def blur(m, r):
    return ndimage.gaussian_filter(m, r * K)


def fbm(seed, scale, octaves=6, w=W, h=H, ridge=False):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    s = scale
    for _ in range(octaves):
        gh, gw = max(2, int(h / (s * K)) + 3), max(2, int(w / (s * K)) + 3)
        g = rng.random((gh, gw)).astype(np.float32)
        z = ndimage.zoom(g, (h / (gh - 2), w / (gw - 2)), order=3)[:h, :w]
        if ridge:
            z = 1 - np.abs(z * 2 - 1)
        out += z * amp
        tot += amp
        amp *= 0.5
        s /= 2
    return out / tot


def draw_mask(fn):
    im = Image.new('L', (W, H), 0)
    fn(ImageDraw.Draw(im), K)
    return np.asarray(im, np.float32) / 255


def poly(pts):
    return draw_mask(lambda d, k: d.polygon([(x * k, y * k) for x, y in pts], fill=255))


def ellipse(cx, cy, rx, ry):
    return np.clip(1 - (((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2), 0, 1) ** 0.0001 * \
        ((((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2) <= 1)


def disc(cx, cy, r, soft=0.4):
    d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    return np.clip((r - d) / soft + 0.5, 0, 1)


def vgrad(stops):
    ys = np.array([s[0] for s in stops], np.float32)
    cols = np.array([rgb(s[1]) for s in stops])
    out = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        out[..., i] = np.interp(Y, ys, cols[:, i])
    return out


# ------------------------------------------------------------------ pieces
def sky(top='#04021a', stops=None):
    stops = stops or [(0, top), (60, '#120a3c'), (120, '#3a1458'), (165, '#8a2a66'), (190, '#e0604a'),
                      (205, '#ffb070'), (256, '#ffd8a0')]
    c = vgrad(stops)
    # nebula: two fractal clouds
    n1 = fbm(11, 60, 7)
    n2 = fbm(23, 40, 7, ridge=True)
    neb = np.clip((n1 - 0.45) * 3, 0, 1) * np.clip(1 - Y / 170, 0, 1)
    c = screen(c, rgb('#ff3a9a') * 0.55, neb * (0.4 + n2 * 0.6))
    neb2 = np.clip((fbm(37, 50, 7) - 0.5) * 3.5, 0, 1) * np.clip(1 - Y / 150, 0, 1)
    c = screen(c, rgb('#30c0ff') * 0.5, neb2 * n2)
    # stars
    rng = np.random.default_rng(5)
    st = np.zeros((H, W), np.float32)
    n = 700
    xs, ys = rng.integers(0, W, n), (rng.random(n) ** 1.6 * H * 0.7).astype(int)
    st[ys, xs] = rng.random(n) ** 2 * 3
    big = rng.random(n) > 0.97
    for x, y in zip(xs[big], ys[big]):
        for d in range(1, 7 * K):
            f = (1 - d / (7 * K)) ** 2 * 1.5
            for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    st[y + dy, x + dx] += f
    st = blur(st, 0.25) * 6
    st *= np.clip(1 - Y / 175, 0, 1)
    c = add(c, rgb('#ffffff'), st * 0.9)
    return c


def planet(c, cx, cy, r, base=('#2a3a8a', '#8ad0ff'), band=('#5a3aa0', '#c0a0ff'), sun=(-0.7, -0.4),
           rings=True, seed=3, tilt=-0.28):
    dx, dy = (X - cx) / r, (Y - cy) / r
    d2 = dx * dx + dy * dy
    m = np.clip((1 - np.sqrt(d2)) * r * 2, 0, 1)
    z = np.sqrt(np.clip(1 - d2, 0, 1))
    sx, sy = sun
    sz = np.sqrt(max(0.0, 1 - sx * sx - sy * sy))
    lam = np.clip(dx * sx + dy * sy + z * sz, 0, 1)
    # bands: latitude in the tilted frame + turbulence
    lat = dy * np.cos(tilt) - dx * np.sin(tilt)
    turb = fbm(seed, 20, 5) - 0.5
    b = np.sin((lat + turb * 0.25) * 14) * 0.5 + 0.5
    col = rgb(base[0]) * (1 - b[..., None]) + rgb(band[1]) * b[..., None] * 0.9
    col = col * 0.6 + rgb(base[1]) * (fbm(seed + 1, 12, 5)[..., None] - 0.3) * 0.5
    lit = col * (0.06 + 1.1 * lam[..., None] ** 0.9)
    rim = np.clip(1 - z, 0, 1) ** 3 * (lam > 0.02)
    lit = lit + rgb(base[1]) * rim[..., None] * 0.7
    # ring shadow lines
    ring = None
    if rings:
        rx, ry = 1.9, 0.42
        u = dx * np.cos(tilt) + dy * np.sin(tilt)
        v = -dx * np.sin(tilt) + dy * np.cos(tilt)
        rr = np.sqrt((u / rx) ** 2 + (v / ry) ** 2) * rx
        bandr = (rr > 1.25) & (rr < 1.85)
        stripes = 0.55 + 0.45 * np.sin(rr * 45) * np.sin(rr * 13 + 1)
        ra = bandr * stripes * np.clip((rr - 1.25) * 20, 0, 1) * np.clip((1.85 - rr) * 20, 0, 1)
        ring_col = rgb('#ffe0b0') * 0.9
        behind = (v < 0) & (d2 < 1)
        c = over(c, ring_col * (0.5 + 0.5 * np.clip(u * sx + 0.6, 0, 1))[..., None] if False else ring_col,
                 ra * 0.85 * ~(d2 < 1))
        ring = (ra, v, d2)
    # atmosphere glow
    halo = np.clip(1 - (np.sqrt(d2) - 1) * 8, 0, 1) * (d2 > 1) * np.clip(dx * sx + dy * sy + 0.4, 0, 1)
    c = add(c, rgb(base[1]), halo * 0.6)
    c = over(c, lit, m)
    if ring is not None:
        ra, v, d2_ = ring
        front = (v > 0)
        c = over(c, rgb('#ffe8c0') * 0.95, ra * 0.9 * front)
        # the ring's shadow on the planet
        c = c * (1 - (0.0 * m))[..., None]
    return c


def profile(seed, scale, octaves=5, sharp=1.0):
    """a 1D mountain line (0..1) over the width"""
    rng = np.random.default_rng(seed)
    xs = np.arange(W, dtype=np.float32) / K
    out = np.zeros(W, np.float32)
    amp, tot, s = 1.0, 0.0, scale
    for _ in range(octaves):
        n = int(320 / s) + 3
        g = rng.random(n).astype(np.float32)
        v = np.interp(xs / s, np.arange(n), g)
        v = 1 - np.abs(v * 2 - 1) if sharp > 1 else v
        out += v * amp
        tot += amp
        amp *= 0.45
        s /= 2.1
    return out / tot


def mountains(c, base_y, height, seed, col_top, col_bot, glow=None, scale=60, sharp=2, haze=None):
    pr = profile(seed, scale, 6, sharp)
    pr = (pr - pr.min()) / (pr.max() - pr.min() + 1e-6)
    prof = base_y - height * pr ** 1.3
    m = np.clip((Y - prof[None, :]) * K * 0.6, 0, 1)
    t = np.clip((Y - prof[None, :]) / max(height, 1), 0, 1)
    col = rgb(col_top) * (1 - t[..., None]) + rgb(col_bot) * t[..., None]
    # light from the right on the slopes
    slope = ndimage.gaussian_filter1d(np.gradient(prof) * K, 3 * K)[None, :]
    tex = fbm(seed + 3, 6, 4)
    col = col * (1 + np.clip(-slope * 1.5, -0.5, 0.5)[..., None] * np.exp(-t * 2)[..., None]) * (0.85 + tex[..., None] * 0.3)
    if glow is not None:
        edge = np.exp(-np.clip(Y - prof[None, :], 0, None) / 1.2) * (Y >= prof[None, :])
        col = col + rgb(glow) * edge[..., None] * 0.6
    if haze is not None:
        col = col * 0.75 + rgb(haze) * 0.25 * (1 - t[..., None])
    c = over(c, col, m)
    return c, prof


def crystals(c, seed, n, y0, y1, x0, x1):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        h = rng.uniform(10, 34) * (y - y0 + 20) / (y1 - y0 + 20)
        w = h * rng.uniform(0.18, 0.3)
        lean = rng.uniform(-0.3, 0.3) * h
        tip = (x + lean, y - h)
        left = poly([(x - w, y), tip, (x, y + 1)])
        right = poly([(x, y + 1), tip, (x + w, y)])
        c = add(c, rgb('#40e0ff'), blur(left + right, 4) * 0.35)
        c = over(c, rgb('#2a80c0'), left)
        c = over(c, rgb('#a0f8ff'), right * 0.9)
        c = over(c, rgb('#ffffff'), poly([(tip[0] - w * 0.15, tip[1] + h * 0.25), tip,
                                         (tip[0] + w * 0.1, tip[1] + h * 0.3)]) * 0.8)
    return c


def manor(c, x, y, s=1.0, lit=1.0):
    """a gothic manor silhouette on a cliff with warm windows"""
    sil = np.zeros((H, W), np.float32)
    parts = []
    def R(x0, y0, x1, y1):
        parts.append(poly([(x + x0 * s, y + y0 * s), (x + x1 * s, y + y0 * s), (x + x1 * s, y + y1 * s),
                           (x + x0 * s, y + y1 * s)]))
    def T(x0, x1, yb, yt):
        parts.append(poly([(x + x0 * s, y + yb * s), ((x + (x0 + x1) / 2 * s), y + yt * s), (x + x1 * s, y + yb * s)]))
    R(-30, -22, 30, 0)          # main house
    T(-34, 34, -22, -38)        # roof
    R(-44, -40, -30, 0)         # left tower
    T(-47, -27, -40, -66)
    R(30, -50, 42, 0)           # right tower
    T(28, 44, -50, -80)
    R(10, -48, 14, -36)         # chimney
    R(-12, -30, -8, -20)
    for p in parts:
        sil = np.maximum(sil, p)
    c = over(c, rgb('#0a0612'), sil)
    # rim light from the sky (right side)
    rim = np.clip(sil - ndimage.shift(sil, (0, -1.2 * K), order=1), 0, 1)
    c = add(c, rgb('#ff8a70'), rim * 0.5)
    wins = np.zeros((H, W), np.float32)
    for wx, wy in [(-22, -16), (-12, -16), (-2, -16), (8, -16), (18, -16), (-22, -8), (8, -8), (18, -8),
                   (-39, -32), (-39, -22), (34, -42), (34, -30), (34, -18), (-10, -27)]:
        wins = np.maximum(wins, poly([(x + (wx - 1.6) * s, y + (wy - 2.4) * s), (x + (wx + 1.6) * s, y + (wy - 2.4) * s),
                                      (x + (wx + 1.6) * s, y + (wy + 2.4) * s), (x + (wx - 1.6) * s, y + (wy + 2.4) * s)]))
    c = add(c, rgb('#ff9a30'), blur(wins, 3) * 1.2 * lit)
    c = over(c, rgb('#ffd070'), wins * lit)
    return c


def lightning(c, x0, y0, x1, y1, seed):
    rng = np.random.default_rng(seed)
    pts = [(x0, y0)]
    n = 14
    for i in range(1, n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t + rng.normal(0, 4) * (1 - t * 0.5), y0 + (y1 - y0) * t))
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    d.line([(px * K, py * K) for px, py in pts], fill=255, width=int(1.2 * K))
    # a branch
    b0 = pts[5]
    bp = [b0]
    for i in range(1, 6):
        bp.append((b0[0] - i * 4 + rng.normal(0, 2), b0[1] + i * 4))
    d.line([(px * K, py * K) for px, py in bp], fill=160, width=int(0.8 * K))
    m = np.asarray(im, np.float32) / 255
    c = add(c, rgb('#9a7aff'), blur(m, 10) * 3.5)
    c = add(c, rgb('#c0b0ff'), blur(m, 2.5) * 1.5)
    c = over(c, rgb('#ffffff'), m)
    return c


def ship(c, cx, cy, ang, sc=1.0, trail_to=None):
    """the STARRAVEN: a silver ship flying up and to the right"""
    ca, sa = np.cos(ang), np.sin(ang)
    def P(u, v):                    # ship coordinates (u forward, v up) -> picture
        return (cx + (u * ca - v * sa) * sc, cy - (u * sa + v * ca) * sc)
    # local coordinates of every pixel
    lx = ((X - cx) * ca - (cy - Y) * -sa) / sc
    lx = ((X - cx) * ca + (cy - Y) * sa) / sc
    ly = (-(X - cx) * sa + (cy - Y) * ca) / sc
    # exhaust: a long glowing trail behind
    if trail_to is not None:
        tx, ty = trail_to
        im = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(im)
        ex, ey = P(-34, 0)
        pts = []
        for i in range(41):
            t = i / 40
            mx = ex + (tx - ex) * t + np.sin(t * 3.0) * 18 * t
            my = ey + (ty - ey) * t ** 0.9
            pts.append((mx * K, my * K))
        for i in range(40):
            wdt = int((1.5 + i * 0.55) * K)
            d.line([pts[i], pts[i + 1]], fill=255, width=wdt)
        tm = np.asarray(im, np.float32) / 255
        cloud = fbm(77, 10, 6)
        smoke = blur(tm, 3) * (0.55 + cloud * 0.8)
        dist = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)
        warm = np.clip(1 - dist / 220, 0, 1)
        lit = np.clip((Y - ey) / max(1, ty - ey), 0, 1)[..., None]
        smoke_col = rgb('#b8a8d8') * (1 - lit) + rgb('#ffb080') * lit
        smoke_col = smoke_col * (0.7 + cloud[..., None] * 0.6)
        c = over(c, smoke_col, np.clip(smoke * 1.4, 0, 1) * 0.9)
        c = add(c, rgb('#ff9050'), blur(tm, 6) * (1 - warm) * 0.25)
        c = add(c, rgb('#80c0ff'), blur(tm, 2) * warm ** 3 * 0.9)
    # hull (fuselage): a long ellipse with a pointed nose
    hull = ((lx / 36) ** 2 + (ly / (7.2 - np.clip(lx, 0, 40) * 0.1)) ** 2 <= 1) & (lx > -34)
    hull = hull.astype(np.float32)
    wing = poly([P(-8, -2), P(-30, -22), P(-36, -22), P(-26, -2)])
    wing2 = poly([P(-8, 2), P(-24, 15), P(-30, 15), P(-24, 2)])
    fin = poly([P(-20, 5), P(-32, 16), P(-36, 16), P(-34, 5)])
    eng = poly([P(-38, -5), P(-31, -5), P(-31, 5), P(-38, 5)])
    shade_v = np.clip(ly / 8, -1, 1)
    metal = 0.55 + 0.45 * np.cos((shade_v - 0.35) * 2.2)          # a bright band on top
    metal = metal * (0.85 + 0.15 * np.sin(lx * 0.9))
    hullcol = np.stack([metal * 0.82, metal * 0.86, metal * 0.95], -1)
    hullcol = hullcol + rgb('#ff7a50')[None, None] * np.clip(-shade_v, 0, 1)[..., None] * 0.35   # warm light from below
    c = over(c, rgb('#5a6078'), wing2)
    c = over(c, rgb('#6a7088') * 0.8 + 0.15, fin)
    c = over(c, hullcol, blur(hull, 0.15))
    wl = np.clip((lx + 36) / 28, 0, 1)
    c = over(c, np.stack([0.35 + wl * 0.5, 0.38 + wl * 0.5, 0.48 + wl * 0.45], -1), wing)
    c = over(c, rgb('#e03040'), wing * (np.abs(lx + 30) < 1.6))
    # panel lines
    lines = (np.abs(np.sin(lx * 0.45)) < 0.06) * hull
    c = over(c, rgb('#2a3040'), lines * 0.5)
    # red stripe
    stripe = hull * (np.abs(ly + 1.5 - lx * 0.02) < 0.9) * (lx < 24)
    c = over(c, rgb('#e03040'), stripe)
    # cockpit
    cock = ((((lx - 18) / 9) ** 2 + ((ly - 2.8) / 3.0) ** 2) <= 1).astype(np.float32)
    glass = 0.35 + 0.65 * np.clip((ly - 2) / 3, 0, 1)
    c = over(c, np.stack([0.1 + glass * 0.5, 0.5 + glass * 0.4, 0.8 + glass * 0.2], -1), blur(cock, 0.1))
    c = add(c, rgb('#ffffff'), cock * np.clip(1 - np.abs(ly - 4.6) * 1.4, 0, 1) * 0.8)
    # the engine: flame + glow
    c = over(c, rgb('#303848'), eng)
    ex, ey = P(-38, 0)
    fl = np.clip(1 - np.sqrt(((lx + 38) / 22) ** 2 + (ly / 4.5) ** 2), 0, 1) * (lx < -36)
    c = add(c, rgb('#60a0ff'), blur(fl, 1.2) * 2.5)
    c = add(c, rgb('#ffffff'), fl ** 2 * 2)
    c = add(c, rgb('#4080ff'), disc(ex, ey, 1) * 0 + np.exp(-((X - ex) ** 2 + (Y - ey) ** 2) / (2 * (14 * sc) ** 2)) * 0.9)
    # a specular glint on the nose
    gx, gy = P(26, 4)
    c = add(c, rgb('#ffffff'), np.exp(-((X - gx) ** 2 + (Y - gy) ** 2) / 6) * 1.2)
    return c


def flare(c, x, y, size=1.0, col='#ffe0b0'):
    d2 = (X - x) ** 2 + (Y - y) ** 2
    c = add(c, rgb(col), np.exp(-d2 / (2 * (3 * size) ** 2)) * 2.0)
    c = add(c, rgb(col), np.exp(-d2 / (2 * (18 * size) ** 2)) * 0.5)
    streak = np.exp(-((Y - y) ** 2) / (2 * (0.6 * size) ** 2)) * np.exp(-np.abs(X - x) / (70 * size))
    c = add(c, rgb('#ffd0a0'), streak * 1.2)
    v = np.exp(-((X - x) ** 2) / (2 * (0.5 * size) ** 2)) * np.exp(-np.abs(Y - y) / (10 * size))
    c = add(c, rgb('#ffd0a0'), v * 0.4)
    return c


def text_mask(s, font, size, cx, y, track=0.0, sx=1.0):
    f = ImageFont.truetype(font, int(size * K))
    tmp = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(tmp)
    # letter by letter (tracking)
    widths = [d.textlength(ch, font=f) for ch in s]
    total = sum(widths) + track * K * (len(s) - 1)
    x = cx * K - total * sx / 2
    lay = Image.new('L', (int(total + 4 * K), int(size * K * 1.6)), 0)
    dl = ImageDraw.Draw(lay)
    xx = 0
    for ch, w_ in zip(s, widths):
        dl.text((xx, 0), ch, font=f, fill=255)
        xx += w_ + track * K
    if sx != 1.0:
        lay = lay.resize((int(lay.width * sx), lay.height), Image.LANCZOS)
    bbox = lay.getbbox()
    tmp.paste(lay, (int(x), int(y * K - bbox[1])), lay)
    return np.asarray(tmp, np.float32) / 255


def chrome(c, m, top='#e8f4ff', mid='#5a7ab8', low='#ffffff', edge='#1a1030', glow='#60a0ff', y0=0, y1=1, bevel=1.2):
    """metal letters: a dark outline, a bevel lit from the top left, a sky reflection"""
    ys = np.where(m.max(1) > 0.5)[0]
    ya, yb = (ys.min() / K, ys.max() / K) if len(ys) else (y0, y1)
    t = np.clip((Y - ya) / max(1, yb - ya), 0, 1)
    # the reflection (80s chrome): a blue sky above the horizon, a warm ground below
    tt = t[..., None]
    upper = rgb('#ffffff') * (1 - tt / 0.52) + rgb('#4a8aff') * (tt / 0.52)
    lower = rgb('#1a0a3a') * (1 - (tt - 0.52) / 0.48) + rgb('#ffb070') * np.clip((tt - 0.52) / 0.48, 0, 1) ** 1.3 * 1.2
    refl = np.where(tt < 0.52, upper, lower)
    line = np.exp(-((t - 0.535) ** 2) / 0.0004)
    refl = refl + rgb('#ffffff') * line[..., None] * 0.9
    # bevel lighting from a height map
    hgt = blur(m, bevel)
    gy, gx = np.gradient(hgt)
    light = np.clip(-(gx * -0.7 + gy * -0.7) * K * 3.5, -1, 1)
    out_m = np.clip(blur(m, 1.0) * 2.5, 0, 1)
    c = add(c, rgb(glow), blur(m, 8) * 0.55)
    c = over(c, rgb(edge), out_m)
    col = refl + light[..., None] * 0.45
    c = over(c, col, m)
    return c


def gold(c, m):
    ys = np.where(m.max(1) > 0.5)[0]
    ya, yb = ys.min() / K, ys.max() / K
    t = np.clip((Y - ya) / max(1, yb - ya), 0, 1)
    col = np.where(t[..., None] < 0.5, rgb('#fff2b0') * (1 - t[..., None]) + rgb('#ffb020') * t[..., None] * 2,
                   rgb('#b05a00') * (1 - (t[..., None] - 0.5)) + rgb('#ffd060') * (t[..., None] - 0.5) * 1.5)
    hgt = blur(m, 0.8)
    gy, gx = np.gradient(hgt)
    light = np.clip(-(gx * -0.7 + gy * -0.7) * K * 3.5, -1, 1)
    c = add(c, rgb('#ff8020'), blur(m, 6) * 0.5)
    c = over(c, rgb('#2a0a04'), np.clip(blur(m, 1.0) * 2.5, 0, 1))
    c = over(c, col + light[..., None] * 0.4, m)
    return c


def logo(c, cy, big=1.0):
    m1 = text_mask('THE WORLD OF', F_BLACK, 9 * big, 160, cy, track=2.2)
    c = chrome(c, m1, glow='#a060ff', bevel=0.8)
    m2 = text_mask('STRONKIE', F_BLACK, 31 * big, 160, cy + 12 * big, track=0.6)
    c = chrome(c, m2, bevel=1.6)
    m3 = text_mask('REMAKE', F_ANTON, 14 * big, 160, cy + 45 * big, track=4.0)
    c = gold(c, m3)
    # a star glint on the S
    sx = np.where(m2.max(0) > 0.5)[0]
    if len(sx):
        c = flare(c, sx.min() / K + 6, cy + 12 * big + 2, 0.7, '#e0f0ff')
    return c


def stronkiesoft(c, x, y, scale=1):
    im = Image.open(os.path.join(HERE, '..', 'images', 'stronkiesoft_logo.png')).convert('RGBA')
    w0, h0 = im.width, im.height
    im = im.resize((w0 * K * scale // 2, h0 * K * scale // 2), Image.NEAREST)
    a = np.asarray(im, np.float32) / 255
    h, w = a.shape[:2]
    x0, y0 = int(x * K), int(y * K)
    region = c[y0:y0 + h, x0:x0 + w]
    al = a[..., 3:4]
    sh = ndimage.shift(al[..., 0], (K, K), order=0)
    region[:] = region * (1 - sh[..., None] * 0.6)
    region[:] = region * (1 - al) + a[..., :3] * al
    return c


def cached(key, fn):
    """a painting (float 256 x 320 x 3), kept in source/.cache"""
    p = os.path.join(HERE, '..', '.cache', f'art_{key}_v1.npy')
    if os.path.exists(p):
        return np.load(p)
    a = down(fn())
    os.makedirs(os.path.dirname(p), exist_ok=True)
    np.save(p, a)
    return a


def down(c):
    c = np.clip(c, 0, 1)
    return c.reshape(256, K, 320, K, 3).mean((1, 3))


def vignette(c, k=0.35):
    d = ((X - 160) / 180) ** 2 + ((Y - 128) / 150) ** 2
    return c * (1 - np.clip(d - 0.35, 0, 1) * k)[..., None]


# ------------------------------------------------------------------ the pictures
PANEL_Y = 200                     # the loading screen's panel: lines 200-255


def dead_tree(c, x, y, h, seed, col='#06040c'):
    rng = np.random.default_rng(seed)
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    def br(x0, y0, ang, ln, wd, depth):
        x1, y1 = x0 + np.cos(ang) * ln, y0 - np.sin(ang) * ln
        d.line([(x0 * K, y0 * K), (x1 * K, y1 * K)], fill=255, width=max(1, int(wd * K)))
        if depth > 0:
            for _ in range(2):
                br(x1, y1, ang + rng.uniform(-0.8, 0.8), ln * rng.uniform(0.55, 0.75), wd * 0.65, depth - 1)
    br(x, y, np.pi / 2 + rng.uniform(-0.15, 0.15), h * 0.4, h * 0.06, 5)
    m = np.asarray(im, np.float32) / 255
    return over(c, rgb(col), m)


def launch_tower(c, x, y0, y1):
    m = np.zeros((H, W), np.float32)
    m = np.maximum(m, poly([(x - 3, y1), (x - 1.5, y0), (x + 1.5, y0), (x + 3, y1)]))
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    yy = y0
    while yy < y1 - 4:
        d.line([((x - 3) * K, yy * K), ((x + 3) * K, (yy + 5) * K)], fill=255, width=K // 2)
        d.line([((x + 3) * K, yy * K), ((x - 3) * K, (yy + 5) * K)], fill=255, width=K // 2)
        yy += 5
    d.line([(x * K, y0 * K), ((x + 12) * K, (y0 + 8) * K)], fill=255, width=K)
    m = np.maximum(m * 0.0, np.asarray(im, np.float32) / 255)
    m = np.maximum(m, poly([(x - 3.2, y0), (x - 2.4, y0), (x - 2.4, y1), (x - 3.2, y1)]))
    m = np.maximum(m, poly([(x + 2.4, y0), (x + 3.2, y0), (x + 3.2, y1), (x + 2.4, y1)]))
    c = over(c, rgb('#140c1c'), m)
    for yy in range(int(y0), int(y1), 9):
        c = add(c, rgb('#ff3030'), np.exp(-((X - x) ** 2 + (Y - yy) ** 2) / 1.2) * 1.5)
    return c


def loading_art():
    c = sky()
    c = planet(c, 262, 52, 30, seed=4)
    c = add(c, rgb('#e0e0ff'), disc(34, 132, 0) * 0)
    c = over(c, rgb('#c8c0e8'), disc(196, 30, 5.5) * (0.7 + 0.3 * fbm(8, 3, 4)))
    c = over(c, rgb('#1a0e3a'), disc(198.2, 28.6, 5.3) * 0.8)                     # a crescent
    c = add(c, rgb('#b0a0ff'), np.exp(-((X - 196) ** 2 + (Y - 30) ** 2) / 120) * 0.25)
    # three layers of mountains, far to near
    c, _ = mountains(c, 168, 34, 31, '#7a5ab0', '#3a2a70', glow='#ffb0d0', scale=70, haze='#ff80a0')
    c, _ = mountains(c, 178, 26, 52, '#3a2a78', '#1a1448', glow='#80e0ff', scale=45)
    c = crystals(c, 9, 9, 168, 186, 196, 318)
    c = add(c, rgb('#ff6080'), np.exp(-((Y - 184) / 7) ** 2) * 0.3)                # haze in the valley
    # the launch pad: fire light, the tower
    c = add(c, rgb('#ff9a40'), np.exp(-(((X - 140) / 46) ** 2 + ((Y - 188) / 10) ** 2)) * 1.1)
    c = launch_tower(c, 128, 146, 190)
    # the ship rising, its smoke down to the pad
    c = ship(c, 206, 104, 0.72, 1.25, trail_to=(138, 190))
    # the cliff with the manor on the left
    cliff = poly([(0, 118), (10, 116), (26, 118), (46, 120), (58, 126), (66, 140), (70, 158), (80, 176),
                  (92, 200), (0, 200)])
    rough = fbm(91, 4, 5)
    c = over(c, rgb('#140e26') * (0.6 + rough[..., None] * 0.8), cliff)
    rim = np.clip(cliff - ndimage.shift(cliff, (0, -1.6 * K), order=1), 0, 1)
    c = add(c, rgb('#ff8a70'), rim * 0.7)
    c = dead_tree(c, 60, 124, 34, 3)
    c = manor(c, 30, 119, 0.62)
    c = add(c, rgb('#ffa040'), np.exp(-(((X - 30) / 26) ** 2 + ((Y - 112) / 14) ** 2)) * 0.18)
    c = lightning(c, 96, 0, 74, 104, 4)
    # the foreground: a dark meadow with a warm rim
    gl = 190 + 4 * np.sin(X / 31) + 2.5 * np.sin(X / 11 + 2) + (fbm(5, 2, 3)[0][None, :] - 0.5) * 3
    hill = np.clip((Y - gl) * K * 0.5, 0, 1)
    c = over(c, rgb('#08060e'), hill)
    c = add(c, rgb('#ff9a70'), np.exp(-np.clip(Y - gl, 0, None) / 0.8) * hill * 0.6)
    c = vignette(c, 0.3)
    c = logo(c, 6)
    c = stronkiesoft(c, 3, 3, 1)
    return c


def title_art(chapter_name='', chapter_no=1, demo=False):
    c = sky(stops=[(0, '#02010c'), (90, '#0c0830'), (150, '#24104a'), (256, '#2a1248')])
    # the planet Stronkie from orbit, the sun rising over its edge
    pcx, pcy, pr = 150, 520, 360
    dx, dy = (X - pcx) / pr, (Y - pcy) / pr
    d = np.sqrt(dx * dx + dy * dy)
    m = np.clip((1 - d) * pr * 2, 0, 1)
    z = np.sqrt(np.clip(1 - d * d, 0, 1))
    # surface coordinates squeezed toward the edge (a sphere)
    u = dx / (z + 0.25)
    v = dy / (z + 0.25)
    land = ndimage.map_coordinates(fbm(61, 30, 7), [np.clip((v * 0.12 + 0.62) * (H - 1), 0, H - 1),
                                                    np.clip((u * 0.12 + 0.5) * (W - 1), 0, W - 1)], order=1)
    cl = ndimage.map_coordinates(fbm(62, 12, 7), [np.clip((v * 0.12 + 0.62) * (H - 1), 0, H - 1),
                                                  np.clip((u * 0.11 + 0.5) * (W - 1), 0, W - 1)], order=1)
    clouds = np.clip((cl - 0.52) * 2.6, 0, 1)
    ocean = rgb('#10306a') * (0.7 + z[..., None] * 0.4)
    green = rgb('#2a6a4a') * (0.7 + land[..., None] * 0.6)
    purple = rgb('#6a3a9a')
    col = np.where((land > 0.54)[..., None], np.where((land > 0.64)[..., None], purple, green), ocean)
    col = col * (1 - clouds[..., None] * 0.7) + rgb('#e8f0ff') * clouds[..., None] * 0.75
    lam = np.clip(-dx * 0.35 + -dy * 0.94 + 0.02, 0, 1)
    lit = col * (0.03 + lam[..., None] ** 0.8 * 0.95)
    c = over(c, lit, m)
    # the atmosphere: a thin blue line, a pink glow
    edge = (d - 1) * pr
    c = add(c, rgb('#5aa8ff'), np.exp(-edge ** 2 / (2 * 2.2 ** 2)) * np.clip(-dy * 1.4 + 0.2, 0, 1) * 1.4)
    c = add(c, rgb('#ff70b0'), np.exp(-np.clip(edge, 0, None) / 9) * (d > 1) * np.clip(-dy, 0, 1) * 0.45)
    c = add(c, rgb('#3a70ff'), np.exp(-np.clip(-edge, 0, None) / 6) * m * np.clip(-dy * 1.2, 0, 1) * 0.5)
    # the sun just over the edge
    c = flare(c, 232, 162, 1.3, '#fff0d0')
    # moons
    c = planet(c, 48, 104, 15, base=('#5a3a2a', '#ffc080'), band=('#8a5a3a', '#ffd0a0'), sun=(0.8, 0.5),
               rings=False, seed=12)
    c = planet(c, 288, 84, 8, base=('#3a4a5a', '#c0e0ff'), band=('#4a5a6a', '#e0f0ff'), sun=(-0.7, 0.6),
               rings=False, seed=19)
    # the ship, heading for the planet
    c = ship(c, 96, 140, -0.3, 0.95, trail_to=None)
    # dark at the bottom for the texts
    c = c * (1 - np.clip((Y - 196) / 22, 0, 1) * 0.72)[..., None]
    c = vignette(c, 0.25)
    c = logo(c, 10, 1.2)
    c = stronkiesoft(c, 3, 3, 1)
    return c


def title_text(img, chapter_name, chapter_no, demo):
    """the sharp texts at the bottom (in 320 x 256, uint8 rgb)"""
    import loading
    line1 = f'DISK {chapter_no}: {chapter_name.upper()}' if not demo else 'THE FREE DEMO'
    loading.prop_text(img, 160, 214, line1, (255, 216, 112), (20, 8, 40))
    loading.prop_text(img, 160, 230, 'Click or press a key  -  F5: menu', (224, 236, 255), (20, 8, 40))
    loading.prop_text(img, 160, 245, 'Created By Mark Stronks, Stronkie Soft', (150, 140, 200), (10, 4, 24))


if __name__ == '__main__':
    import sys
    a = down(loading_art())
    Image.fromarray((a * 255).astype(np.uint8)).resize((640, 512), Image.LANCZOS).save('/tmp/ka_load.png')
    sys.exit() if len(sys.argv)>1 else None
    b = down(title_art('The Prologue', 1))
    Image.fromarray((b * 255).astype(np.uint8)).resize((640, 512), Image.LANCZOS).save('/tmp/ka_title.png')
