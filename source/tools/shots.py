#!/usr/bin/env python3
"""steps for the screenshots of the manual and the itch page (python3 shots.py full|demo)"""
import sys
sys.argv += ['full']
exec(open(__file__.replace('shots.py', 'walk.py')).read().split('# the title and the intro')[0])
out.extend(['w 120', 's x_title', 'k 64', 'w 4', 's x_card', 'k 64', 'w 4', 'k 64', 'w 4', 'k 64', 'w 4', 's x_intro', 'w 18'])
if sys.argv[1] == 'demo':
    go(310, 130)
    go(308, 112, 4)
    snap('d_gate')
    out.append('w 6')
    snap('d_end')
else:
    do('look', 85, 80, 1)
    snap('x_look')
    skip(2, 2)
    go(310, 130)
    do('look', 50, 120, 1)
    snap('x_well')
    skip(2, 2)
    go(160, 95)                       # the Elder's hut
    do('look', 248, 57, 2)
    snap('x_guru')
    skip(4, 2)
    go(38, 85)                        # the library
    do('look', 160, 47, 2)
    snap('x_monkey')
    skip(4, 2)
    do('look', 140, 124, 2)
    snap('x_book')
    skip(4, 2)
    go(300, 90)                       # back: elder, square, meadow, forest
    go(170, 165)
    go(8, 140)
    go(228, 108)
    do('pull', 93, 110, 2)
    snap('x_sword')
    skip(3, 2)
    go(179, 112)
    snap('x_deep')
out.append('end')
print('\n'.join(out))
