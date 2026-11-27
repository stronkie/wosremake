#!/usr/bin/env python3
"""Plays a chapter's scripts in Python (no Amiga needed), to check that the
puzzles can be solved: flags, inventory, rooms, conversations.

    WOS2_CHAPTER=2 python3 tools/sim.py            (plays chapters/chN_walk.py)

A walk is a list of steps:
    ('walk', 'thing')                     click a thing (walk to it / the exit)
    ('look', 'thing') ('open', ...) ...   a verb on a thing (or an item)
    ('use', 'item', 'thing')              use / give with two things
    ('talk', 'person', ['choice', ...])   talk; the choices are picked in order,
                                          then always the last one (goodbye)
    ('expect', 'item' | 'flag:name' | 'room:name' | 'end')
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import game                                   # noqa: E402
from wosdata import V                         # noqa: E402

G = game.G


class Sim:
    def __init__(self, verbose=False):
        self.flags = set()
        self.inv = []
        self.state = {}
        for o in G.obj_order[1:]:
            self.state[o] = G.objects[o]['state'] if G.objects[o]['room'] else 0
        self.where = {a: (None, 0, 0) for a in G.actors}
        for a, (r, x, y, d) in game.START_ACTORS.items():
            self.where[a] = (r, x, y)
        self.room = None
        self.ended = False
        self.v = verbose
        self.said = []
        self.choices = []
        self.picked = []
        self.cards = 0
        self.events = []
        self.story = None
        self.saved = None
        self.labels = {}
        for s in G.scripts:
            for k, it in enumerate(s.items):
                if it[0] == 'label':
                    self.labels[it[1]] = (s, k)
            self.labels[s.name] = (s, 0)

    def log(self, *a):
        if self.v:
            print('   ', *a)

    def run(self, script, pos=0, depth=0):
        s, k = script, pos
        steps = 0
        while True:
            steps += 1
            assert steps < 5000, 'endless script ' + s.name
            if k >= len(s.items):
                return
            it = s.items[k]
            k += 1
            if it[0] == 'label':
                continue
            _, op, a = it
            if op == 'END':
                return
            if op in ('SAY', 'SAYNW'):
                t = G.strings.texts[a[1]]
                self.said.append(t)
                self.events.append(('say', t))
                self.log(f'{G.actors[a[0]]}: {t}')
            elif op == 'RANDSAY':
                self.said.append(G.strings.texts[a[2]])
                self.events.append(('say', ''))
            elif op in ('WALK', 'WALKNW'):
                if op == 'WALK':
                    self.events.append(('pause', 3))
                a_ = G.actors[a[0]]
                self.where[a_] = (self.where[a_][0], a[1], a[2])
            elif op == 'WAIT':
                self.events.append(('pause', max(1, round(a[0] / 25))))
            elif op in ('ANIM', 'FADE'):
                self.events.append(('pause', 2))
            elif op in ('FACE', 'SOUND', 'MUSIC', 'CUTON', 'CUTOFF', 'ANIM', 'ANIMNW',
                        'FADE', 'COSTUME', 'SPEECH', 'WAITKEY'):
                pass
            elif op in ('CARD', 'CARDNW'):
                self.log('CARD', G.strings.texts[a[0]])
                if op == 'CARD':
                    self.cards += 1
                    self.events.append(('card', 0))
                else:
                    self.events.append(('pause', 2))
            elif op == 'PUT':
                rn = G.room_order[a[1] - 1] if a[1] else None
                self.where[G.actors[a[0]]] = (rn, a[2], a[3])
            elif op == 'PICKUP':
                o = G.obj_order[a[0]]
                if o not in self.inv:
                    self.inv.append(o)
                self.log('+', o)
            elif op == 'DROP':
                o = G.obj_order[a[0]]
                if o in self.inv:
                    self.inv.remove(o)
                self.log('-', o)
            elif op == 'SETF':
                self.flags.add(a[0])
            elif op == 'CLRF':
                self.flags.discard(a[0])
            elif op in ('IFF', 'IFNF'):
                if (a[0] in self.flags) == (op == 'IFF'):
                    s, k = self.labels[a[1][1]]
            elif op == 'JMP':
                s, k = self.labels[a[0][1]]
            elif op in ('HAS', 'NOTHAS'):
                if (G.obj_order[a[0]] in self.inv) == (op == 'HAS'):
                    s, k = self.labels[a[1][1]]
            elif op == 'IFROOM':
                if self.room == G.room_order[a[0] - 1]:
                    s, k = self.labels[a[1][1]]
            elif op == 'HIDE':
                self.state[G.obj_order[a[0]]] = 0
            elif op == 'SHOW':
                self.state[G.obj_order[a[0]]] = max(1, self.state[G.obj_order[a[0]]])
            elif op in ('IMGON', 'IMGOFF'):
                pass
            elif op == 'SETSTATE':
                self.state[G.obj_order[a[0]]] = a[1]
            elif op == 'ROOM':
                self.events.append(('pause', 3))
                self.go(G.room_order[a[0] - 1] if a[0] else None, depth)
            elif op == 'ENDGAME':
                self.ended = True
                self.log('ENDGAME')
                return
            elif op == 'DIALOG':
                n = a[0]
                opts = []
                for j in range(n):
                    c, t, lab = a[1 + j * 3:4 + j * 3]
                    ok = True
                    if c:
                        f = c & 0xff
                        ok = (f in self.flags) if c & 0x100 else (f not in self.flags)
                    if ok:
                        opts.append((G.strings.texts[t], lab[1]))
                if self.choices:
                    want = self.choices.pop(0)
                    hit = [o for o in opts if o[0].startswith(want)]
                    assert hit, f'no choice "{want}" in {[o[0] for o in opts]}'
                    pick = hit[0]
                else:
                    pick = opts[-1]
                self.log('>', pick[0])
                self.picked.append(opts.index(pick))
                self.events.append(('pick', opts.index(pick)))
                s, k = self.labels[pick[1]]
            elif op == 'STORYLOAD':
                if a[0] == 0 and self.story is not None:
                    self.apply_story(self.story)
                    self.flags.add(a[1])
            elif op == 'STORYDEF':
                self.apply_story(getattr(game, 'STORY_DEFAULT', ((), ())))
            elif op == 'STORYSAVE':
                import story
                fl = [n for n in story.FLAGS if G.flags[n] in self.flags]
                if self.story:
                    fl += [n for n in self.story[0] if n not in fl and n in story.FLAGS]
                it = [n for n in story.ITEMS if n in self.inv]
                self.saved = (fl, it)
                self.flags.add(a[0])
            elif op == 'RANDJMP':
                import random as _r
                lab = _r.choice(a[1:])
                s, k = self.labels[lab[1]]
            elif op in ('IFHERE', 'IFNHERE'):
                here = self.where[G.actors[a[0]]][0] == self.room
                if here == (op == 'IFHERE'):
                    s, k = self.labels[a[1][1]]
            elif op == 'STORYVOL':
                self.flags.add(a[0])
            else:
                raise SystemExit('sim: unknown op ' + op)

    def apply_story(self, st):
        fl, it = st
        for n in fl:
            self.flags.add(G.flags[n])
        for n in it:
            if n in G.objects and n not in self.inv:
                self.inv.append(n)

    def go(self, room, depth=0):
        self.room = room
        self.where['pilot'] = (room, 0, 0)
        for a, w in list(self.where.items()):
            pass
        self.log('== room', room)
        R = G.rooms.get(room)
        if R and R['enter'] and depth < 5:
            self.run(R['enter'], 0, depth + 1)

    def here(self, o):
        ob = G.objects[o]
        if o in self.inv:
            return True
        if ob['actor']:
            return self.where[ob['actor']][0] == self.room and ob['room'] == self.room
        return ob['room'] == self.room and self.state[o] > 0

    def act(self, verb, o, other=None):
        assert self.here(o), f'{o} is not here (room {self.room})'
        if other:
            assert self.here(other), f'{other} is not here (room {self.room})'
        ob = G.objects[o]
        vn = V[verb]
        for hv, hother, scr in ob['handlers']:
            if hv == vn and hother == other:
                return self.run(scr)
        if other:
            for hv, hother, scr in ob['handlers']:
                if hv == vn and hother == '*':
                    return self.run(scr)
            for hv, hother, scr in G.objects[other]['handlers']:
                if hv == vn and hother in ('*', o):
                    return self.run(scr)
        raise AssertionError(f'nothing happens: {verb} {o} {other or ""}')

    def step(self, st):
        c = st[0]
        if c == 'expect':
            w = st[1]
            if w.startswith('flag:'):
                assert G.flags[w[5:]] in self.flags, 'flag not set: ' + w
            elif w.startswith('room:'):
                assert self.room == w[5:], f'in room {self.room}, not {w[5:]}'
            elif w == 'end':
                assert self.ended, 'the chapter did not end'
            else:
                assert w in self.inv, f'{w} is not in the inventory {self.inv}'
            return
        if c == 'talk':
            self.choices = list(st[2]) if len(st) > 2 else []
            self.act('talk', st[1])
            assert not self.choices, f'choices not used: {self.choices}'
            return
        if c == 'walk':
            return self.act('walk', st[1])
        if len(st) == 3:
            return self.act(c, st[1], st[2])
        return self.act(c, st[1])


def play(walk, verbose=False, story=None):
    sim = Sim(verbose)
    sim.story = story
    sim.run(G.scripts[[s.name for s in G.scripts].index('start')])
    for i, st in enumerate(walk):
        if verbose:
            print(i, st)
        try:
            sim.step(st)
        except AssertionError as e:
            raise SystemExit(f'step {i} {st}: {e}')
    return sim


if __name__ == '__main__':
    ch = game.CH
    ns = {}
    exec(open(os.path.join(HERE, 'chapters', f'ch{ch}_walk.py')).read(), ns)
    s = play(ns['WALK'], '-v' in sys.argv, ns.get('STORY'))
    print(f'chapter {ch}: {len(ns["WALK"])} steps OK, ended={s.ended}, {len(s.said)} lines said, story out: {s.saved}')
