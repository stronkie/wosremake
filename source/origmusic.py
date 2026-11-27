"""The music of the original World of Stronkie (Amiga V2.4), for the remake.

The original plays its tunes like a C64: three voices, each with a SID waveform
(triangle, saw, pulse, noise) and an ADSR envelope, and a list of (note, frames).
Here every (waveform, envelope) becomes a sampled instrument of the remake's
sequencer (sound.s), and the notes go over one to one: same notes, same frames,
same tempo. orig/songs.json holds the songs as they are in the original's
source (menu.s = the title tune, part01-03.s = the Prologue, part04.s = Chapter 1).

    events(name) -> [track, track, track], track = [(note, instrument, frames, volume)]
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SONGS = json.load(open(os.path.join(HERE, 'orig', 'songs.json')))
SR = 8287.0
C4 = 261.6256
DECAY_MS = [6, 24, 48, 72, 114, 168, 204, 240, 300, 750, 1500, 2400, 3000, 9000, 15000, 24000]
VOLUME = {0x10: 30, 0x20: 22, 0x40: 22, 0x80: 34}       # by waveform (softer: under the speech)


def _wave(kind, duty=0.5):
    n_cyc = 19
    L = int(round(SR / C4 * n_cyc))
    t = (np.arange(L) / L * n_cyc) % 1
    if kind == 0x10:
        x = 1 - 4 * np.abs(t - 0.5)
    elif kind == 0x20:
        x = t * 2 - 1
    else:
        x = np.where(t < duty, 1.0, -1.0)
        k = np.array([0.25, 0.5, 0.25])               # a little softer than a hard square
        x = np.convolve(np.concatenate([x[-1:], x, x[:1]]), k, 'valid')
    x = x / np.abs(x).max() * 0.95
    return np.round(x * 127).astype(np.int8), 0, L


def _noise(kind):
    rng = np.random.default_rng({'kick': 1, 'snare': 2, 'hat': 3}[kind])
    if kind == 'kick':
        n = int(SR * 0.16)
        t = np.arange(n) / SR
        f = 150 * np.exp(-t * 20) + 45
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 15) + rng.uniform(-1, 1, n) * 0.15 * np.exp(-t * 60)
    elif kind == 'snare':
        n = int(SR * 0.14)
        t = np.arange(n) / SR
        x = rng.uniform(-1, 1, n) * np.exp(-t * 24)
    else:
        n = int(SR * 0.05)
        t = np.arange(n) / SR
        x = rng.uniform(-1, 1, n)
        x = np.diff(np.concatenate([[0], x])) * np.exp(-t * 70)
    x = x / np.abs(x).max() * 0.95
    return np.round(x * 127).astype(np.int8), 0, 1


def _decay(ad, sr, vol):
    """SID envelope -> (volume, decay per frame of the remake's sequencer)"""
    sustain = sr >> 4
    if sustain:
        return max(8, vol * (8 + sustain) // 23), 0
    frames = max(1.0, DECAY_MS[ad & 15] / 20.0)
    return vol, int(min(40, max(1, round(vol / frames))))


def instruments():
    """[(name, fn, decay)] for every waveform + envelope the songs use, and the drums"""
    out, seen = [], set()
    for song in SONGS.values():
        for wf, ad, sr, pw in song['inst']:
            if wf == 0x80:
                continue
            vol, dec = _decay(ad, sr, VOLUME.get(wf, 36))
            duty = (pw / 16) if wf == 0x40 and pw else 0.5
            name = f'sid{wf:02x}_{dec}_{int(duty * 16)}'
            if name in seen:
                continue
            seen.add(name)
            out.append((name, (lambda wf=wf, duty=duty: (*_wave(wf, duty), 1)), dec))
    for k in ('kick', 'snare', 'hat'):
        out.append(('sid_' + k, (lambda k=k: (*_noise(k), 0)), 0))
    return out


def events(name, inum):
    """the song as three tracks of the remake's sequencer (inum: instrument name -> number)"""
    song = SONGS[name]
    voices = list(zip(song['inst'], song['voices']))
    if len(voices) > 3:                    # the title tune has 4 voices: channel 3 is for speech
        voices = voices[:3]
    tracks = []
    for (wf, ad, sr, pw), data in voices:
        if 255 in data:
            data = data[:data.index(255)]
        data = [b for b in data if b != 0xFE]
        ev = []
        if wf == 0x80:
            for i in range(0, len(data) - 1, 2):
                n, fr = data[i], data[i + 1]
                if n == 0:
                    ev.append((0, 0, fr, 0))
                    continue
                k = 'kick' if n <= 0x20 else 'snare' if n <= 0x40 else 'hat'
                ev.append((25, inum['sid_' + k], fr, {'kick': 60, 'snare': 44, 'hat': 26}[k]))
        else:
            vol, dec = _decay(ad, sr, VOLUME.get(wf, 36))
            duty = (pw / 16) if wf == 0x40 and pw else 0.5
            ins = inum[f'sid{wf:02x}_{dec}_{int(duty * 16)}']
            for i in range(0, len(data) - 1, 2):
                n, fr = data[i], data[i + 1]
                if n == 0:                     # a rest: the same instrument at volume 0 (silence)
                    ev.append((25, ins, fr, 0))
                    continue
                e = n - 24                     # original: MIDI - 11, remake: MIDI - 35 (C4 = 25)
                while e < 1:
                    e += 12
                while e > 46:                  # (period 127: Paula needs 124 or more)
                    e -= 12
                ev.append((e, ins, fr, vol))
        out = []
        for n, i, f, v in ev:
            while f > 250:
                out.append((n, i, 250, v))
                n, v = 0, 0
                f -= 250
            if f:
                out.append((n, i, f, v))
        tracks.append(out)
    return tracks
