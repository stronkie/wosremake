#!/usr/bin/env python3
"""The whole of chapter 1 as a vtest step list (python3 walk.py > steps.txt)."""
import sys

VERB = {'give': (23, 191), 'pickup': (23, 206), 'use': (23, 221),
        'open': (75, 191), 'look': (75, 206), 'push': (75, 221),
        'close': (131, 191), 'talk': (131, 206), 'pull': (131, 221)}
out = []
shot = [0]


def at(x, y):
    out.append(f'g {x} {y}')


def click(x, y):
    at(x, y)
    out.append('l')
    out.append('w 1')


def skip(n, w=1):
    for _ in range(n):
        out.extend([f'w {w}', 'k 56'])


def snap(name=None):
    shot[0] += 1
    out.append(f's {name or "w%02d" % shot[0]}')


def do(verb, x, y, wait=4):
    click(*VERB[verb])
    click(x, y)
    out.append(f'w {wait}')


def inv(i):
    return 192 + 32 * (i % 4) + 16, 169 + 15 + 31 * (i // 4) + 12


def use(i, x, y, verb='use', wait=4):
    click(*VERB[verb])
    click(*inv(i))
    click(x, y)
    out.append(f'w {wait}')


def go(x, y, wait=8):
    click(x, y)
    out.append(f'w {wait}')


def dlg(i, wait=2):
    click(60, 186 + 11 * i)
    out.append(f'w {wait}')


# the title and the intro
out += ['w 170', 'k 64', 'w 4', 'k 64', 'w 4', 'k 64', 'w 4', 'k 64', 'w 22']
snap('m_meadow')
do('open', 85, 80, 3)
skip(4, 2)
snap('m_hatch')
go(310, 130)                         # the square
use(0, 50, 120)                      # rope with the well
skip(5, 2)
snap('s_bucket')
go(232, 163)                          # the workshop
do('pickup', 260, 125)
skip(6, 2)
snap('w_chicken')
go(24, 90)                            # back to the square
go(308, 112)                          # the garden
snap('g_garden')
do('talk', 205, 125, 3)
snap('g_dialog')
dlg(0)
skip(8, 2)
snap('g_dialog2')
dlg(3)
skip(3, 2)
go(252, 97)                           # the gorge
snap('o_gorge')
use(2, 178, 72, wait=3)               # the chicken with the zip line
skip(5, 2)
snap('c_cave')
do('pickup', 232, 145)
skip(2, 2)
snap('c_crystal')
use(3, *inv(1))                      # the crystal with the bucket
skip(3, 2)
snap('c_starwater')
go(8, 100)                            # back across
skip(2, 2)
go(50, 162)                           # the garden
use(2, 164, 97)                       # starlit water with the Moonflower
skip(12, 2)
snap('g_bloom')
go(8, 140)                            # the square
use(0, 258, 128, verb='give')         # the coin to Gobbo
skip(6, 2)
snap('s_ribbon')
go(308, 112)                          # the garden
do('talk', 205, 125, 3)
snap('g_ask')
dlg(2)
skip(4, 2)
snap('f_yes')
skip(3, 3)
snap('f_night')
out.append('w 8')
snap('f_dance')
skip(6, 3)
snap('f_shard')
skip(3, 3)
snap('f_end1')
skip(2, 4)
snap('f_end2')
out.append('w 10')
snap('f_after')
out.append('end')
print('\n'.join(out))
