"""The people of The World of Stronkie II as pixel sprites.

Every frame is drawn four times too big with plain shapes in palette colours
(16-31, the colours every room shares), shrunk by taking the most common
colour of each 4x4 block, and gets a black outline: the look of the LucasArts
games. Directions: 0 right, 1 left (the mirror), 2 front, 3 back."""
import math
import numpy as np
from PIL import Image, ImageDraw

K = 4                                  # drawing scale

BLACK, WHITE, DARK, YELLOW = 16, 17, 18, 19
SKIN, SKIN2, SILVER, BLUE = 20, 21, 22, 23
LBLUE, ORANGE, DORANGE, BROWN = 24, 25, 26, 27
NAVY, SBLUE, SLIGHT, GREEN = 28, 29, 30, 31

FIXED = ['#000', '#fff', '#112', '#fd4', '#fca', '#c86', '#dde', '#34b',
         '#8af', '#e72', '#943', '#642', '#335', '#47d', '#9cf', '#5d5']


class Pen:
    """a canvas of palette indices, 4x the sprite size; origin = between the feet"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new('L', (w * K, h * K), 0)
        self.d = ImageDraw.Draw(self.im)
        self.ox, self.oy = w / 2, h - 1

    def p(self, x, y):
        return ((self.ox + x) * K, (self.oy + y) * K)

    def ellipse(self, cx, cy, rx, ry, c):
        x0, y0 = self.p(cx - rx, cy - ry)
        x1, y1 = self.p(cx + rx, cy + ry)
        self.d.ellipse([x0, y0, x1, y1], fill=c)

    def poly(self, pts, c):
        self.d.polygon([self.p(x, y) for x, y in pts], fill=c)

    def rect(self, x0, y0, x1, y1, c):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], c)

    def limb(self, x0, y0, x1, y1, w, c):
        """a thick line with round ends"""
        a, b = self.p(x0, y0), self.p(x1, y1)
        self.d.line([a, b], fill=c, width=max(1, int(w * K)))
        r = w * K / 2
        for x, y in (a, b):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=c)

    def dot(self, x, y, c):
        x0, y0 = self.p(x - 0.5, y - 0.5)
        self.d.rectangle([x0, y0, x0 + K - 1, y0 + K - 1], fill=c)

    def finish(self, outline=True):
        a = np.asarray(self.im, np.int16).reshape(self.h, K, self.w, K).transpose(0, 2, 1, 3).reshape(self.h, self.w, K * K)
        out = np.zeros((self.h, self.w), np.int16)
        for y in range(self.h):
            for x in range(self.w):
                v = a[y, x]
                nz = v[v > 0]
                if len(nz) * 2 >= K * K * 0.75:          # mostly painted: the commonest colour
                    vals, cnt = np.unique(nz, return_counts=True)
                    out[y, x] = vals[cnt.argmax()]
        if outline:
            body = out > 0
            ring = np.zeros_like(body)
            ring[1:] |= body[:-1]
            ring[:-1] |= body[1:]
            ring[:, 1:] |= body[:, :-1]
            ring[:, :-1] |= body[:, 1:]
            out[ring & ~body] = BLACK
        out[out == 0] = -1
        return out


def mirror(fr):
    return fr[:, ::-1].copy()


# ---------------------------------------------------------------- humans
def human(look, view, t=0.0, talk=False, pose=None):
    """look: colours and shape; view 'side' (facing right), 'front', 'back';
    t: walk phase 0..1 (None = standing)"""
    P = Pen(30, look.get('h', 48) + 2)
    H = look.get('h', 48)
    s = H / 48.0
    hip = -21 * s
    sh = -34 * s                      # shoulders
    head_y = -40 * s
    walking = t is not None
    sw = math.sin(t * 2 * math.pi) if walking else 0.0
    skirt = look.get('skirt')
    if view == 'side':
        # back arm, back leg, body, front leg, front arm
        a1 = 0.45 * sw
        a2 = -0.45 * sw
        if pose == 'reach':
            a2, a1 = 1.3, 0.2
        if pose == 'dance':
            a2, a1 = 2.4, -0.6
        def leg(ang, c, cs):
            kx = math.sin(ang) * 10 * s
            ky = hip + math.cos(ang) * 10 * s
            lift = max(0, -math.sin(ang)) * 3 * s if walking else 0
            fx = kx + math.sin(ang * 0.5) * 9 * s
            fy = -1 - lift
            P.limb(0, hip, kx, ky, 4.4 * s, c)
            P.limb(kx, ky, fx, fy - 1, 4.0 * s, c)
            P.poly([(fx - 2 * s, fy - 2.5 * s), (fx + 4 * s, fy - 2.5 * s), (fx + 4 * s, fy), (fx - 2 * s, fy)], cs)
        def arm(ang, c):
            ex = math.sin(ang) * 6.5 * s
            ey = sh + 2 + math.cos(ang) * 6.5 * s
            hx = ex + math.sin(ang * 1.2 + 0.3) * 6 * s
            hy = ey + math.cos(ang * 1.2 + 0.3) * 6 * s
            P.limb(0.5, sh + 2, ex, ey, 3.8 * s, c)
            P.limb(ex, ey, hx, hy, 3.4 * s, c)
            P.ellipse(hx, hy, 1.8 * s, 1.8 * s, SKIN)
        arm(a1, look['sleeve2'])
        if skirt:
            P.limb(0, hip, 0 + sw * 3 * s, -2, 3.6 * s, SKIN2)
            P.limb(0, hip, 0 - sw * 3 * s, -2, 3.6 * s, SKIN)
            for k in (-1, 1):
                fx = k * sw * 3 * s
                P.poly([(fx - 2 * s, -3 * s), (fx + 3.5 * s, -3 * s), (fx + 3.5 * s, 0), (fx - 2 * s, 0)], look['shoes'])
            P.poly([(-4 * s, sh + 1), (4 * s, sh + 1), (8 * s + sw * s, -6 * s), (-8 * s + sw * s, -6 * s)], skirt)
            P.poly([(-8 * s + sw * s, -7 * s), (8 * s + sw * s, -7 * s), (8 * s + sw * s, -5 * s), (-8 * s + sw * s, -5 * s)], look['trim'])
        else:
            leg(-0.55 * sw, look['legs2'], look['shoes'])
        P.poly([(-4.5 * s, sh), (4.5 * s, sh), (4 * s, hip + 2), (-4 * s, hip + 2)], look['body'])
        P.poly([(1.5 * s, sh), (4.5 * s, sh), (4 * s, hip + 2), (1.5 * s, hip + 2)], look['body2'])
        if look.get('collar'):
            P.poly([(-1 * s, sh), (3 * s, sh), (1.5 * s, sh + 4 * s)], look['collar'])
        if not skirt:
            leg(0.55 * sw, look['legs'], look['shoes'])
        arm(a2, look['sleeve'])
        # head
        P.rect(-1.2 * s, head_y + 3 * s, 2 * s, sh + 1, SKIN2)          # neck
        P.ellipse(0.5 * s, head_y, 5.2 * s, 5.8 * s, SKIN)
        P.ellipse(4.8 * s, head_y + 0.8 * s, 1.4 * s, 1.6 * s, SKIN)       # nose
        look['hair_side'](P, s, head_y)
        P.dot(3 * s, head_y - 0.8 * s, BLACK)                            # eye
        if talk:
            P.rect(2.2 * s, head_y + 2.6 * s, 4.2 * s, head_y + 3.6 * s, BLACK)
        if look.get('pendant'):
            P.dot(2.5 * s, sh + 3.5 * s, look['pendant'])
    else:
        front = view == 'front'
        lift1 = max(0, sw) * 2.5 * s
        lift2 = max(0, -sw) * 2.5 * s
        armsw = sw * 1.5 * s
        if pose == 'dance':
            armsw = 0
        def legs():
            if skirt:
                for k, lf in ((-1, lift1), (1, lift2)):
                    P.poly([(k * 3.8 * s - 2.2 * s, -3 * s - lf), (k * 3.8 * s + 2.2 * s, -3 * s - lf),
                            (k * 3.8 * s + 2.2 * s, -lf), (k * 3.8 * s - 2.2 * s, -lf)], look['shoes'])
                return
            for k, lf in ((-1, lift1), (1, lift2)):
                P.limb(k * 2.6 * s, hip, k * 2.8 * s, -3 * s - lf, 4.2 * s, look['legs'] if k < 0 else look['legs2'])
                P.poly([(k * 2.8 * s - 2.3 * s, -3 * s - lf), (k * 2.8 * s + 2.3 * s, -3 * s - lf),
                        (k * 2.8 * s + 2.3 * s, -lf), (k * 2.8 * s - 2.3 * s, -lf)], look['shoes'])
        legs()
        if skirt:
            P.poly([(-5 * s, sh + 1), (5 * s, sh + 1), (9 * s, -4 * s), (-9 * s, -4 * s)], skirt)
            P.poly([(-9 * s, -6 * s), (9 * s, -6 * s), (9 * s, -3.5 * s), (-9 * s, -3.5 * s)], look['trim'])
        P.poly([(-6 * s, sh), (6 * s, sh), (5 * s, hip + 2), (-5 * s, hip + 2)], look['body'])
        if front and look.get('shirt'):
            P.poly([(-2 * s, sh), (2 * s, sh), (1.5 * s, hip + 2), (-1.5 * s, hip + 2)], look['shirt'])
        for k in (-1, 1):
            if pose == 'dance':
                P.limb(k * 6.5 * s, sh + 1.5, k * 9 * s, sh - 5 * s, 3.6 * s, look['sleeve'])
                P.ellipse(k * 9.5 * s, sh - 6.5 * s, 1.8 * s, 1.8 * s, SKIN)
                continue
            P.limb(k * 6.5 * s, sh + 1.5, k * 7.3 * s, hip + 1 + k * armsw, 3.6 * s, look['sleeve'])
            P.ellipse(k * 7.4 * s, hip + 2.5 * s + k * armsw, 1.8 * s, 1.8 * s, SKIN)
        P.rect(-1.6 * s, head_y + 3.5 * s, 1.6 * s, sh + 1, SKIN2)
        P.ellipse(0, head_y, 5.6 * s, 6.0 * s, SKIN)
        look['hair_front' if front else 'hair_back'](P, s, head_y)
        if front:
            P.dot(-2 * s, head_y - 0.5 * s, BLACK)
            P.dot(2 * s, head_y - 0.5 * s, BLACK)
            if talk:
                P.rect(-1.2 * s, head_y + 2.6 * s, 1.2 * s, head_y + 3.8 * s, BLACK)
            if look.get('pendant'):
                P.dot(0, sh + 3 * s, look['pendant'])
    return P.finish()


def pilot_hair_side(P, s, hy):
    P.poly([(-5 * s, hy - 1 * s), (-3 * s, hy - 6 * s), (2 * s, hy - 7 * s), (6 * s, hy - 4.5 * s),
            (5.5 * s, hy - 2.5 * s), (0, hy - 3.2 * s), (-1 * s, hy + 1.5 * s), (-4.8 * s, hy + 2.5 * s)], BROWN)


def pilot_hair_front(P, s, hy):
    P.poly([(-5.8 * s, hy + 0.5 * s), (-5 * s, hy - 5.5 * s), (0, hy - 7.2 * s), (5 * s, hy - 5.5 * s),
            (5.8 * s, hy + 0.5 * s), (4.5 * s, hy - 3 * s), (-2 * s, hy - 3.5 * s), (-4.5 * s, hy - 2 * s)], BROWN)


def pilot_hair_back(P, s, hy):
    P.ellipse(0, hy - 0.5 * s, 5.8 * s, 6.2 * s, BROWN)


def lyra_hair_side(P, s, hy):
    P.poly([(-6 * s, hy - 2 * s), (-2 * s, hy - 7 * s), (3 * s, hy - 6.5 * s), (5.5 * s, hy - 3.5 * s),
            (1 * s, hy - 3.5 * s), (-1 * s, hy + 3 * s), (-3 * s, hy + 12 * s), (-7 * s, hy + 14 * s), (-7 * s, hy + 4 * s)], SILVER)


def lyra_hair_front(P, s, hy):
    P.poly([(-6.5 * s, hy + 13 * s), (-6.5 * s, hy - 3 * s), (-3 * s, hy - 7 * s), (3 * s, hy - 7 * s),
            (6.5 * s, hy - 3 * s), (6.5 * s, hy + 13 * s), (4.6 * s, hy + 12 * s), (4.6 * s, hy - 2.5 * s),
            (-4.6 * s, hy - 2.5 * s), (-4.6 * s, hy + 12 * s)], SILVER)


def lyra_hair_back(P, s, hy):
    P.poly([(-6.5 * s, hy + 13 * s), (-6.5 * s, hy - 3 * s), (-3 * s, hy - 7 * s), (3 * s, hy - 7 * s),
            (6.5 * s, hy - 3 * s), (6.5 * s, hy + 13 * s)], SILVER)


PILOT = dict(h=48, body=ORANGE, body2=DORANGE, sleeve=ORANGE, sleeve2=DORANGE, shirt=WHITE, collar=WHITE,
             legs=NAVY, legs2=DARK, shoes=BLACK, hair_side=pilot_hair_side, hair_front=pilot_hair_front,
             hair_back=pilot_hair_back)
LYRA = dict(h=45, body=BLUE, body2=BLUE, sleeve=LBLUE, sleeve2=BLUE, skirt=BLUE, trim=LBLUE, shoes=SILVER,
            legs=SKIN, legs2=SKIN2, hair_side=lyra_hair_side, hair_front=lyra_hair_front,
            hair_back=lyra_hair_back, pendant=YELLOW)


LITE = set()           # costumes with a short walk cycle (two frames: less chip memory)


def costume_human(look, name=None):
    """-> frames list, stand[4], walk[4][6], talk[4][2], specials {name: [frames]}"""
    frames = []

    def add(f):
        frames.append(f)
        return len(frames) - 1
    stand, walk, talk = [], [], []
    for view in ('side', 'front', 'back'):
        st = human(look, view, None)
        if name in LITE:
            w2 = [human(look, view, 1 / 6.0), human(look, view, 4 / 6.0)]
            wk = [w2[i % 2] for i in range(6)]
        else:
            wk = [human(look, view, i / 6.0) for i in range(6)]
        tk = [st, human(look, view, None, talk=view != 'back')]
        if view == 'side':
            dirs = [(st, wk, tk, False), (st, wk, tk, True)]
        else:
            dirs = [(st, wk, tk, False)]
        for s_, w_, t_, mir in dirs:
            m = mirror if mir else (lambda f: f)
            stand.append(add(m(s_)))
            walk.append([add(m(f)) for f in w_])
            talk.append([add(m(f)) for f in t_])
    specials = {
        'reach': [add(human(look, 'side', None, pose='reach'))],
        'reachl': [add(mirror(human(look, 'side', None, pose='reach')))],
        'dance': [add(human(look, 'front', None, pose='dance')), add(human(look, 'front', 0.25, pose='dance')),
                  add(human(look, 'front', None, pose='dance')), add(human(look, 'front', 0.75, pose='dance'))],
    }
    return frames, stand, walk, talk, specials


# ---------------------------------------------------------------- Stronkies
def stronkie(view, t=None, talk=False, fur=SBLUE, light=SLIGHT, extra=None, h=26, pose=None):
    """small blue folk with long ears and big eyes"""
    P = Pen(26, h + 14)
    s = h / 26.0
    hop = abs(math.sin(t * 2 * math.pi)) * 2.2 * s if t is not None else 0
    by = -9 * s - hop
    if pose == 'jump':
        by -= 6 * s
    feet_sw = math.sin(t * 2 * math.pi) * 2 * s if t is not None else 0
    # feet
    for k in (-1, 1):
        P.ellipse(k * 3.5 * s + (feet_sw * k if view != 'side' else feet_sw * k), -1.5 * s - (hop if k * feet_sw > 0 else 0), 3 * s, 1.8 * s, fur)
    # ears
    if view == 'side':
        P.poly([(-1 * s, by - 13 * s), (-6 * s, by - 26 * s), (-3 * s, by - 26 * s), (2 * s, by - 13 * s)], fur)
        P.poly([(-0.5 * s, by - 14 * s), (-4.5 * s, by - 24 * s), (-3.4 * s, by - 24 * s), (1 * s, by - 14 * s)], light)
    else:
        for k in (-1, 1):
            P.poly([(k * 2 * s, by - 13 * s), (k * 8 * s, by - 26 * s), (k * 5 * s, by - 26.5 * s), (k * 5.5 * s, by - 13 * s)], fur)
            if view == 'front':
                P.poly([(k * 3 * s, by - 14 * s), (k * 7 * s, by - 24 * s), (k * 5.6 * s, by - 24 * s), (k * 4.8 * s, by - 14 * s)], light)
    # body: one round blob
    P.ellipse(0, by - 4 * s, 7.5 * s, 10 * s, fur)
    if view == 'front':
        P.ellipse(0, by - 1 * s, 4.5 * s, 6 * s, light)
    if view == 'side':
        P.ellipse(2 * s, by - 1 * s, 3.5 * s, 6 * s, light)
    if extra:
        extra(P, s, by, view)
    # eyes
    if view == 'front':
        for k in (-1, 1):
            P.ellipse(k * 2.8 * s, by - 8 * s, 2.4 * s, 2.8 * s, WHITE)
            P.dot(k * 2.6 * s, by - 7.5 * s, BLACK)
        if talk:
            P.ellipse(0, by - 3.5 * s, 1.5 * s, 1.2 * s, BLACK)
    elif view == 'side':
        P.ellipse(4 * s, by - 8 * s, 2.4 * s, 2.8 * s, WHITE)
        P.dot(5 * s, by - 7.5 * s, BLACK)
        if talk:
            P.rect(5 * s, by - 4 * s, 7 * s, by - 3 * s, BLACK)
    return P.finish()


def costume_stronkie(name=None, **kw):
    frames = []

    def add(f):
        frames.append(f)
        return len(frames) - 1
    stand, walk, talk = [], [], []
    for view in ('side', 'front', 'back'):
        st = stronkie(view, **kw)
        if name in LITE:
            w2 = [stronkie(view, t=1 / 6.0, **kw), stronkie(view, t=4 / 6.0, **kw)]
            wk = [w2[i % 2] for i in range(6)]
        else:
            wk = [stronkie(view, t=i / 6.0, **kw) for i in range(6)]
        tk = [st, stronkie(view, talk=view != 'back', **kw)]
        dirs = [False, True] if view == 'side' else [False]
        for mir in dirs:
            m = mirror if mir else (lambda f: f)
            stand.append(add(m(st)))
            walk.append([add(m(f)) for f in wk])
            talk.append([add(m(f)) for f in tk])
    specials = {'jump': [add(stronkie('front', pose='jump', **kw)), add(stronkie('front', **kw))]}
    return frames, stand, walk, talk, specials


def bix_extra(P, s, by, view):
    P.rect(-6 * s, by - 2 * s, 6 * s, by + 4 * s, BROWN)             # apron
    if view == 'front':
        P.rect(-7.5 * s, by - 10 * s, 7.5 * s, by - 8.5 * s, ORANGE)  # goggle strap
        for k in (-1, 1):
            P.ellipse(k * 2.8 * s, by - 9.5 * s, 2.6 * s, 2.6 * s, YELLOW)
    elif view == 'side':
        P.rect(-7.5 * s, by - 10 * s, 6.5 * s, by - 8.5 * s, ORANGE)
        P.ellipse(5.5 * s, by - 9.5 * s, 2.2 * s, 2.4 * s, YELLOW)


def zooma_extra(P, s, by, view):
    P.poly([(-7 * s, by - 5 * s), (7 * s, by - 5 * s), (8 * s, by + 6 * s), (-8 * s, by + 6 * s)], BLUE)   # shawl
    P.limb(8 * s, by - 6 * s, 9 * s, 0, 1.6 * s, BROWN)                                                  # stick


def gobbo_extra(P, s, by, view):
    P.rect(-7 * s, by - 3 * s, 7 * s, by + 2 * s, ORANGE)               # vest
    P.poly([(-6 * s, by - 13 * s), (6 * s, by - 13 * s), (4 * s, by - 18 * s), (-4 * s, by - 18 * s)], BROWN)   # hat
    P.rect(-8 * s, by - 13.5 * s, 8 * s, by - 12 * s, BROWN)


# ---------------------------------------------------------------- the white rabbit
def rabbit(t=None, talk=False):
    P = Pen(24, 22)
    hop = abs(math.sin(t * 2 * math.pi)) * 3 if t is not None else 0
    y = -hop
    P.ellipse(-2, y - 6, 6, 5, WHITE)                    # body
    P.ellipse(4, y - 11, 3.5, 3.5, WHITE)                # head
    P.poly([(3, y - 13), (2, y - 21), (4, y - 21), (5, y - 13)], WHITE)
    P.poly([(5, y - 13), (6, y - 20), (8, y - 20), (6.5, y - 13)], WHITE)
    P.poly([(3.3, y - 14), (2.8, y - 19), (3.6, y - 19), (4.3, y - 14)], SKIN)
    P.rect(-4, y - 9, 1, y - 3, BLUE)                    # waistcoat
    P.ellipse(-1.5, y - 5, 1.6, 1.6, YELLOW)             # the pocket watch
    P.ellipse(-8, y - 6, 1.6, 1.6, WHITE)                # tail
    for k in (-1, 1):
        P.ellipse(-1 + k * 2 + math.sin((t or 0) * 6.28) * 2 * k, -1, 2.2, 1.2, WHITE)
    P.dot(5.5, y - 12, BLACK)
    P.dot(7.3, y - 10.5, SKIN)
    if talk:
        P.dot(6.5, y - 9.5, BLACK)
    return P.finish()


def costume_rabbit():
    frames = []

    def add(f):
        frames.append(f)
        return len(frames) - 1
    st = rabbit()
    wk = [rabbit(i / 6.0) for i in range(6)]
    tk = [st, rabbit(talk=True)]
    stand, walk, talk = [], [], []
    for d in range(4):
        mir = d == 1
        m = mirror if mir else (lambda f: f)
        stand.append(add(m(st)))
        walk.append([add(m(f)) for f in wk])
        talk.append([add(m(f)) for f in tk])
    return frames, stand, walk, talk, {}


# ---------------------------------------------------------------- the people of the later chapters
def edmund_hair_side(P, s, hy):
    P.poly([(-5.4 * s, hy - 2 * s), (-4 * s, hy - 5 * s), (-1 * s, hy - 4 * s), (-1 * s, hy + 1 * s), (-5 * s, hy + 3 * s)], WHITE)
    P.poly([(2 * s, hy + 2.5 * s), (6 * s, hy + 2 * s), (5 * s, hy + 6.5 * s), (1 * s, hy + 6 * s)], WHITE)   # beard


def edmund_hair_front(P, s, hy):
    for k in (-1, 1):
        P.poly([(k * 5.8 * s, hy + 1 * s), (k * 5.6 * s, hy - 4 * s), (k * 3.5 * s, hy - 3 * s), (k * 4 * s, hy + 2 * s)], WHITE)
    P.poly([(-4 * s, hy + 2 * s), (4 * s, hy + 2 * s), (2.5 * s, hy + 7 * s), (-2.5 * s, hy + 7 * s)], WHITE)
    P.rect(-1.2 * s, hy + 2.6 * s, 1.2 * s, hy + 3.4 * s, SKIN2)


def edmund_hair_back(P, s, hy):
    P.poly([(-5.8 * s, hy - 3 * s), (5.8 * s, hy - 3 * s), (5.6 * s, hy + 3 * s), (-5.6 * s, hy + 3 * s)], WHITE)


def vex_hair_side(P, s, hy):
    P.poly([(-5.4 * s, hy), (-4 * s, hy - 6 * s), (3 * s, hy - 7 * s), (6 * s, hy - 4 * s), (0, hy - 4 * s),
            (-1 * s, hy + 1 * s), (-5 * s, hy + 3 * s)], BLACK)
    P.rect(2 * s, hy + 2.8 * s, 5.5 * s, hy + 3.4 * s, DARK)                 # a thin moustache


def vex_hair_front(P, s, hy):
    P.poly([(-5.8 * s, hy), (-5 * s, hy - 6 * s), (0, hy - 7.5 * s), (5 * s, hy - 6 * s), (5.8 * s, hy),
            (4.5 * s, hy - 4 * s), (0, hy - 5 * s), (-4.5 * s, hy - 4 * s)], BLACK)
    P.rect(-2.5 * s, hy + 2 * s, 2.5 * s, hy + 2.6 * s, DARK)


def vex_hair_back(P, s, hy):
    P.ellipse(0, hy - 0.5 * s, 5.8 * s, 6.2 * s, BLACK)


def queen_hair_side(P, s, hy):
    lyra_hair_side(P, s, hy)
    P.poly([(-3 * s, hy - 6.5 * s), (-2 * s, hy - 10 * s), (0, hy - 7.5 * s), (2 * s, hy - 10 * s), (3 * s, hy - 6.5 * s)], YELLOW)


def queen_hair_front(P, s, hy):
    lyra_hair_front(P, s, hy)
    P.poly([(-4 * s, hy - 6 * s), (-4 * s, hy - 10 * s), (-2 * s, hy - 8 * s), (0, hy - 11 * s), (2 * s, hy - 8 * s),
            (4 * s, hy - 10 * s), (4 * s, hy - 6 * s)], YELLOW)


def queen_hair_back(P, s, hy):
    lyra_hair_back(P, s, hy)
    P.rect(-4 * s, hy - 9 * s, 4 * s, hy - 6 * s, YELLOW)


def roger_hair_side(P, s, hy):
    P.poly([(-5 * s, hy - 1 * s), (-3 * s, hy - 6 * s), (2 * s, hy - 7 * s), (6 * s, hy - 4.5 * s),
            (0, hy - 3.5 * s), (-1 * s, hy + 1 * s), (-4.8 * s, hy + 2 * s)], YELLOW)


def roger_hair_front(P, s, hy):
    P.poly([(-5.8 * s, hy), (-5 * s, hy - 5.5 * s), (0, hy - 7.2 * s), (5 * s, hy - 5.5 * s), (5.8 * s, hy),
            (3 * s, hy - 3.5 * s), (-4 * s, hy - 2.5 * s)], YELLOW)


def roger_hair_back(P, s, hy):
    P.ellipse(0, hy - 0.5 * s, 5.8 * s, 6.2 * s, YELLOW)


EDMUND = dict(h=46, body=BROWN, body2=DARK, sleeve=BROWN, sleeve2=DARK, shirt=WHITE, collar=WHITE,
              legs=DARK, legs2=BLACK, shoes=BLACK, hair_side=edmund_hair_side, hair_front=edmund_hair_front,
              hair_back=edmund_hair_back)
VEX = dict(h=50, body=NAVY, body2=DARK, sleeve=NAVY, sleeve2=DARK, shirt=SILVER, collar=SILVER,
           legs=DARK, legs2=BLACK, shoes=BLACK, hair_side=vex_hair_side, hair_front=vex_hair_front,
           hair_back=vex_hair_back)
QUEEN = dict(h=46, body=WHITE, body2=SILVER, sleeve=WHITE, sleeve2=SILVER, skirt=WHITE, trim=YELLOW, shoes=SILVER,
             legs=SKIN, legs2=SKIN2, hair_side=queen_hair_side, hair_front=queen_hair_front,
             hair_back=queen_hair_back, pendant=LBLUE)
PILOTGUARD = dict(h=48, body=NAVY, body2=DARK, sleeve=NAVY, sleeve2=DARK, shirt=SKIN, collar=SKIN,
                  legs=DARK, legs2=BLACK, shoes=BLACK, hair_side=pilot_hair_side, hair_front=pilot_hair_front,
                  hair_back=pilot_hair_back)
ROGER = dict(h=47, body=SILVER, body2=SBLUE, sleeve=SILVER, sleeve2=SBLUE, shirt=WHITE, collar=None,
             legs=SBLUE, legs2=NAVY, shoes=BLACK, hair_side=roger_hair_side, hair_front=roger_hair_front,
             hair_back=roger_hair_back)


def quill_extra(P, s, by, view):
    P.poly([(-4 * s, by - 3 * s), (4 * s, by - 3 * s), (2 * s, by + 4 * s), (-2 * s, by + 4 * s)], WHITE)   # beard
    if view == 'front':
        for k in (-1, 1):
            P.ellipse(k * 2.8 * s, by - 8 * s, 3 * s, 3 * s, YELLOW)
            P.ellipse(k * 2.8 * s, by - 8 * s, 2 * s, 2.3 * s, WHITE)
    elif view == 'side':
        P.ellipse(4.5 * s, by - 8 * s, 2.8 * s, 3 * s, YELLOW)
        P.ellipse(4.5 * s, by - 8 * s, 1.9 * s, 2.2 * s, WHITE)
    P.rect(-9 * s, by - 2 * s, -5 * s, by + 4 * s, BROWN)                    # a big book


def guard_extra(P, s, by, view):
    P.poly([(-6 * s, by - 12 * s), (6 * s, by - 12 * s), (4 * s, by - 17 * s), (-4 * s, by - 17 * s)], YELLOW)   # helmet
    P.limb(8 * s, by - 20 * s, 8 * s, 0, 1.4 * s, SILVER)                                                     # spear
    P.poly([(8 * s, by - 26 * s), (10 * s, by - 20 * s), (6 * s, by - 20 * s)], WHITE)


PIRATE = dict(h=49, body=DORANGE, body2=BROWN, sleeve=DORANGE, sleeve2=BROWN, shirt=WHITE, collar=WHITE,
              legs=BLACK, legs2=DARK, shoes=BLACK, hair_side=vex_hair_side, hair_front=vex_hair_front,
              hair_back=vex_hair_back)     # World of Stronkie remake: LeChuckle's guard
SUITED = dict(PILOT, body=SILVER, body2=SBLUE, sleeve=SILVER, sleeve2=SBLUE, shirt=ORANGE, collar=SILVER,
              legs=SILVER, legs2=SBLUE)     # World of Stronkie remake: the silver flight suit

COSTUMES = {
    'suit': lambda: costume_human(SUITED, 'pilot'),
    'pilot': lambda: costume_human(PILOT, 'pilot'),
    'pirate': lambda: costume_human(PIRATE, 'pirate'),
    'lyra': lambda: costume_human(LYRA, 'lyra'),
    'pip': lambda: costume_stronkie('pip'),
    'bix': lambda: costume_stronkie('bix', extra=bix_extra),
    'zooma': lambda: costume_stronkie('zooma', fur=SILVER, light=WHITE, extra=zooma_extra, h=24),
    'gobbo': lambda: costume_stronkie('gobbo', extra=gobbo_extra),
    'rabbit': lambda: costume_rabbit(),
    'quill': lambda: costume_stronkie('quill', fur=BLUE, light=LBLUE, extra=quill_extra, h=24),
    'edmund': lambda: costume_human(EDMUND, 'edmund'),
    'vex': lambda: costume_human(VEX, 'vex'),
    'queen': lambda: costume_human(QUEEN, 'queen'),
    'roger': lambda: costume_human(ROGER, 'roger'),
    'pilotguard': lambda: costume_human(PILOTGUARD, 'pilotguard'),
    'guard': lambda: costume_stronkie('guard', fur=WHITE, light=SILVER, extra=guard_extra),
    'lumi': lambda: costume_stronkie('lumi', fur=WHITE, light=LBLUE, h=22),
    'sage': lambda: costume_stronkie('sage', fur=WHITE, light=SILVER, extra=zooma_extra, h=24),
}


def all_costumes(used=None, lite=()):
    LITE.clear()
    LITE.update(lite)
    return {k: f() for k, f in COSTUMES.items() if used is None or k in used}


def preview(path):
    """a sheet of every costume's frames, for looking at"""
    pal = np.zeros((32, 3), np.uint8)
    for i, c in enumerate(FIXED):
        c = c.lstrip('#')
        pal[16 + i] = [int(ch, 16) * 17 for ch in c]
    rows = []
    for name, (frames, *_rest) in all_costumes(sys.argv[2:] or None).items():
        h = max(f.shape[0] for f in frames)
        w = sum(f.shape[1] + 2 for f in frames)
        img = np.full((h, w, 3), 90, np.uint8)
        x = 0
        for f in frames:
            fh = f.shape[0]
            sub = img[h - fh:h, x:x + f.shape[1]]
            m = f >= 0
            sub[m] = pal[f[m]]
            x += f.shape[1] + 2
        rows.append(img)
    W = max(r.shape[1] for r in rows)
    out = np.full((sum(r.shape[0] + 4 for r in rows), W, 3), 60, np.uint8)
    y = 0
    for r in rows:
        out[y:y + r.shape[0], :r.shape[1]] = r
        y += r.shape[0] + 4
    Image.fromarray(out).resize((out.shape[1] * 3, out.shape[0] * 3), Image.NEAREST).save(path)


import sys
if __name__ == '__main__':
    preview(sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/people.png')
