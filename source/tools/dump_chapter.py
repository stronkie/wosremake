#!/usr/bin/env python3
"""Dumps one chapter as JSON for the map and the walkthrough:
rooms (name, art, description), the exits between rooms, and the walkthrough
(chapters/chN_walk.py) as readable lines, room by room.

    WOS2_CHAPTER=3 python3 tools/dump_chapter.py > ch3.json"""
import json
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim                                            # noqa: E402
from wosdata import OP                                # noqa: E402

G = sim.G
game = sim.game
ROOMS = [r for r in G.room_order if r not in ('title', 'cards')]


def script_rooms(scr):
    out = []
    for it in scr.items:
        if it[0] == 'op' and it[1] == 'ROOM':
            out.append(it[2][0])
    return out


edges = set()
for name in G.obj_order[1:]:
    o = G.objects[name]
    if not o['room'] or o['room'] not in ROOMS:
        continue
    for verb, other, scr in o['handlers']:
        for rn in script_rooms(scr):
            to = G.room_order[rn - 1] if rn else None
            if to in ROOMS and to != o['room']:
                edges.add((o['room'], to, o['label']))

desc = {}
for r in ROOMS:
    e = G.rooms[r]['enter']
    if e:
        for it in e.items:
            if it[0] == 'op' and it[1] == 'SAY':
                t = G.strings.texts[it[2][1]]
                if t.startswith('You are') or t.startswith('You stand') or t.startswith('You hide') or 'A secret' in t:
                    desc[r] = t
                    break


def lab(o):
    return G.objects[o]['label'] if o in G.objects else o


def the(o):
    s = lab(o)
    return s if s[:1].isupper() else 'the ' + s


def go(o):
    s = lab(o)
    if s.startswith('back to') or s.startswith('way back to'):
        return 'Go ' + s.replace('way back to', 'back to') + '.'
    if s.split()[0] in ('way', 'path', 'ladder', 'passage', 'steps', 'stairs', 'hatch', 'lift', 'archway', 'rock'):
        return f'Take the {s}.'
    return f'Go to {the(o)}.'


ns = {}
exec(open(os.path.join(sim.HERE, 'chapters', f'ch{game.CH}_walk.py')).read(), ns)
S = sim.Sim()
S.story = ns.get('STORY')
S.run(G.scripts[[x.name for x in G.scripts].index('start')])
walk = []
for st in ns['WALK']:
    c = st[0]
    room = S.room
    if c == 'expect':
        continue
    if c == 'walk':
        line = go(st[1])
    elif c == 'talk':
        line = f'Talk to {the(st[1])}' + (': say ' + ', then '.join(f'"{x}"' for x in st[2]) if st[2] else '') + '.'
    elif c in ('use', 'give') and len(st) == 3:
        line = f'{"Use" if c == "use" else "Give"} {the(st[1])} {"with" if c == "use" else "to"} {the(st[2])}.'
    else:
        v = {'pickup': 'Pick up', 'look': 'Look at', 'open': 'Open', 'push': 'Push', 'pull': 'Pull', 'use': 'Use',
             'close': 'Close'}[c]
        line = f'{v} {the(st[1])}.'
    f0 = set(S.flags)
    i0 = list(S.inv)
    S.step(st)
    got = [lab(x) for x in S.inv if x not in i0]
    frag = [k for k, v in G.flags.items() if v in S.flags and v not in f0 and re.fullmatch(r'frag\d+', k)]
    if frag:
        line += f' (star fragment {frag[0][4:]}!)'
    elif got:
        line += f' You get: {", ".join(got)}.'
    line = line.replace('.".', '."').replace('!".', '!"').replace('?".', '?"')
    walk.append((G.rooms[room]['name'] if room else '', line))
json.dump({'ch': game.CH, 'rooms': [(r, G.rooms[r]['art'], desc.get(r, '')) for r in ROOMS],
           'edges': sorted(edges), 'walk': walk}, sys.stdout, indent=0)
