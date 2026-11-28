"""HAM6 for the Amiga: 4096 colours on screen, 16 base colours.

A HAM6 pixel (6 bits): control (bits 4-5) 00 = base colour (bits 0-3),
01 = keep red and green of the pixel on the left, set blue, 10 = set red,
11 = set green. Every line starts from colour 0 (the border).

    encode(img, keep=(), exact=None) -> (chunky uint8 h x w, palette 16 x 3 in 0..15)

img: float rgb 0..1, h x 320. keep: colours (0-255 rgb) that must be in the base
palette. exact: rows (bool, h) that may use base colours only (so a part of the
line can change later without changing the rest, e.g. a loading bar).
"""
import numpy as np

WT = np.array([0.30, 0.50, 0.20], np.float32)       # perceptual weights


def kmeans12(px, n, keep, iters=25, seed=1):
    rng = np.random.default_rng(seed)
    q = np.round(px * 15).astype(np.int16)
    cols, cnt = np.unique(q, axis=0, return_counts=True)
    cols = cols.astype(np.float32)
    w = cnt.astype(np.float32)
    k = n - len(keep)
    # start: the most used colours, spread out
    order = np.argsort(-w)
    cent = []
    for i in order:
        c = cols[i]
        if all(((c - d) ** 2).sum() > 6 for d in cent):
            cent.append(c)
        if len(cent) == k:
            break
    while len(cent) < k:
        cent.append(cols[rng.integers(len(cols))])
    cent = np.array(cent, np.float32)
    fixed = np.array(keep, np.float32).reshape(-1, 3)
    for _ in range(iters):
        allc = np.concatenate([cent, fixed]) if len(fixed) else cent
        d = (((cols[:, None] - allc[None]) ** 2) * WT).sum(2)
        lab = d.argmin(1)
        for j in range(k):
            m = lab == j
            if m.any():
                cent[j] = (cols[m] * w[m, None]).sum(0) / w[m].sum()
    pal = np.concatenate([np.round(cent), fixed]) if len(fixed) else np.round(cent)
    return np.clip(pal, 0, 15).astype(np.int16)


def encode(img, keep=(), exact=None, border=(0, 0, 0), diffuse=0.75):
    h, w, _ = img.shape
    keep = [tuple(int(round(v / 17)) for v in c) for c in keep]
    b12 = tuple(int(round(v / 17)) for v in border)
    if b12 not in keep:
        keep = [b12] + keep
    pal = kmeans12(img.reshape(-1, 3), 16, keep)
    # colour 0 = the border
    i0 = [tuple(p) for p in pal].index(b12)
    order = [i0] + [i for i in range(16) if i != i0]
    pal = pal[order]
    palf = pal.astype(np.float32)
    tgt = img.astype(np.float32) * 15
    out = np.zeros((h, w), np.uint8)
    err_next = np.zeros((w + 2, 3), np.float32)
    for y in range(h):
        row = tgt[y] + err_next[1:w + 1] * diffuse
        err_next = np.zeros((w + 2, 3), np.float32)
        prev = palf[0].copy()
        only_base = exact is not None and exact[y]
        carry = np.zeros(3, np.float32)
        for x in range(w):
            t = np.clip(row[x] + carry, 0, 15)
            tq = np.round(t)
            # candidates: 16 base colours, then modify b, r, g of prev
            d_base = (((palf - t) ** 2) * WT).sum(1)
            jb = int(d_base.argmin())
            best, val, col = d_base[jb], jb, palf[jb]
            if not only_base:
                cb = prev.copy(); cb[2] = tq[2]
                cr = prev.copy(); cr[0] = tq[0]
                cg = prev.copy(); cg[1] = tq[1]
                for code, ch, cc in ((1, 2, cb), (2, 0, cr), (3, 1, cg)):
                    e = (((cc - t) ** 2) * WT).sum()
                    if e < best - 1e-6:
                        best, val, col = e, (code << 4) | int(tq[ch]), cc
            out[y, x] = val
            prev = col
            e = (row[x] + carry) - col
            e = np.clip(e, -4, 4)
            carry = e * (7 / 16) * diffuse
            err_next[x] += e * (3 / 16)
            err_next[x + 1] += e * (5 / 16)
            err_next[x + 2] += e * (1 / 16)
    return out, pal


def decode(chunky, pal):
    h, w = chunky.shape
    out = np.zeros((h, w, 3), np.float32)
    for y in range(h):
        prev = pal[0].astype(np.float32)
        for x in range(w):
            v = int(chunky[y, x])
            c, d = v >> 4, v & 15
            if c == 0:
                prev = pal[d].astype(np.float32)
            else:
                prev = prev.copy()
                prev[{1: 2, 2: 0, 3: 1}[c]] = d
            out[y, x] = prev
    return out / 15
