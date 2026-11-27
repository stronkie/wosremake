#!/usr/bin/env python3
"""Turns a chapter's walk (chapters/chN_walk.py) into vtest steps for the
real game in vAmiga: clicks on the verbs, things, items and conversation lines,
waits, skips the lines of text, and a screenshot after every step.

    WOS2_CHAPTER=2 python3 tools/vwalk.py > /tmp/steps.txt"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim                                            # noqa: E402

G = sim.G
VERB = {'give': (23, 191), 'pickup': (23, 206), 'use': (23, 221),
        'open': (75, 191), 'look': (75, 206), 'push': (75, 221),
        'close': (131, 191), 'talk': (131, 206), 'pull': (131, 221)}
out = []


def click(x, y):
    out.append(f'g {int(x)} {int(y)}')
    out.append('l')
    out.append('w 1')


def inv(i):
    return 192 + 32 * (i % 4) + 16, 169 + 15 + 31 * (i // 4) + 12


def target(S, o):
    if o in S.inv:
        return inv(S.inv.index(o))
    ob = G.objects[o]
    if ob['actor']:
        r, x, y = S.where[ob['actor']]
        return x, y - 18
    x0, y0, x1, y1 = ob['box']

    def top(x, y):          # the engine picks the last thing in the room's list under the pointer
        hit = None
        for n in G.rooms[S.room]['objects']:
            b = G.objects[n]
            if b['actor'] or not b['box'] or not (S.state[n] & 1):
                continue
            if b['box'][0] <= x <= b['box'][2] and b['box'][1] <= y <= b['box'][3]:
                hit = n
        return hit
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if top(cx, cy) == o:
        return cx, cy
    for fy in (0.5, 0.3, 0.7, 0.15, 0.85):
        for fx in (0.5, 0.3, 0.7, 0.15, 0.85):
            x, y = x0 + (x1 - x0) * fx, y0 + (y1 - y0) * fy
            if top(x, y) == o:
                print(f'note: {o} is partly covered by {top(cx, cy)}', file=sys.stderr)
                return x, y
    raise SystemExit(f'{o} can not be clicked: covered by {top(cx, cy)}')


def skip(n, w=2):
    for _ in range(n):
        out.extend([f'w {w}', 'k 56'])


def main():
    ns = {}
    wf = os.environ.get('VW_WALK') or os.path.join(sim.HERE, 'chapters', f'ch{sim.game.CH}_walk.py')
    exec(open(wf).read(), ns)
    walk = ns['WALK']
    S = sim.Sim()
    if os.environ.get('WOS2_STORY'):           # 'flag,flag|item,item': as if the story file is there
        f, i = os.environ['WOS2_STORY'].split('|')
        S.story = ([x for x in f.split(',') if x], [x for x in i.split(',') if x])
    S.run(G.scripts[[s.name for s in G.scripts].index('start')])
    # the title (loading), the cards, the intro
    out.extend(['w 200', 'k 56', 'w 4'])
    for kind, v in S.events:
        if kind == 'pause':
            out.append(f'w {v}')
        elif kind == 'pick':
            out.extend(['w 3', 'k 56', 'w 3', 'k 56', 'w 4'])
            click(60, 186 + 11 * v)
        else:
            out.extend(['w 4', 'k 56'] if kind == 'card' else ['w 2', 'k 56'])
    out.append('w 4')
    out.append('s v00_start')
    for i, st in enumerate(walk):
        c = st[0]
        if c == 'expect':
            continue
        ev0 = len(S.events)
        inv_before = list(S.inv)
        top = [S.inv_top]

        def tg(o):                      # the click on o: an item (scroll the inventory to it) or a thing
            def f():
                if o in inv_before:
                    i = inv_before.index(o)
                    while i < top[0]:
                        click(183, 190)
                        top[0] -= 4
                    while i >= top[0] + 8:
                        click(183, 220)
                        top[0] += 4
                    return inv(i - top[0])
                return pos
            pos = None if o in inv_before else target(S, o)
            return f
        if c == 'walk' or c == 'talk' or len(st) < 3:
            tgt = [tg(st[1])]
        else:
            tgt = [tg(st[1]), tg(st[2])]
        top0 = S.inv_top
        S.step(st)
        changed = S.inv_top != top0 or S.inv != inv_before
        out.extend(['k 56', 'w 1', 'k 56', 'w 2'])
        if c == 'walk':
            click(*tgt[0]())
            out.append('w 6')
        else:
            click(*VERB[c])
            for t in tgt:
                click(*t())
            if c in ('use', 'give') and len(st) < 3 and st[1] in inv_before:
                click(*tgt[0]())                  # the same item again: use it on its own
            out.append('w 7')
        if not changed:
            S.inv_top = top[0]
        for kind, v in S.events[ev0:]:
            if kind == 'say':
                out.extend(['w 2', 'k 56'])
            elif kind == 'card':
                out.extend(['w 4', 'k 56'])
            elif kind == 'pause':
                out.append(f'w {v}')
            else:
                out.extend(['w 3', 'k 56', 'w 3', 'k 56', 'w 4'])
                click(60, 186 + 11 * v)
        out.append('w 2')
        out.append(f's v{i + 1:02d}_{c}_{st[1]}')
    out.append('w 6')
    out.append('s v_end')
    print('\n'.join(out))


main()
