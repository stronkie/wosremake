#!/usr/bin/env python3
"""Plays the game disk in vAmigaWeb (the toolkit's emu/, AROS ROMs) in headless
Chrome, with the mouse: for testing World of Stronkie remake without vAmiga headless.

    python3 tools/webplay.py disk.adf outdir steps.txt
Steps (one per line):
    w SECONDS        wait (emulated time runs in real time)
    s NAME           screenshot outdir/NAME.png
    g X Y            pointer to game pixel X,Y (pins the pointer top-left, then moves)
    l / r            left / right click
    k KEY            a key (playwright name: Space, Escape, F5, KeyL ...)
    shell CMD        a RetroShell command (vAmiga)
The ADF must be in the toolkit's emu/vamigaweb/emu/games/ and serve.py running.
"""
import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright

adf, outdir, stepfile = sys.argv[1:4]
steps = [ln.strip() for ln in open(stepfile) if ln.strip() and not ln.startswith('#')]
os.makedirs(outdir, exist_ok=True)
cfg = {"url": f"http://127.0.0.1:8000/games/{adf}", "AROS": True, "port1": True, "navbar": False,
       "dialog_on_missing_roms": False, "dialog_on_disk": False, "mouse": True}
url = "http://127.0.0.1:8000/index.html#" + json.dumps(cfg)
SCALE = float(os.environ.get('WP_SCALE', '1'))        # mouse counts per lores pixel


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome',
                                    args=['--autoplay-policy=no-user-gesture-required', '--use-gl=swiftshader',
                                          '--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width': 1024, 'height': 900})
        logs = []
        pg.on('console', lambda m: logs.append(m.text))
        await pg.goto(url)

        async def mouse(dx, dy):
            await pg.evaluate(f'Module._wasm_mouse(1,{dx},{dy})')

        for st in steps:
            a = st.split()
            c = a[0]
            if c == 'w':
                await pg.wait_for_timeout(int(float(a[1]) * 1000))
            elif c == 's':
                await pg.screenshot(path=os.path.join(outdir, a[1] + '.png'))
            elif c == 'g':
                for _ in range(8):            # (moves are 8-bit counters on the Amiga: steps under 128)
                    await mouse(-100, -100)
                    await pg.wait_for_timeout(40)
                x, y = float(a[1]), float(a[2])
                n = 8
                for _ in range(n):
                    await mouse(int(round(x * SCALE / n)), int(round(y * SCALE / n)))
                    await pg.wait_for_timeout(40)
                await pg.wait_for_timeout(150)
            elif c in ('l', 'r'):
                btn = 1 if c == 'l' else 3
                await pg.evaluate(f'Module._wasm_mouse_button(1,{btn},1)')
                await pg.wait_for_timeout(120)
                await pg.evaluate(f'Module._wasm_mouse_button(1,{btn},0)')
                await pg.wait_for_timeout(200)
            elif c == 'k':
                await pg.keyboard.down(a[1])
                await pg.wait_for_timeout(150)
                await pg.keyboard.up(a[1])
                await pg.wait_for_timeout(200)
            elif c == 'shell':
                await pg.evaluate(f'wasm_retro_shell({json.dumps(" ".join(a[1:]))})')
                await pg.wait_for_timeout(300)
        open(os.path.join(outdir, 'console.txt'), 'w').write('\n'.join(logs))
        await b.close()

asyncio.run(main())
