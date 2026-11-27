#!/usr/bin/env python3
"""Runs the game disk in vAmiga headless (AROS ROM, 2 MB fast RAM) and
takes screenshots.  Steps (one per argument or line in a file):
    w N          wait N seconds
    s NAME       screenshot NAME.png (lores, 320 wide)
    m DX DY      move the mouse
    l / r        left / right click
    k N          press raw key N
    g X Y        put the pointer at room/screen pixel X,Y (from the top left corner)"""
import os
import subprocess
import sys
import numpy as np
from PIL import Image

VA = '/home/claude/tools/vamiga/build/VAHeadless'
BIN = '/home/claude/tools/vamiga/Resources/Assets.xcassets/Binary'
ROM = BIN + '/aros-20250219-rom.dataset/aros-20250219-rom.bin'
EXT = BIN + '/aros-20250219-ext.dataset/aros-20250219-ext.bin'
SCALE = 1
W, H = 912 - 4 * 0x31, 313 - 2 - 0x1a


def run(adf, steps, outdir):
    os.makedirs(outdir, exist_ok=True)
    rom = os.environ.get('VT_ROM')     # a real Kickstart image (not in the repo), else AROS
    setup = f'regression setup A500_ECS_1MB {rom}' if rom else f'regression setup A500_ECS_1MB {ROM} {EXT}'
    lines = [setup, 'mem set FAST_RAM 2048', 'paula dc set SPEED 8', *os.environ.get('VT_PRE','').split(';'),
             f'regression run {adf}']
    shots = []
    for st in steps:
        a = st.split()
        if not a:
            continue
        c = a[0]
        if c == 'w':
            lines.append(f'wait {a[1]} seconds')
        elif c == 's':
            name = f'vt{os.getpid()}_{len(shots)}'
            shots.append((name, a[1]))
            lines.append(f'screenshot save {name}')
        elif c == 'm':
            lines.append(f"mouse1 move {a[1].replace('-', 'm')} {a[2].replace('-', 'm')}")
        elif c == 'l':
            lines.append('mouse1 press left')
        elif c == 'r':
            lines.append('mouse1 press right')
        elif c == 'x':
            lines.append(st[2:])
        elif c == 'k':
            lines.append(f'keyboard press {a[1]}')
        elif c == 'g':        # home the pointer to the top left, then move there
            for _ in range(5):
                lines.append('mouse1 move m100 m100')
                lines.append('wait 1 seconds')
            x, y = int(a[1]) * SCALE, int(a[2]) * SCALE
            while x or y:
                sx, sy = max(-100, min(100, x)), max(-100, min(100, y))
                lines.append(f"mouse1 move {str(sx).replace('-', 'm')} {str(sy).replace('-', 'm')}")
                lines.append('wait 1 seconds')
                x -= sx
                y -= sy
    lines.append('screenshot quit')
    ini = os.path.join(outdir, 'run.ini')
    open(ini, 'w').write('\n'.join(lines) + '\n')
    r = subprocess.run([VA, '-v', ini] if os.environ.get('VT_V') else [VA, ini], capture_output=True, text=True, timeout=1800)
    if r.returncode not in (0, 1):
        print(r.stdout[-2000:], r.stderr[-2000:])
    if os.environ.get('VT_V'):
        open(os.path.join(outdir, 'log.txt'), 'w').write(r.stdout)
    out = []
    for name, nice in shots:
        raw = f'/tmp/{name}.raw'
        if not os.path.exists(raw):
            print('no screenshot', name, r.stdout[-1500:])
            continue
        a = np.fromfile(raw, np.uint8)
        a = a[:W * H * 3].reshape(H, W, 3)
        img = Image.fromarray(a[:, ::2])
        p = os.path.join(outdir, nice + '.png')
        img.save(p)
        os.remove(raw)
        out.append(p)
    return out


if __name__ == '__main__':
    adf = os.path.abspath(sys.argv[1])
    outdir = sys.argv[2]
    steps = sys.argv[3:]
    if len(steps) == 1 and os.path.exists(steps[0]):
        steps = open(steps[0]).read().splitlines()
    print('\n'.join(run(adf, steps, outdir)))
