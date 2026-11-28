#!/usr/bin/env python3
"""Builds World of Stronkie remake (the original World of Stronkie as a point-and-click
adventure on the World of Stronkie II engine): the rooms from the original pictures,
the original music, sound effects and speech, the scripts, the program:

    out/WOSR       the program            (vasm)
    out/WOSR.DAT   rooms, scripts, texts, sounds   (any memory)
    out/WOSR.STR   room pictures and speech, read from disk when needed
    out/WOSR.GFX   people, object pictures, instruments   (any memory; frames cached in chip)
    out/*.adf      the disk

    python3 build.py [all|data|engine|adf|preview]"""
import hashlib
import os
import struct
import subprocess
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'art'))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import zxpack                                    # noqa: E402
import wosdata as WD                             # noqa: E402
import music                                     # noqa: E402
import sndlib                                    # noqa: E402

DEMO = bool(os.environ.get('WOS2_DEMO'))
CH = int(os.environ.get('WOS2_CHAPTER', '1'))
OUT = os.path.join(HERE, 'out_demo' if DEMO else ('out' if CH == 1 else f'out_c{CH}'))
CACHE = os.path.join(HERE, '.cache')
VASM = os.environ.get('VASM', '/home/claude/amiga-toolkit/vasm/vasmm68k_mot')
TOOLKIT = os.environ.get('AMIGA_TK', '/home/claude/amiga-toolkit')
FONT = os.path.join(HERE, 'font8x8_basic.h')    # font8x8 (public domain), as WoS II uses it
VERSIONS = {n: 'V1.2' for n in range(1, 8)}
VERSION = VERSIONS[CH]
PREFIX = 'WOSR' if CH == 1 else f'WOSRC{CH}'        # the file names of this chapter's disk
CHAPTER_NAMES = {1: 'Chapter One: The Prologue', 2: 'Chapter Two: Into Space', 3: 'Chapter Three: Asteroid 42', 4: 'Chapter Four: Landfall', 5: 'Chapter Five: The Crystal Mountains', 6: 'Chapter Six: The Star Heart', 7: 'Chapter Seven: Vex\'s Flagship'}
DISK_NAME = f'WorldOfStronkieRemake_Chapter{CH}'


def volume_name(ch, demo=False):
    """the disk's name on the Workbench: chapter and version (AmigaDOS: 30 characters, no colon)"""
    v = f'Stronkie Remake {"Demo" if demo else f"Ch {ch}"} {VERSIONS[ch]}'
    assert len(v) <= 30 and ':' not in v, v
    return v
WHD_INC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whdload', 'inc')
GAME_NAME = 'WorldOfStronkieRemake'
INTRO = os.path.join(TOOLKIT, 'intro', 'disk', 'SSIntro')    # the Stronkie Soft boot intro (packed)
ORIG = os.path.join(HERE, 'orig')

for d in (OUT, CACHE):
    os.makedirs(d, exist_ok=True)


def rgb_of(h):
    h = h.lstrip('#')
    if len(h) == 3:
        return np.array([int(c, 16) / 15 for c in h], np.float32)
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def word12(c):
    r, g, b = (int(round(float(v) * 15)) for v in np.clip(c, 0, 1))
    return r << 8 | g << 4 | b


# ================================================================ pictures
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16 - 0.47


MAX_CYC = 4                                 # colour registers a room may give to cycling


def anim_assign(cv):
    """the room's colour cycles: registers from 15 down -> (register per pixel or 0, cycles)"""
    anim = cv.anim[::2, ::2]
    assign = np.zeros(anim.shape, np.int16)
    cycles = []
    reg = 15
    for i, a in enumerate(cv.anims):
        sel = anim == i + 1
        n = a['regs']
        if not sel.any() or 15 - reg + n > MAX_CYC:
            continue
        rr = [reg - k for k in range(n)]
        reg -= n
        cols = [word12(cc) for cc in a['colours']]
        ph = a['phase'][::2, ::2]
        idx = np.clip((ph * n).astype(int), 0, n - 1) if n > 1 else np.zeros(anim.shape, int)
        for k, r in enumerate(rr):
            assign[sel & (idx == k)] = r
            rot = (k * len(cols)) // n
            cycles.append((r, max(1, int(a['speed']) * 2), cols[rot:] + cols[:rot]))
    return assign, cycles


def room_palette(cv, fixed):
    """16 colours for the room (k-means), next to the 16 every room shares; the top
    registers can go to colour cycles"""
    import paint
    c = cv.c.reshape(cv.h // 2, 2, cv.w // 2, 2, 3).mean((1, 3))
    assign, cycles = anim_assign(cv)
    used = len(cycles)
    px = c[assign == 0].reshape(-1, 3)
    keep = [rgb_of(k) for k in getattr(cv, 'keep', ())]    # colours a room must have (small, important things)
    pal = paint.to12(paint.kmeans(px, 16 - used - len(keep)))
    if keep:
        pal = np.concatenate([pal, paint.to12(np.array(keep, np.float32))])
    pal = pal[np.argsort(pal.sum(1))]
    if len(pal) < 16 - used:                # (a picture with few colours: fill up with black)
        pal = np.concatenate([np.zeros((16 - used - len(pal), 3), np.float32), pal])
    pal[0] = 0                              # the border: black
    pal16 = np.zeros((16, 3), np.float32)
    pal16[:16 - used] = pal
    for r, _, cols in cycles:
        w = cols[0]
        pal16[r] = [(w >> 8 & 15) / 15, (w >> 4 & 15) / 15, (w & 15) / 15]
    return np.concatenate([pal16, fixed]), c, cycles


def quantize(c, pal32, dither=0.04, cv=None, cycles=()):
    h, w, _ = c.shape
    thr = BAYER[np.arange(h)[:, None] % 4, np.arange(w)[None, :] % 4]
    cd = c + thr[..., None] * dither
    wgt = np.array([0.30, 0.59, 0.11]) * 3
    best = np.zeros((h, w), np.int16)
    bd = np.full((h, w), 1e9, np.float32)
    skip = {r for r, _, _ in cycles}
    for j, p in enumerate(pal32):
        if j in skip:
            continue
        d = (((cd - p) ** 2) * wgt).sum(2)
        m = d < bd
        bd[m] = d[m]
        best[m] = j
    if cv is not None and cycles:
        assign, _ = anim_assign(cv)
        best[assign > 0] = assign[assign > 0]
    return best


def preview_img(chunky, pal32):
    return Image.fromarray((pal32[chunky] * 255).astype(np.uint8))


def cached(key, fn):
    p = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest() + '.npz')
    if os.path.exists(p):
        z = np.load(p, allow_pickle=True)
        return z['v'].item()
    v = fn()
    np.savez(p, v=np.array(v, dtype=object))
    return v


ART_FILES = ('orig.py', 'paint.py', 'rooms.py', 'kit.py')


def room_art(art):
    """the picture of a room: an original World of Stronkie picture (art/orig.py)"""
    import orig
    return orig.ROOM_ART[art], 'orig.py'


def art_key(name):
    src = ''.join(open(os.path.join(HERE, 'art', f)).read() for f in ART_FILES)
    pics = b''.join(open(os.path.join(ORIG, f), 'rb').read() for f in sorted(os.listdir(ORIG)) if f.endswith('.png'))
    return hashlib.sha1(src.encode() + pics + name.encode()).hexdigest()


def variants():
    import game
    return game.VARIANTS


def paint_room(art, fixed):
    def make():
        base_kw = {}
        for img, (a, bk, vk) in variants().items():
            if a == art:
                base_kw = bk
        if art == 'black':
            return dict(chunky=np.zeros((168, 320), np.int16),
                        pal32=np.concatenate([np.zeros((16, 3), np.float32), fixed]), images={})
        fn = room_art(art)[0]
        cv = fn(**base_kw) if base_kw else fn()
        pal32, c, cycles = room_palette(cv, fixed)
        chunky = quantize(c, pal32, cv=cv, cycles=cycles)
        images = {}
        for img, (a, bk, vk) in variants().items():
            if a != art:
                continue
            cv2 = fn(**vk)
            c2 = cv2.c.reshape(cv2.h // 2, 2, cv2.w // 2, 2, 3).mean((1, 3))
            ch2 = quantize(c2, pal32, cv=cv2, cycles=cycles)
            diff = np.argwhere(ch2 != chunky)
            if len(diff) == 0:
                continue
            y0, x0 = diff.min(0)
            y1, x1 = diff.max(0) + 1
            images[img] = (int(x0), int(y0), ch2[y0:y1, x0:x1].copy())
        return dict(chunky=chunky, pal32=pal32, images=images, cycles=cycles)
    vk = repr(sorted((k, repr(v)) for k, v in variants().items() if v[0] == art))
    tk = (('|demo' if DEMO else '') + ('' if CH == 1 else f'|ch{CH}')) if art == 'title' else ''
    return cached('room|' + art + '|' + art_key(art) + tk + '|v4|' + vk, make)


# ================================================================ walk masks
def walk_mask(room, polys, blocks):
    from PIL import ImageDraw
    im = Image.new('L', (320, 168), 0)
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon(p, fill=255)
    for p in blocks:
        d.polygon(p, fill=0)
    a = np.asarray(im)
    cells = a[2::4, 2::4][:42, :80] > 0
    out = bytearray()
    for y in range(42):
        out += np.packbits(cells[y].astype(np.uint8)).tobytes()
    return bytes(out), cells


# ================================================================ speech
SPEECH = {   # the spoken lines of the original game (orig/sound/say_*.spk, sampled from the V2.4 disks)
    'Welcome to the World of Stronkie!': 'say_welcome',
    'Prologue, Part 2: The Manor': 'say_p2',
    'Prologue, Part 3: The Launch Pad': 'say_p3',
    'Chapter 1: Into Space': 'say_c1',
    'Congratulations!': 'say_congrats',
}
SFX = {'pickup': 'take'}           # sound name in the game -> the original's sampled effect


FIB = [-34, -21, -13, -8, -5, -3, -2, -1, 0, 1, 2, 3, 5, 8, 13, 21]


def spk_decode(b):
    """.w samples, .w period, Fibonacci delta data -> (samples, period)"""
    n, per = struct.unpack('>HH', b[:4])
    d = b[4:]
    cur = d[0] - 256 if d[0] > 127 else d[0]
    out = []
    for x in d[1:1 + (n + 1) // 2]:
        for nib in (x >> 4, x & 15):
            cur += FIB[nib]
            out.append(cur)
    return np.array(out[:n], np.float64), per


SPEECH_GAIN = 2.6       # the original speech samples are soft (RMS ~20 of 127): louder, with a soft limiter


def speech_clip(text, voice, speed):
    """the original's speech sample for this line, made louder: .w samples, .w period, Fibonacci delta data"""
    import game
    name = SPEECH.get(text) or game.EXTRA_SPEECH[text]
    x, per = spk_decode(open(os.path.join(ORIG, 'sound', name + '.spk'), 'rb').read())
    y = np.tanh(x / 127 * SPEECH_GAIN) / np.tanh(SPEECH_GAIN) * 124
    y = np.round(y).astype(np.int16)
    if len(y) % 2:
        y = y[:-1]
    return struct.pack('>HH', len(y), per) + sndlib.fib_encode(y)


def orig_sfx(name):
    return open(os.path.join(ORIG, 'sound', SFX.get(name, name) + '.spk'), 'rb').read()


# ================================================================ the data file
def build_data():
    import game
    import people
    import icons
    G = game.G
    fixed = np.array([rgb_of(c) for c in people.FIXED])
    gfx = bytearray()
    A = []          # data.s lines
    E = A.append
    E('; WOS2.DAT - made by build.py, do not edit')
    E('base')
    E('        dc.b    "WOS2"')
    for lab in ('rooms', 'objects', 'actor_init', 'strings', 'songs', 'instruments', 'sounds', 'font',
                'verbs', 'defscripts', 'start', 'objinit', 'panelpal', 'fixedpal', 'storymap', 'storydef'):
        E(f'        dc.l    {lab}-base')

    # ---- costumes (frames in the chip file)
    used = {a[1] for a in game.ACTORS if a[1]}
    used |= set(getattr(game, 'EXTRA_COSTUMES', []))
    costumes = {k: v for k, v in people.all_costumes(used, getattr(game, 'LITE', ())).items() if k in used}
    frame_seen = {}
    frame_max_c = 0
    for name, (frames, stand, walk, talk, specials) in costumes.items():
        E(f'cost_{name}')
        E(f'        dc.l    frames_{name}-base')
        E('        dc.w    ' + ','.join(str(v) for v in stand))
        E(f'        dc.w    {len(walk[0])}')
        for d in range(4):
            w = list(walk[d]) + [walk[d][-1]] * (8 - len(walk[d]))
            E('        dc.w    ' + ','.join(str(v) for v in w[:8]))
        E('        dc.w    ' + ','.join(str(v) for d in range(4) for v in talk[d]))
        E(f'        dc.l    spec_{name}-base')
        actor_col = [a[2] for a in game.ACTORS if a[1] == name]
        E(f'        dc.w    {actor_col[0] if actor_col else 17}')
        E(f'frames_{name}')
        for f in frames:
            h, w = f.shape
            ys, xs = np.nonzero(f >= 0)
            y0, x0 = (ys.min(), xs.min()) if len(ys) else (0, 0)
            g = f[y0:ys.max() + 1, x0:xs.max() + 1] if len(ys) else f[:1, :1]
            ww, hh, data = WD.frame_bytes(g)
            hx, hy = w // 2 - x0, h - 1 - y0
            off = frame_seen.get(data)
            if off is None:
                off = frame_seen[data] = len(gfx)
                gfx += data
                frame_max_c = max(frame_max_c, len(data))
            E(f'        dc.w    {ww},{hh},{hx},{hy}')
            E(f'        dc.l    {off}')
        E(f'spec_{name}')
        names = G.specials.get(name, [])
        for i, sp in enumerate(names):
            E(f'        dc.l    spec_{name}_{i}-base')
        if not names:
            E('        dc.l    0')
        for i, sp in enumerate(names):
            fr = specials[sp]
            E(f'spec_{name}_{i}')
            E(f'        dc.w    {len(fr)},{4 if sp == "dance" else 6},' + ','.join(str(v) for v in fr))

    print('costume frames', len(gfx))
    # ---- the stream file (PREFIX.STR): room pictures and speech stay on disk and are
    # read when needed, so the game fits a 512K chip + 512K trapdoor Amiga 500.
    # Each piece: .l length, the data (even). Pointers to it: $80000000 + offset.
    stream = bytearray()
    smax = {'room': 0, 'spk': 0}

    def add_blob(data, kind):
        off = len(stream)
        stream.extend(struct.pack('>L', len(data)) + bytes(data))
        if len(stream) % 2:
            stream.append(0)
        smax[kind] = max(smax[kind], len(data))
        return off
    # ---- rooms
    room_data = {}
    for rname in G.room_order:
        R = G.rooms[rname]
        room_data[rname] = paint_room(R['art'], fixed)
        rd = room_data[rname]
        packed = zx_cached(WD.picture_bytes(rd['chunky']))
        pf = os.path.join(OUT, f'room_{rname}.bin')
        open(pf, 'wb').write(packed)
        rd['packed'] = len(packed)
        rd['stream'] = add_blob(packed, 'room')
    E('rooms')
    for rname in G.room_order:
        R = G.rooms[rname]
        rd = room_data[rname]
        pal = [word12(c) for c in rd['pal32'][:16]]
        E(f'        dc.l    ${0x80000000 + rd["stream"]:08x}')
        E('        dc.w    ' + ','.join(f'${p:03x}' for p in pal))
        E(f'        dc.l    {"walk_" + rname + "-base" if R["walk"] else 0}')
        E(f'        dc.l    objs_{rname}-base')
        E(f'        dc.l    {R["enter"].name + "-base" if R["enter"] else 0}')
        E(f'        dc.l    {R["timer"].name + "-base" if R["timer"] else 0}')
        E(f'        dc.w    {R["ticks"]}')
        E(f'        dc.w    {R["rmin"]},{R["rmax"]}')
        E(f'        dc.l    {R["random"].name + "-base" if R["random"] else 0}')
        E(f'        dc.w    {G.song_no(R["music"]) if R["music"] else 0}')
        E(f'        dc.l    {"cyc_" + rname + "-base" if rd.get("cycles") else 0}')
    for rname in G.room_order:
        cyc = room_data[rname].get('cycles')
        if cyc:
            E(f'cyc_{rname}')
            E(f'        dc.w    {len(cyc)}')
            for r, step, cols in cyc:
                E(f'        dc.w    {r},{step},{len(cols)},' + ','.join(f'${w:03x}' for w in cols))
    for rname in G.room_order:
        R = G.rooms[rname]
        E(f'objs_{rname}')
        nums = [G.obj(o) for o in R['objects']]
        E('        dc.w    ' + ','.join(str(n) for n in nums + [-1]))
        if R['walk']:
            data, cells = walk_mask(rname, R['walk'], game.BLOCK.get(rname, []))
            room_data[rname]['cells'] = cells
            E(f'walk_{rname}')
            A.extend(WD.asm_bytes(data))
        E('        even')

    # ---- objects
    E('objects')
    obj_images = {}
    obj_datas = []
    for i, oname in enumerate(G.obj_order):
        if oname is None:
            E('        dcb.b   40,0')
            continue
        o = G.objects[oname]
        box = o['box'] or (0, 0, -1, -1)
        wx, wy = o['walk'] if o['walk'] else (-1, -1)
        img = 0
        ix = iy = 0
        if o['image']:
            rd = room_data[o['room']]
            x0, y0, ch = rd['images'][o['image']]
            ww, hh, data = WD.frame_bytes(ch)
            E_label = f'img_{oname}'
            obj_images[oname] = (E_label, ww, hh, len(gfx))
            gfx += data
            obj_datas.append(data)
            img = f'{E_label}-base'
            ix, iy = x0, y0
        actor = G.act(o['actor']) + 1 if o['actor'] else 0
        icon = f'icon_{o["icon"]}-base' if o['icon'] else 0
        E(f'        dc.w    {box[0]},{box[1]},{box[2]},{box[3]},{wx},{wy}')
        E(f'        dc.b    {o["face"] if o["walk"] else 4},{o["verb"]}')
        E(f'        dc.w    {G.room_no(o["room"]) if o["room"] else 0}')
        E(f'        dc.l    name_{i}-base')
        E(f'        dc.l    {"hand_" + str(i) + "-base" if o["handlers"] else 0}')
        E(f'        dc.l    {img}')
        E(f'        dc.w    {ix},{iy}')
        E(f'        dc.l    {icon}')
        E(f'        dc.w    {o["state"]},{actor}')
    for oname, (lab, ww, hh, off) in obj_images.items():
        E(lab)
        E(f'        dc.w    {ww},{hh},0,0')
        E(f'        dc.l    {off}')
    for i, oname in enumerate(G.obj_order):
        if oname is None:
            continue
        o = G.objects[oname]
        E(f'name_{i}')
        E(WD.asm_text(o['label']))
        E('        even')
        if o['handlers']:
            E(f'hand_{i}')
            for verb, other, scr in o['handlers']:
                ov = 0 if other is None else (0xffff if other == '*' else G.obj(other))
                E(f'        dc.b    {verb},0')
                E(f'        dc.w    {ov}')
                E(f'        dc.l    {scr.name}-base')
            E('        dc.b    $ff,0')
            E('        dc.w    0')
            E('        dc.l    0')
    # icons (4 planes, 32 x 24)
    used_icons = {G.objects[o]['icon'] for o in G.obj_order[1:] if G.objects[o]['icon']}
    for name, fn in icons.ICONS.items():
        if name not in used_icons:
            continue
        E(f'icon_{name}')
        A.extend(WD.asm_bytes(WD.icon_bytes(fn())))
    E('objinit')
    st = [0] * 256
    for i, oname in enumerate(G.obj_order):
        if oname:
            o = G.objects[oname]
            st[i] = o['state'] if o['room'] else 0
    A.extend(WD.asm_bytes(bytes(st)))

    # ---- actors at the start
    E('actor_init')
    start_room = game.START_ACTORS
    assert len(game.ACTORS) <= 16, f'{len(game.ACTORS)} actors: the engine has 16 (MAXACT)'
    for i in range(16):
        if i < len(game.ACTORS):
            nm, cost, col, _ = game.ACTORS[i]
            r, x, y, d = start_room.get(nm, (None, 0, 0, 2))
            E(f'        dc.w    {G.room_no(r)},{x},{y},{d}')
            E(f'        dc.l    {"cost_" + cost + "-base" if cost else 0}')
            E(f'        dc.w    {col},0')
        else:
            E('        dcb.b   16,0')

    # ---- scripts
    for s in G.scripts:
        s.asm(A)
    E('start')
    E('        dc.w    13')
    E('        dc.l    start-base+6')  # (never used: start_script points at 'start' below)
    # the real start script is the one named 'start' (see game.py): point at it
    A[-3] = 'start_unused'
    E('defscripts')
    for verb in ['walk', 'give', 'pickup', 'use', 'open', 'look', 'push', 'close', 'talk', 'pull']:
        E(f'        dc.l    def_{verb}-base')

    # ---- strings (and speech)
    sounds_list = []
    for nm in game.SOUNDS:
        sounds_list.append(('fx', nm))
    speech_ids = {}
    for i, (t, v) in enumerate(zip(G.strings.texts, G.strings.speech)):
        if v:
            speech_ids[i] = len(sounds_list) + 1
            sounds_list.append(('speech', i))
    E('strings')
    for i, t in enumerate(G.strings.texts):
        E(f'        dc.l    str_{i}-base')
        E(f'        dc.w    {speech_ids.get(i, 0)},0')
    for i, t in enumerate(G.strings.texts):
        E(f'str_{i}')
        E(WD.asm_text(t))
    E('        even')
    E('sounds')
    sound_data = []
    for k, (kind, what) in enumerate(sounds_list):
        if kind == 'fx':
            b = orig_sfx(what)
            n, per = struct.unpack('>HH', b[:4])
            data = b[4:]
        else:
            who = G.strings.speech[what]
            voice, speed = game.VOICES[who]
            b = speech_clip(G.strings.texts[what], voice, speed)
            n, per = struct.unpack('>HH', b[:4])
            data = b[4:]
        if kind == 'speech':
            E(f'        dc.l    ${0x80000000 + add_blob(data, "spk"):08x}')
            data = None
        else:
            E(f'        dc.l    snd_{k}-base')
        E(f'        dc.w    {n},{per}')
        sound_data.append(data)
    for k, data in enumerate(sound_data):
        if data is None:
            continue
        E(f'snd_{k}')
        A.extend(WD.asm_bytes(data))
        E('        even')
    open(os.path.join(OUT, PREFIX + '.STR'), 'wb').write(stream)
    open(os.path.join(OUT, 'stream.i'), 'w').write(
        f'STR_ROOM_MAX = {(smax["room"] + 7) & ~3}\nSTR_SPK_MAX = {(smax["spk"] + 7) & ~3}\n')
    print(f'stream file {len(stream)} bytes (largest room {smax["room"]}, speech {smax["spk"]})')

    # ---- music: instruments (chip) and songs
    print('with object pictures', len(gfx))
    frame_max = max(frame_max_c, max((len(d) for d in obj_datas), default=0))
    ins_start = len(gfx)
    E('instruments')
    for name, fn in music.INSTRUMENTS:
        s, ls, ll, _ = fn()
        if len(s) % 2:
            s = np.concatenate([s, np.zeros(1, np.int8)])
        off = len(gfx)
        gfx += s.astype(np.int8).tobytes()
        E(f'        dc.l    {off}')
        E(f'        dc.w    {len(s) // 2},{ls // 2},{max(1, ll // 2)},{music.DECAY[name] * 16}')
    ins_size = len(gfx) - ins_start
    songs = music.songs()
    E('songs')
    for nm in game.SONGS:
        E(f'        dc.l    song_{nm}-base')
    for nm in game.SONGS:
        trs = songs[nm]
        E(f'song_{nm}')
        E(f'        dc.w    {len(trs)}')
        for j in range(len(trs)):
            E(f'        dc.l    song_{nm}_{j}-base')
        for j, tr in enumerate(trs):
            E(f'song_{nm}_{j}')
            flat = []
            for n, i, f, v in tr:
                flat += [n, i, f, v]
            flat.append(255)
            A.extend(WD.asm_bytes(bytes(flat)))
            E('        even')

    # ---- font, verbs, palettes
    E('font')
    for w, rows in WD.font_glyphs(FONT):
        E(f'        dc.b    {w},' + ','.join(str(r) for r in rows))
    E('        even')
    E('verbs')
    for i in range(10):
        E(f'        dc.l    verb_{i}-base')
    for i, v in enumerate(WD.VERBS):
        E(f'verb_{i}')
        E(WD.asm_text(v))
    E('        even')
    # ---- the story between the chapters
    import story
    E('storymap')
    for k, nm in enumerate(story.FLAGS):
        E(f'        dc.w    0,{k},{G.flag(nm)}')
    for k, nm in enumerate(story.ITEMS):
        if nm in G.objects and G.objects[nm]['room'] is None:
            E(f'        dc.w    1,{k},{G.obj(nm)}')
    E('        dc.w    -1')
    E('storydef')
    bits = bytearray(32)
    dflags, ditems = getattr(game, 'STORY_DEFAULT', ((), ()))
    for nm in dflags:
        k = story.FLAGS.index(nm)
        bits[k >> 3] |= 1 << (k & 7)
    for nm in ditems:
        k = story.ITEMS.index(nm)
        bits[16 + (k >> 3)] |= 1 << (k & 7)
    A.extend(WD.asm_bytes(bytes(bits)))
    E('        even')
    E('panelpal')
    E('        dc.w    ' + ','.join(f'${word12(rgb_of(c)):03x}' for c in icons.PANEL))
    E('fixedpal')
    E('        dc.w    ' + ','.join(f'${word12(c):03x}' for c in fixed))

    # the start: 'start' must be the script called start
    text = '\n'.join(A) + '\n'
    text = text.replace('\nstart_unused\n        dc.w    13\n        dc.l    start-base+6\n', '\n')
    open(os.path.join(OUT, 'dat.s'), 'w').write(text)
    open(os.path.join(OUT, PREFIX + '.GFX'), 'wb').write(bytes(gfx))
    r = subprocess.run([VASM, '-quiet', '-Fbin', '-o', os.path.join(OUT, PREFIX + '.DAT'), os.path.join(OUT, 'dat.s')],
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit('dat.s failed')
    sz = os.path.getsize(os.path.join(OUT, PREFIX + '.DAT'))
    print(f'WOS2.DAT {sz} bytes, WOS2.GFX {len(gfx)} bytes, {len(G.strings.texts)} texts, '
          f'{len(speech_ids)} spoken, {len(G.scripts)} scripts')
    write_dev_i(G, game)
    g_raw, g_packed = crunch(os.path.join(OUT, PREFIX + '.GFX'))
    g_alloc = crunch.alloc
    d_raw, d_packed = crunch(os.path.join(OUT, PREFIX + '.DAT'))
    print(f'crunched: GFX {g_raw} -> {g_packed}, DAT {d_raw} -> {d_packed} '
          f'({100 - 100 * (g_packed + d_packed) // (g_raw + d_raw)}% less to load)')
    total = g_packed + d_packed
    bar = build_loading()
    build_title()
    write_names()
    open(os.path.join(OUT, 'game.i'), 'w').write(
        f'SND_PICKUP = {game.SOUNDS.index("pickup") + 1}\n'
        f'LOAD_TOTAL = {total}\nGFX_ALLOC = {g_alloc}\n'
        f'INS_START = {ins_start}\nINS_SIZE = {ins_size}\nFRAME_MAX = {frame_max}\n'
        f'FC_SIZE = {max(40 * 1024, (frame_max + 16 * 1024 + 3) & ~3)}\n'
        f'BAR_ROW = {bar[0]}\nBAR_LINES = {bar[1]}\nBAR_COL = {bar[2]}\nBAR_BYTES = {bar[3]}\n'
        f'HAM_PAL = {HAM_PAL}\nHAM_COP = {HAM_COP}\n')
    return room_data


def write_names():
    """the file names of this chapter (names.i, files.i, nofile.i in the program)"""
    open(os.path.join(OUT, 'names.i'), 'w').write(f'vbl_name dc.b   "{PREFIX}",0\n')
    open(os.path.join(OUT, 'files.i'), 'w').write(
        f'n_dat   dc.b    "PROGDIR:{PREFIX}.DAT",0\n'
        f'n_gfx   dc.b    "PROGDIR:{PREFIX}.GFX",0\n'
        f'n_str   dc.b    "PROGDIR:{PREFIX}.STR",0\n'
        f'n_ttl   dc.b    "PROGDIR:{PREFIX}.TTL",0\n'
        f'n_intro dc.b    "PROGDIR:SSIntro",0\n'
        f'n_save  dc.b    "PROGDIR:{PREFIX}.SAV"\n')
    prev_vol = volume_name(max(1, CH - 1))
    vol = volume_name(CH, DEMO)
    old_prev = prev_vol.replace(VERSIONS[max(1, CH - 1)], 'V1.0')   # (a V1.0 / V1.1 disk before this one)
    st = f'WOSR.ST{CH}'
    open(os.path.join(OUT, 'story.i'), 'w').write(
        f'n_story_in   dc.b "PROGDIR:{st}",0\n'
        # the last chapter's disk: by its name, its old name, or any disk in a drive
        f'n_story_prev dc.b "{prev_vol}:{st}",0,"{old_prev}:{st}",0\n'
        f'             dc.b "DF0:{st}",0,"DF1:{st}",0,"DF2:{st}",0,"DF3:{st}",0,0\n'
        f'n_story_out  dc.b "PROGDIR:WOSR.ST{CH + 1}",0\n'
        f'n_vol_self   dc.b "{vol}:",0\n        even\n')
    open(os.path.join(OUT, 'nofile.i'), 'w').write(
        f'm_nofile dc.b   10,"World of Stronkie remake: {PREFIX}.DAT, .GFX or .STR is missing",10\n')


def write_dev_i(G, game):
    """dev mode: the rooms to jump to and the items to get (dev.i, in the program)"""
    spots = game.DEV_SPOTS
    items = game.DEV_ITEMS
    L = [f'DEV_ROOMS = {len(spots)}', 'dev_rooms']
    for r, n, x, y in spots:
        L.append(f'        dc.w    {G.room_no(r)},{x},{y}')
    L.append('dev_items')
    L.append('        dc.w    ' + ','.join(str(G.obj(o)) for o in items) + ',0')
    L.append('dev_texts')
    L.append('        dc.l    ' + ','.join(f'dvt{i}' for i in range(len(spots) + 2)) + ',0,0,0,0,0')
    for i, (r, n, x, y) in enumerate(spots):
        L.append(f'dvt{i}   dc.b    "{n}",0')
    L.append(f'dvt{len(spots)}   dc.b    "All items",0')
    L.append(f'dvt{len(spots) + 1}   dc.b    "Back",0')
    L.append('        even')
    open(os.path.join(OUT, 'dev.i'), 'w').write('\n'.join(L) + '\n')


TITLE_NAMES = {1: 'The Prologue', 2: 'Into Space', 3: 'Asteroid 42', 4: 'Landfall', 5: 'The Crystal Mountains',
               6: 'The Star Heart', 7: "Vex's Flagship"}


def cached_art(key, fn):
    """a painting (float 256 x 320 x 3) from the cache, or painted now"""
    p = os.path.join(CACHE, f'art_{key}_v1.npy')
    if os.path.exists(p):
        return np.load(p)
    a = fn()
    os.makedirs(CACHE, exist_ok=True)
    np.save(p, a)
    return a


def build_loading():
    """the loading screen: HAM6 (4096 colours), packed planes, 16 base colours, the full bar"""
    import loading
    import keyart
    import ham
    loading_pic = keyart.cached('loading', keyart.loading_art)
    a, full, exact, keep = loading.make_ham(CH, loading_pic)
    ca, pal = ham.encode(a / 255.0, keep=keep, exact=exact)
    cf, pal_f = ham.encode(full / 255.0, keep=keep, exact=exact)
    # the full bar: the same base colours (only the exact panel rows are used from it)
    cf = ca.copy()
    lut = {tuple(c): i for i, c in enumerate(pal)}
    x0, y0, x1, y1 = loading.HAM_BAR
    for y in range(y0 + 2, y1 - 2):
        for x in range(320):
            c = tuple(int(round(v / 17)) for v in full[y, x])
            cf[y, x] = lut[c]
    Image.fromarray((ham.decode(ca, pal) * 255).astype(np.uint8)).resize((640, 512), Image.NEAREST).save(
        os.path.join(OUT, 'loading.png'))
    Image.fromarray((ham.decode(cf, pal) * 255).astype(np.uint8)).resize((640, 512), Image.NEAREST).save(
        os.path.join(OUT, 'loading_full.png'))
    planes = WD.picture_bytes(ca.astype(np.int16), planes=6)
    open(os.path.join(OUT, 'loadpic.zx'), 'wb').write(zx_cached(planes))
    open(os.path.join(OUT, 'loadpal.bin'), 'wb').write(b''.join(struct.pack('>H', word12(c / 15)) for c in pal))
    r0, r1 = y0 + 2, y1 - 2
    strip = WD.picture_bytes(cf[r0:r1].astype(np.int16), planes=6)
    open(os.path.join(OUT, 'barstrip.bin'), 'wb').write(strip)
    c0, c1 = (x0 + 2) // 8, (x1 - 2) // 8 + 1
    return r0, r1 - r0, c0, c1 - c0


HAM_PAL = 6 * 40 * 256
HAM_COP = HAM_PAL + 32


def build_title():
    """the painted title screen (HAM6) in PREFIX.TTL: the planes, 16 colours, room for its copper list"""
    import keyart
    import ham
    pic = keyart.cached('title', keyart.title_art)
    a = (np.clip(pic, 0, 1) * 255).astype(np.uint8).copy()
    keyart.title_text(a, TITLE_NAMES[CH], CH, DEMO)
    ex = np.zeros(256, bool)
    ex[208:] = True
    ch, pal = ham.encode(a / 255.0, keep=[(255, 216, 112), (224, 236, 255), (20, 8, 40), (150, 140, 200)], exact=ex)
    Image.fromarray((ham.decode(ch, pal) * 255).astype(np.uint8)).resize((640, 512), Image.NEAREST).save(
        os.path.join(OUT, 'title_ham.png'))
    raw = WD.picture_bytes(ch.astype(np.int16), planes=6) + b''.join(struct.pack('>H', word12(c / 15)) for c in pal)
    raw += bytes(256)                               # the copper list goes here
    assert len(raw) == HAM_COP + 256
    p = os.path.join(OUT, PREFIX + '.TTL')
    open(p, 'wb').write(raw)
    crunch(p)
    return pic


def crunch(path):
    """pack a file for the loader: 'WZX1', unpacked size, memory size, the packed stream.
    The loader reads the stream into the end of the memory and unpacks it to the start;
    the memory size leaves enough room that the unpacker never overtakes what it reads."""
    raw = open(path, 'rb').read()
    packed = zx_cached(raw)
    tr = []
    assert zxpack.unpack(packed, tr) == raw
    worst = max(w - r for w, r in tr) if tr else 0
    base = max(len(raw) - len(packed), worst)
    base = (base + 16 + 3) & ~3                       # a little spare, long-aligned
    alloc = (base + len(packed) + 2 + 3) & ~3    # (+2: the read starts at an even address)
    open(path, 'wb').write(b'WZX1' + struct.pack('>LL', len(raw), alloc) + packed)
    crunch.alloc = alloc
    return len(raw), len(packed) + 12


def zx_cached(data):
    key = hashlib.sha1(data).hexdigest()
    p = os.path.join(CACHE, key + '.zx')
    if os.path.exists(p):
        return open(p, 'rb').read()
    packed = zxpack.pack(data)
    assert zxpack.unpack(packed) == data
    open(p, 'wb').write(packed)
    return packed


# ================================================================ the program
def build_engine():
    exe = os.path.join(OUT, PREFIX)
    for args, o in ((['-nosym'], exe), ([], exe + '.sym')):
        r = subprocess.run([VASM, '-quiet', '-Fhunkexe', '-kick1hunks', '-m68000', *args, '-I', OUT, '-I', HERE, '-o', o,
                            os.path.join(HERE, 'wos2.s')], capture_output=True, text=True)
        if r.returncode:
            print(r.stdout, r.stderr)
            raise SystemExit('wos2.s failed')
    print(f'{PREFIX} {os.path.getsize(exe)} bytes')


# ================================================================ previews (rooms with walk masks and hotspots)
def previews(room_data):
    import game
    G = game.G
    for rname, rd in room_data.items():
        im = preview_img(rd['chunky'], rd['pal32']).convert('RGB')
        a = np.asarray(im).copy()
        cells = rd.get('cells')
        if cells is not None:
            for y in range(42):
                for x in range(80):
                    if cells[y, x]:
                        a[y * 4 + 2, x * 4 + 2] = (0, 255, 0)
        im = Image.fromarray(a)
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        for o in G.rooms[rname]['objects']:
            ob = G.objects[o]
            if ob['box']:
                d.rectangle(ob['box'], outline=(255, 255, 0))
            if ob['walk']:
                x, y = ob['walk']
                d.ellipse([x - 2, y - 2, x + 2, y + 2], outline=(255, 0, 0))
        im.resize((640, 336), Image.NEAREST).save(os.path.join(OUT, f'preview_{rname}.png'))


# ================================================================ the disk
def build_adf():
    """the disk: OFS, bootable on Kickstart 1.3 - 3.1 (the toolkit's adf.py)"""
    sys.path.insert(0, os.path.join(TOOLKIT, 'tools'))
    import adf as ADF
    import shutil
    disk = os.path.join(OUT, f'{DISK_NAME}{"_Demo" if DEMO else ""}_{VERSION}.adf')
    src = os.path.join(OUT, 'disk')
    shutil.rmtree(src, ignore_errors=True)
    os.makedirs(os.path.join(src, 's'))
    open(os.path.join(src, 's', 'startup-sequence'), 'w').write(f'{PREFIX}\n')
    open(os.path.join(OUT, f'{PREFIX}.info'), 'wb').write(tool_icon())
    for f in (PREFIX, PREFIX + '.DAT', PREFIX + '.GFX', PREFIX + '.STR', PREFIX + '.TTL', PREFIX + '.info'):
        shutil.copy(os.path.join(OUT, f), os.path.join(src, f))
    shutil.copy(INTRO, os.path.join(src, 'SSIntro'))          # the boot intro: the game runs it first
    if os.environ.get('WOS2_TESTSTORY'):          # a test disk: with the story of the last chapter on it
        disk = disk.replace('.adf', '_TEST.adf')
        subprocess.run([sys.executable, os.path.join(HERE, 'tools', 'storyfile.py'), os.path.join(src, f'WOSR.ST{CH}'),
                        os.environ['WOS2_TESTSTORY']], check=True)
    ADF.build(disk, volume_name(CH, DEMO), src, os.path.join(TOOLKIT, 'tools', 'bootblock.bin'))
    used = sum(os.path.getsize(os.path.join(src, f)) for f in os.listdir(src) if os.path.isfile(os.path.join(src, f)))
    print(os.path.basename(disk), f'{used} bytes of files')
    return disk


def build_whdload():
    """the WHDLoad version: a drawer with the slave (Kickstart 3.1 emulation),
    its icon, a ReadMe and the game in data/"""
    import zipfile
    wd = os.path.join(HERE, 'whdload')
    open(os.path.join(OUT, 'version.i'), 'w').write(f'\t\tdc.b\t"Version {VERSION}",10\n')
    title = 'World of Stronkie remake' + (' (Demo)' if DEMO else '' if CH == 1 else f' - Chapter {CH}')
    open(os.path.join(OUT, 'whdname.i'), 'w').write(f'slv_name\tdc.b\t"{title}",0\n')
    open(os.path.join(OUT, 'whdprog.i'), 'w').write(f'_program\tdc.b\t"{PREFIX}",0\n')
    slave = os.path.join(OUT, PREFIX + '.slave')
    r = subprocess.run([VASM, '-quiet', '-Fhunkexe', '-nosym', '-I', WHD_INC, '-I', OUT, '-I', wd, '-o', slave,
                        os.path.join(wd, 'slave.s')], capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr)
        raise SystemExit('slave.s failed')
    z = os.path.join(OUT, f'{DISK_NAME}{"_Demo" if DEMO else ""}_{VERSION}_WHDLoad.zip')
    dr = 'WorldOfStronkieRemake' + ('Demo' if DEMO else '')  # every chapter goes into the same drawer (the story file is shared)
    readme = open(os.path.join(wd, 'ReadMe.txt')).read().replace('WOS2', PREFIX).replace('WORLD OF STRONKIE REMAKE - WHDLoad', 'WORLD OF STRONKIE REMAKE' + (
            '' if CH == 1 else f' - CHAPTER {CH}') + (' (DEMO)' if DEMO else '') + ' - WHDLoad')
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(slave, f'{dr}/{PREFIX}.slave')
        f.writestr(f'{dr}/{PREFIX}.info', tool_icon(project=('WHDLoad', [f'SLAVE={PREFIX}.slave', 'PRELOAD'])))
        f.writestr(f'{dr}/ReadMe', readme)
        for n in (PREFIX, PREFIX + '.DAT', PREFIX + '.GFX', PREFIX + '.STR', PREFIX + '.TTL'):
            f.write(os.path.join(OUT, n), f'{dr}/data/{n}')
        f.write(INTRO, f'{dr}/data/SSIntro')
    print(os.path.basename(z), os.path.getsize(z))
    return z


def tool_icon(project=None):
    """a classic tool icon: a heart with two moons (project: (default tool, tooltypes))"""
    art = []
    for y in range(22):
        row = ''
        for x in range(36):
            dx, dy = (x - 18) / 13.0, (y - 12) / 10.0
            heart = ((dx * dx + dy * dy - 0.5) ** 3 - dx * dx * (-dy) ** 3) < 0
            moon = (x - 30) ** 2 + (y - 3) ** 2 < 8 or (x - 6) ** 2 + (y - 4) ** 2 < 5
            row += '3' if heart else ('1' if moon else '0')
        art.append(row)
    h, w = len(art), len(art[0])
    wpr = (w + 15) // 16
    planes = []
    for p in range(2):
        data = b''
        for r in art:
            bits = ''.join('1' if (int(c) >> p) & 1 else '0' for c in r).ljust(wpr * 16, '0')
            data += int(bits, 2).to_bytes(wpr * 2, 'big')
        planes.append(data)
    gadget = struct.pack('>LhhhhHHHLLLlLHL', 0, 0, 0, w, h + 1, 0x0004, 0x0003, 0x0001, 1, 0, 0, 0, 0, 0, 0)
    out = struct.pack('>HH', 0xE310, 1) + gadget + struct.pack('>BB', 4 if project else 3, 0)
    out += struct.pack('>LLllLLl', 1 if project else 0, 1 if project else 0, -0x80000000, -0x80000000, 0, 0,
                       16384)
    out += struct.pack('>hhhhhLBBL', 0, 0, w, h, 2, 1, 3, 0, 0) + b''.join(planes)
    if project:
        tool, types = project
        s = tool.encode() + b'\0'
        out += struct.pack('>L', len(s)) + s
        out += struct.pack('>L', (len(types) + 1) * 4)
        for t in types:
            s = t.encode() + b'\0'
            out += struct.pack('>L', len(s)) + s
    return out


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'data', 'preview'):
        rd = build_data()
        if what == 'preview' or what == 'all':
            previews(rd)
    if what in ('all', 'engine'):
        build_engine()
    if what in ('all', 'adf'):
        build_adf()
    if what in ('all', 'whdload'):
        build_whdload()
