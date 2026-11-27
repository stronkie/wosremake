"""Music and sound effects for World of Stronkie remake.

Instruments are synthesised samples (8 bit, 8287 Hz: they sound at their own pitch
at Paula period 428, middle C). Songs are three tracks of (note, instrument,
frames, volume) events for the small sequencer in sound.s."""
import numpy as np

SR = 8287.0                      # sample rate of an instrument at period 428
C4 = 261.6256
NOTE_BASE = 25                   # engine note number of C4 (period 428)
NAMES = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}


def to8(x):
    x = x / max(1e-9, np.abs(x).max()) * 0.95
    return np.round(x * 127).astype(np.int8)


def cycles_len(f0, n_cycles):
    return int(round(SR / f0 * n_cycles))


def lp(x, a):
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


# ---------------------------------------------------------------- instruments
def inst_harp():
    """plucked string (Karplus-Strong), the tail loops"""
    period = SR / C4
    n = int(SR * 0.5)
    rng = np.random.default_rng(3)
    p = int(round(period))
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        v = buf[i % p]
        out[i] = v
        buf[i % p] = 0.5 * (v + buf[(i + 1) % p]) * 0.998
    loop_len = p * 8
    return to8(out), n - loop_len, loop_len, 3


def inst_flute():
    L = cycles_len(C4, 19)
    t = np.arange(L) / L * 19 * 2 * np.pi
    x = np.sin(t) + 0.25 * np.sin(2 * t) + 0.08 * np.sin(3 * t)
    att = np.arange(int(SR * 0.04)) / (SR * 0.04)
    head = np.sin(np.arange(len(att)) / L * 19 * 2 * np.pi) * att
    s = np.concatenate([head, x])
    return to8(s), len(head), L, 1


def inst_pad():
    L = cycles_len(C4, 19)
    t = np.arange(L) / L * 19
    x = sum(((t * (1 + d)) % 1) * 2 - 1 for d in (0.0,)) * 0.6
    x = x + 0.4 * np.sin(2 * np.pi * t * 2)
    x = lp(np.tile(x, 3), 0.25)[L * 2:]
    return to8(x), 0, L, 1


def inst_bass():
    f0 = C4 / 2
    L = cycles_len(f0, 11)
    t = np.arange(L) / L * 11
    x = 1 - 4 * np.abs((t % 1) - 0.5)
    x = x + 0.3 * np.sin(2 * np.pi * t * 2)
    return to8(x), 0, L, 2


def inst_bell():
    n = int(SR * 0.7)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * C4 * 2 * t) + 0.5 * np.sin(2 * np.pi * C4 * 2 * 2.76 * t) * np.exp(-t * 6)
         + 0.25 * np.sin(2 * np.pi * C4 * 2 * 5.4 * t) * np.exp(-t * 10)) * np.exp(-t * 3)
    loop = cycles_len(C4 * 2, 8)
    return to8(x), n - loop, loop, 3


def inst_drum():
    """kick: a falling sine"""
    n = int(SR * 0.18)
    t = np.arange(n) / SR
    f = 160 * np.exp(-t * 18) + 45
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)
    return to8(x), 0, 1, 0


def inst_snare():
    n = int(SR * 0.16)
    t = np.arange(n) / SR
    rng = np.random.default_rng(4)
    x = (rng.uniform(-1, 1, n) * 0.8 + np.sin(2 * np.pi * 190 * t) * 0.4) * np.exp(-t * 22)
    return to8(x), 0, 1, 0


# The remake plays the original World of Stronkie tunes (origmusic.py): its
# instruments are the original's SID waveforms and envelopes, sampled.
import origmusic                                                  # noqa: E402
_SID = origmusic.instruments()
INSTRUMENTS = [(n, f) for n, f, _ in _SID]
INUM = {n: i for i, (n, _) in enumerate(INSTRUMENTS)}
DECAY = {n: d for n, _, d in _SID}


def note_no(name):
    """'c4', 'f#3', 'bb2' -> engine note number (C4 = 25)"""
    n = name.lower()
    semi = NAMES[n[0]]
    i = 1
    while i < len(n) and n[i] in '#b':
        semi += 1 if n[i] == '#' else -1
        i += 1
    octave = int(n[i:])
    return NOTE_BASE + (octave - 4) * 12 + semi


def track(spec, inst, unit, vol=48, gate=None):
    """spec: 'c4:2 e4:2 r:4 ...' (lengths in units of 'unit' frames) -> events"""
    ev = []
    for tok in spec.split():
        name, ln = tok.split(':') if ':' in tok else (tok, '1')
        frames = int(round(float(ln) * unit))
        if name == 'r':
            ev.append((0, 0, frames, 0))
            continue
        ins = inst
        v = vol
        if '@' in name:
            name, ins = name.split('@')
        if name in ('k', 's'):
            ins = 'kick' if name == 'k' else 'snare'
            ev.append((note_no('c4'), INUM[ins], frames, 60))
            continue
        ev.append((note_no(name), INUM[ins], frames, v))
    # split long events (frames are a byte)
    out = []
    for n, i, f, v in ev:
        while f > 250:
            out.append((n, i, 250, v))
            n, v = 0, 0
            f -= 250
        out.append((n, i, f, v))
    return out


def arp(chords, inst, unit, per=4, vol=34, pattern=(0, 1, 2, 1)):
    """broken chords: [('c3 e3 g3', bars)...] -> a track"""
    s = []
    for ch, bars in chords:
        notes = ch.split()
        for k in range(int(bars * 16 / per * per)):
            s.append(f'{notes[pattern[k % len(pattern)] % len(notes)]}:1')
    return track(' '.join(s), inst, unit, vol)


def bassline(chords, unit, vol=50, pattern=(4, 4, 4, 4)):
    s = []
    for ch, bars in chords:
        root = ch.split()[0]
        for _ in range(bars):
            for ln in pattern:
                s.append(f'{root}:{ln}')
    return track(' '.join(s), 'bass', unit, vol)


# ---------------------------------------------------------------- the songs
def songs():
    """the original tunes: the title, the three parts of the Prologue, and Chapter 1"""
    return {n: origmusic.events(n, INUM) for n in origmusic.SONGS}


# ---------------------------------------------------------------- sound effects (7 kHz, one shot)
FX_RATE = 7000


def sfx():
    rng = np.random.default_rng(5)
    R = FX_RATE

    def t_(sec):
        return np.arange(int(R * sec)) / R
    out = {}
    t = t_(0.25)
    out['pickup'] = to8(np.sin(2 * np.pi * np.cumsum(np.linspace(600, 1600, len(t))) / R) * np.exp(-t * 9))
    t = t_(0.5)
    out['hatch'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.5) * np.exp(-t * 4) * np.minimum(1, t * 30))
    t = t_(0.45)
    out['splash'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.35) * np.exp(-t * 7) * (1 + 0.5 * np.sin(2 * np.pi * 9 * t)))
    t = t_(0.9)
    f = np.linspace(300, 1400, len(t))
    out['zip'] = to8((np.sin(2 * np.pi * np.cumsum(f) / R) * 0.6 + lp(rng.uniform(-1, 1, len(t)), 0.6) * 0.5) * np.minimum(1, t * 8) * np.exp(-t * 1.5))
    t = t_(0.8)
    out['chime'] = to8(sum(np.sin(2 * np.pi * f0 * t) * np.exp(-t * k) for f0, k in ((1046, 4), (1318, 5), (1568, 6))))
    t = t_(1.2)
    sp = sum(np.sin(2 * np.pi * (800 + 300 * k) * t) * np.exp(-((t - k * 0.12) % 1.2) * 12) for k in range(6))
    out['bloom'] = to8(sp * np.minimum(1, t * 3))
    t = t_(0.35)
    f = 900 + 500 * np.sin(2 * np.pi * 7 * t)
    out['squeak'] = to8((np.sin(2 * np.pi * np.cumsum(f) / R) + 0.4 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / R))) * np.exp(-t * 4))
    t = t_(0.5)
    out['clang'] = to8(sum(np.sin(2 * np.pi * f0 * t) for f0 in (420, 1130, 1870)) * np.exp(-t * 8))
    t = t_(0.18)
    out['rabbit'] = to8(np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, len(t))) / R) * np.exp(-t * 14))
    t = t_(0.3)
    out['door'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.15) * np.exp(-t * 12) + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 15))
    t = t_(0.5)
    out['boing'] = to8(np.sin(2 * np.pi * np.cumsum(180 + 400 * np.abs(np.sin(2 * np.pi * 6 * t))) / R) * np.exp(-t * 4))
    t = t_(1.2)
    out['rumble'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.05) * np.minimum(1, t * 4) * np.exp(-t * 1.2))
    t = t_(1.0)
    out['snore'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.08) * (np.sin(np.pi * t) ** 2) * (1 + np.sin(2 * np.pi * 30 * t)))
    t = t_(0.3)
    out['beep'] = to8(np.sign(np.sin(2 * np.pi * 880 * t)) * 0.5 * (t < 0.12) + np.sign(np.sin(2 * np.pi * 1320 * t)) * 0.5 * (t > 0.16))
    t = t_(0.8)
    out['disk'] = to8(lp(rng.uniform(-1, 1, len(t)), 0.3) * (np.sin(2 * np.pi * 6 * t) > 0) * 0.8 + np.sign(np.sin(2 * np.pi * 60 * t)) * 0.2)
    # ---- sounds of the places (quiet: they play now and then in the background)

    def soft(x, a):
        return (to8(x).astype(np.float32) * a).astype(np.int8)
    t = t_(0.45)
    ch = (np.sin(2 * np.pi * np.cumsum(2200 + 900 * np.sin(2 * np.pi * 28 * t)) / R) *
          ((t % 0.2) < 0.07) * np.exp(-(t % 0.2) * 30))
    out['bird'] = soft(ch, 0.35)
    t = t_(0.4)
    out['cricket'] = soft(np.sin(2 * np.pi * 3100 * t) * (np.sin(2 * np.pi * 30 * t) > 0.3) * ((t % 0.2) < 0.12), 0.22)
    t = t_(0.3)
    d = np.sin(2 * np.pi * np.cumsum(np.linspace(900, 2200, len(t))) / R) * np.exp(-t * 28)
    d[int(R * 0.12):] += 0.4 * d[:len(d) - int(R * 0.12)]
    out['drip'] = soft(d, 0.4)
    t = t_(1.4)
    out['wind'] = soft(lp(rng.uniform(-1, 1, len(t)), 0.06) * np.sin(np.pi * t / 1.4) ** 2 *
                       (1 + 0.5 * np.sin(2 * np.pi * 1.7 * t)), 0.3)
    t = t_(0.7)
    cr = np.zeros(len(t))
    for k in rng.integers(0, len(t) - 40, 14):
        cr[k:k + 40] += rng.uniform(-1, 1, 40) * np.exp(-np.arange(40) / 6)
    out['crackle'] = soft(cr, 0.3)
    t = t_(1.0)
    out['hum'] = soft((np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 220 * t) + 0.2 * np.sin(2 * np.pi * 330 * t)) *
                      np.sin(np.pi * t) ** 2, 0.28)
    t = t_(0.45)
    tones = np.array([1200, 1800, 900, 1500, 2100, 1100])[(t * 13).astype(int) % 6]
    out['blip'] = soft(np.sign(np.sin(2 * np.pi * np.cumsum(tones) / R)) * ((t * 13) % 1 < 0.6), 0.18)
    t = t_(0.9)
    out['owl'] = soft(np.sin(2 * np.pi * 420 * t) * (((t > 0.05) & (t < 0.3)) | ((t > 0.45) & (t < 0.8))) *
                      (1 + 0.2 * np.sin(2 * np.pi * 6 * t)), 0.3)
    return out
