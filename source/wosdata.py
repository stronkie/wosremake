"""The data side of The World of Stronkie II: the script language, and writing
WOS2.DAT (an assembler file for vasm -Fbin) and WOS2.GFX (chip memory: the
people's frames, object pictures, the instruments).

Nothing in here knows the story: game.py describes the rooms, things, people
and scripts, build.py paints and puts everything together."""
import os
import re
import numpy as np

# ---------------------------------------------------------------- opcodes
OPS = ['END', 'SAY', 'SAYNW', 'WALK', 'WALKNW', 'FACE', 'PUT', 'PICKUP',
       'DROP', 'SETF', 'CLRF', 'IFF', 'IFNF', 'JMP', 'HIDE', 'SHOW',
       'IMGON', 'IMGOFF', 'ROOM', 'WAIT', 'SOUND', 'MUSIC', 'DIALOG', 'CUTON',
       'CUTOFF', 'RANDSAY', 'ANIM', 'ANIMNW', 'CARD', 'HAS', 'NOTHAS', 'ENDGAME',
       'FADE', 'COSTUME', 'IFROOM', 'SPEECH', 'CARDNW', 'SETSTATE', 'WAITKEY',
       'STORYLOAD', 'STORYDEF', 'STORYSAVE', 'STORYVOL', 'RANDJMP', 'IFHERE', 'IFNHERE', 'HAMPIC']
OP = {n: i for i, n in enumerate(OPS)}

VERBS = ['Walk to', 'Give', 'Pick up', 'Use', 'Open', 'Look at', 'Push', 'Close', 'Talk to', 'Pull']
V = {k: i for i, k in enumerate(['walk', 'give', 'pickup', 'use', 'open', 'look', 'push', 'close', 'talk', 'pull'])}
RIGHT, LEFT, FRONT, BACK = 0, 1, 2, 3


class Strings:
    """every text of the game once; some are spoken"""
    def __init__(self):
        self.texts = ['']
        self.speech = [None]
        self.index = {}

    def add(self, text, speech=None):
        key = (text, speech)
        if key not in self.index:
            self.index[key] = len(self.texts)
            self.texts.append(text)
            self.speech.append(speech)
        return self.index[key]


class Script:
    """a list of opcodes with labels. Arguments: numbers, ('L', label), ('S', text, voice)"""
    count = 0

    def __init__(self, game, name=None):
        Script.count += 1
        self.g = game
        self.name = name or f'scr{Script.count}'
        self.items = []
        self.nlab = 0

    def label(self):
        self.nlab += 1
        return f'{self.name}_L{self.nlab}'

    def here(self, lab):
        self.items.append(('label', lab))
        return self

    def op(self, name, *args):
        self.items.append(('op', name, args))
        return self

    def s(self, text, actor=None):
        """a string number; key lines (marked with a leading '*') are spoken"""
        voice = None
        if text.startswith('*'):
            text = text[1:]
            voice = self.g.voice_of(actor) if actor is not None else 'narrator'
        return self.g.strings.add(text, voice)

    # ---- the opcodes
    def say(self, a, text, wait=True):
        return self.op('SAY' if wait else 'SAYNW', self.g.act(a), self.s(text, a))

    def walk(self, a, x, y, wait=True):
        return self.op('WALK' if wait else 'WALKNW', self.g.act(a), x, y)

    def face(self, a, d):
        return self.op('FACE', self.g.act(a), d)

    def put(self, a, room, x, y, d=FRONT):
        return self.op('PUT', self.g.act(a), self.g.room_no(room), x, y, d)

    def pickup(self, o):
        return self.op('PICKUP', self.g.obj(o))

    def drop(self, o):
        return self.op('DROP', self.g.obj(o))

    def setf(self, f):
        return self.op('SETF', self.g.flag(f))

    def clrf(self, f):
        return self.op('CLRF', self.g.flag(f))

    def iff(self, f, lab):
        return self.op('IFF', self.g.flag(f), ('L', lab))

    def ifnf(self, f, lab):
        return self.op('IFNF', self.g.flag(f), ('L', lab))

    def jmp(self, lab):
        return self.op('JMP', ('L', lab))

    def hide(self, o):
        return self.op('HIDE', self.g.obj(o))

    def show(self, o):
        return self.op('SHOW', self.g.obj(o))

    def imgon(self, o):
        return self.op('IMGON', self.g.obj(o))

    def imgoff(self, o):
        return self.op('IMGOFF', self.g.obj(o))

    def room(self, r, x, y, d=FRONT):
        return self.op('ROOM', self.g.room_no(r), x, y, d)

    def wait(self, ticks):
        return self.op('WAIT', ticks)

    def sound(self, name):
        return self.op('SOUND', self.g.sound_no(name))

    def music(self, name):
        return self.op('MUSIC', self.g.song_no(name) if name else 0)

    def cuton(self):
        return self.op('CUTON')

    def cutoff(self):
        return self.op('CUTOFF')

    def randsay(self, a, texts):
        return self.op('RANDSAY', self.g.act(a), len(texts), *[self.s(t, a) for t in texts])

    def anim(self, a, spec, loops=1, wait=True):
        return self.op('ANIM' if wait else 'ANIMNW', self.g.act(a), self.g.special_no(a, spec), loops)

    def card(self, text, wait=True):
        return self.op('CARD' if wait else 'CARDNW', self.s(text))

    def has(self, o, lab):
        return self.op('HAS', self.g.obj(o), ('L', lab))

    def nothas(self, o, lab):
        return self.op('NOTHAS', self.g.obj(o), ('L', lab))

    def endgame(self):
        return self.op('ENDGAME')

    def fade(self, level):
        return self.op('FADE', level)

    def costume(self, a, cost):
        return self.op('COSTUME', self.g.act(a), ('C', cost))

    def ifroom(self, r, lab):
        return self.op('IFROOM', self.g.room_no(r), ('L', lab))

    def setstate(self, o, state):
        return self.op('SETSTATE', self.g.obj(o), state)

    def waitkey(self):
        return self.op('WAITKEY')

    def hampic(self, on):
        """1: the painted title (HAM6, PREFIX.TTL) over the screen, 0: back"""
        return self.op('HAMPIC', 1 if on else 0)

    def storyload(self, src, f):
        """src 0: this drawer, 1: the last chapter's disk; sets f if the story was read"""
        return self.op('STORYLOAD', src, self.g.flag(f))

    def storydef(self):
        return self.op('STORYDEF')

    def storysave(self, f):
        return self.op('STORYSAVE', self.g.flag(f))

    def storyvol(self, f):
        return self.op('STORYVOL', self.g.flag(f))

    def randjmp(self, labs):
        """jump to one of the labels, at random"""
        return self.op('RANDJMP', len(labs), *[('L', l) for l in labs])

    def ifhere(self, a, lab):
        """jump if the actor is in this room"""
        return self.op('IFHERE', self.g.act(a), ('L', lab))

    def ifnhere(self, a, lab):
        return self.op('IFNHERE', self.g.act(a), ('L', lab))

    def end(self):
        return self.op('END')

    def dialog(self, choices):
        """choices: [(text, label, cond)] cond: None, '!flag' (flag not set), 'flag' (set)"""
        args = [len(choices)]
        for text, lab, cond in choices:
            c = 0
            if cond:
                c = self.g.flag(cond[1:]) if cond.startswith('!') else 0x100 + self.g.flag(cond)
            args += [c, self.s(text), ('L', lab)]
        return self.op('DIALOG', *args)

    # ---- assembler output
    def asm(self, out):
        out.append(f'{self.name}')
        if not self.items or self.items[-1][0] != 'op' or self.items[-1][1] not in ('END', 'JMP', 'ENDGAME'):
            self.items.append(('op', 'END', ()))
        for it in self.items:
            if it[0] == 'label':
                out.append(f'{it[1]}')
                continue
            _, name, args = it
            parts = [f'        dc.w    {OP[name]}']
            for a in args:
                if isinstance(a, tuple) and a[0] == 'L':
                    parts.append(f'        dc.l    {a[1]}-base')
                elif isinstance(a, tuple) and a[0] == 'C':
                    parts.append(f'        dc.l    cost_{a[1]}-base')
                else:
                    parts.append(f'        dc.w    {int(a) & 0xffff}')
            out.extend(parts)


# ---------------------------------------------------------------- planar data
def frame_bytes(chunky, planes=5):
    """chunky (h x w, register numbers, -1 transparent) -> (ww, h, bytes): planes
    interleaved by line, then the mask (one line per row), one extra word for the shift"""
    h, w = chunky.shape
    ww = (w + 15) // 16 + 1
    full = np.full((h, ww * 16), -1, np.int16)
    full[:, :w] = chunky
    mask = full >= 0
    val = np.where(mask, full, 0)
    data = bytearray()
    for y in range(h):
        for p in range(planes):
            bits = ((val[y] >> p) & 1).astype(np.uint8)
            data += np.packbits(bits).tobytes()
    m = bytearray()
    for y in range(h):
        m += np.packbits(mask[y].astype(np.uint8)).tobytes()
    return ww, h, bytes(data + m)


def picture_bytes(chunky, planes=5):
    """a whole picture (320 wide), planes interleaved by line"""
    h, w = chunky.shape
    out = bytearray()
    for y in range(h):
        for p in range(planes):
            out += np.packbits(((chunky[y] >> p) & 1).astype(np.uint8)).tobytes()
    return bytes(out)


def icon_bytes(chunky):
    """32 x 24, 4 planes interleaved by line (4 bytes a plane line)"""
    out = bytearray()
    for y in range(24):
        for p in range(4):
            out += np.packbits(((chunky[y] >> p) & 1).astype(np.uint8)).tobytes()
    return bytes(out)


def font_glyphs(path):
    """font8x8_basic.h -> 96 glyphs of (width, 8 rows MSB = left), proportional"""
    src = open(path).read()
    rows = re.findall(r'\{\s*((?:0x[0-9A-Fa-f]{2},?\s*){8})\}', src)
    glyphs = []
    for i in range(32, 128):
        bytes8 = [int(v, 16) for v in re.findall(r'0x([0-9A-Fa-f]{2})', rows[i])]
        bits = [[(b >> x) & 1 for x in range(8)] for b in bytes8]    # bit 0 = left
        cols = [x for x in range(8) if any(r[x] for r in bits)]
        if not cols:
            glyphs.append((3, [0] * 8))
            continue
        x0, x1 = min(cols), max(cols)
        out = []
        for r in bits:
            v = 0
            for k, x in enumerate(range(x0, x1 + 1)):
                if r[x]:
                    v |= 0x80 >> k
            out.append(v)
        glyphs.append((x1 - x0 + 1, out))
    return glyphs


def asm_bytes(data, per=32):
    out = []
    for i in range(0, len(data), per):
        out.append('        dc.b    ' + ','.join(str(b) for b in data[i:i + per]))
    return out


def asm_text(t):
    t = t.replace('"', "'")
    return f'        dc.b    "{t}",0'
