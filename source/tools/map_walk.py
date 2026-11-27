#!/usr/bin/env python3
"""The map of World of Stronkie remake (a poster: every room as a picture, the ways
between them, chapter by chapter) and the walkthrough (PDF + text), made from the
game data (tools/dump_chapter.py JSON files).

    python3 tools/map_walk.py DUMP_DIR OUT_DIR"""
import base64
import io
import json
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'art'))
import orig               # noqa: E402

DUMP, OUTD = sys.argv[1], sys.argv[2]
os.makedirs(OUTD, exist_ok=True)
PRE = 'WorldOfStronkieRemake'

NAMES = {
    'road': 'The Road', 'garden': 'The Garden', 'shed': 'The Shed', 'well': 'The Well', 'porch': 'The Porch',
    'hall': 'The Hall', 'library': 'The Library', 'kitchen': 'The Kitchen', 'cellar': 'The Wine Cellar',
    'study': 'The Study', 'secret': 'The Hidden Chamber', 'stairs': 'The Stairway', 'bunker': 'The Bunker',
    'lockers': 'The Locker Room', 'hangar': 'The Hangar', 'control': 'The Control Room', 'shipin': 'The STARRAVEN',
    'cockpit': 'The Cockpit', 'shipcorr': 'Ship Corridor', 'galley': 'The Galley', 'engine': 'Engine Room',
    'cargo': 'Cargo Hold', 'airlock': 'The Airlock', 'dock': 'Docking Bay KX-9', 'stcorr': 'Station Corridor',
    'quarters': 'Crew Quarters', 'power': 'Power Room', 'maproom': 'The Map Room',
    'pad': 'Landing Pad 42', 'plaza': 'The Plaza', 'bar': 'The SCUMM BAR', 'stan': "Stan's Starships",
    'alley': 'The Alley', 'backroom': "Lefty's Back Room", 'pcockpit': 'Cockpit (tractor beam)',
    'pairlock': 'The Airlock', 'deck': 'Deck of the SPACE MONKEY', 'cabin': "LeChuckle's Cabin",
    'pengine': 'Pirate Engine Room',
    'wreck': 'The Wreck', 'crash': 'The Crash Site', 'jungle': 'The Jungle', 'river': 'The River',
    'ccave': 'The Crystal Cave', 'vgate': 'The Village Gate', 'vsquare': 'Village Square', 'market': 'The Market',
    'elder': "The Elder's Hut", 'workshop': "Bix's Workshop", 'tower': 'The Lookout Tower',
    'ledge': 'The Snowy Ledge', 'icecave': 'The Ice Cave', 'icebridge': 'The Ice Bridge', 'camp': "Vex's Camp",
    'tent': "Vex's Tent", 'steps': 'The Temple Steps', 'tgate': 'The Temple Gate', 'statues': 'Hall of Statues',
    'mirrors': 'The Round Room', 'starbridge': 'The Starbridge', 'heartdoor': 'The Golden Door',
    'heart': 'The Heart Chamber', 'westgal': 'West Gallery', 'eastgal': 'East Gallery', 'altar': 'The Altar',
    'catacomb': 'The Catacombs', 'deadend': 'The Dead End', 'site': "Bix's Workshop", 'mineentry': 'The Old Mines',
    'maze1': 'The Maze (1)', 'maze2': 'The Maze (2)', 'maze3': 'The Maze (3)', 'vein': 'The Crystal Vein',
    'fhangar': 'Hangar, IRON RAVEN', 'fcorr': 'The Checkpoint', 'breakroom': 'The Break Room', 'laundry': 'The Laundry',
    'holodeck': 'Secret Holodeck', 'lift': 'The Lift', 'plift': 'Prison Lobby', 'cellblock': 'The Cellblock',
    'guardroom': 'The Guardroom', 'records': 'Records Room', 'pcontrol': 'Prison Control', 'fbridge': 'The Bridge',
    'comms': 'The Radio Room', 'cannon': 'The Cannon Room', 'vexroom': "Vex's Quarters", 'podbay': 'The Pod Bay',
    'egarden': 'Home: the Garden', 'ehall': 'Home: the Hall', 'estudy': 'Home: the Study'}
CHAPTERS = {1: ('Chapter One', 'The Prologue: Ravenmoor'), 2: ('Chapter Two', 'Into Space'),
            3: ('Chapter Three', 'Asteroid 42'), 4: ('Chapter Four', 'Landfall'),
            5: ('Chapter Five', 'The Crystal Mountains'), 6: ('Chapter Six', 'The Star Heart'),
            7: ('Chapter Seven', "Vex's Flagship")}
# the place of every room on its chapter's grid (column, row): drawn like a real map
GRID = {
    1: {'road': (0, 2), 'garden': (1, 2), 'shed': (1, 3), 'well': (2, 2), 'porch': (1, 1), 'hall': (1, 0),
        'library': (0, 0), 'kitchen': (2, 0), 'cellar': (3, 0), 'study': (2, 1), 'secret': (0, 1),
        'stairs': (4, 0), 'bunker': (4, 1), 'lockers': (5, 1), 'hangar': (4, 2), 'control': (5, 2), 'shipin': (4, 3)},
    2: {'cockpit': (1, 0), 'shipcorr': (1, 1), 'galley': (0, 1), 'engine': (2, 1), 'cargo': (1, 2), 'airlock': (2, 2),
        'dock': (3, 0), 'stcorr': (4, 0), 'quarters': (4, 1), 'power': (5, 1), 'maproom': (5, 0)},
    3: {'pad': (1, 2), 'plaza': (1, 1), 'bar': (0, 1), 'stan': (2, 1), 'alley': (1, 0), 'backroom': (0, 0),
        'pcockpit': (3, 0), 'pairlock': (3, 1), 'deck': (4, 1), 'cabin': (5, 1), 'pengine': (4, 2)},
    4: {'wreck': (0, 1), 'crash': (1, 1), 'jungle': (1, 0), 'river': (2, 0), 'ccave': (3, 0), 'vgate': (2, 1),
        'vsquare': (3, 2), 'market': (4, 2), 'elder': (3, 1), 'workshop': (2, 2), 'tower': (3, 3)},
    5: {'ledge': (0, 1), 'icecave': (0, 0), 'icebridge': (1, 1), 'camp': (2, 1), 'tent': (2, 2), 'steps': (2, 0),
        'tgate': (3, 0), 'statues': (3, 1), 'mirrors': (4, 1), 'starbridge': (4, 0), 'heartdoor': (5, 0)},
    6: {'heart': (1, 0), 'westgal': (0, 0), 'eastgal': (2, 0), 'altar': (1, 1), 'catacomb': (0, 1), 'deadend': (0, 2),
        'site': (3, 0), 'mineentry': (4, 0), 'maze1': (4, 1), 'maze2': (5, 1), 'maze3': (5, 2), 'vein': (4, 2)},
    7: {'fhangar': (0, 1), 'holodeck': (0, 0), 'fcorr': (1, 1), 'breakroom': (1, 0), 'laundry': (1, 2), 'lift': (2, 1),
        'plift': (3, 1), 'cellblock': (3, 0), 'guardroom': (4, 1), 'pcontrol': (4, 0), 'records': (3, 2),
        'fbridge': (5, 1), 'comms': (5, 0), 'cannon': (6, 1), 'vexroom': (5, 2), 'podbay': (6, 2),
        'egarden': (6, 3), 'ehall': (5, 3), 'estudy': (4, 3)}}
DUMPS = {c: json.load(open(os.path.join(DUMP, f'ch{c}.json'))) for c in range(1, 8)}


def uri(im):
    b = io.BytesIO()
    im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


THUMB = {}


def thumb(art):
    if art not in THUMB:
        cv = orig.ROOM_ART[art]() if art in orig.ROOM_ART else orig.base(art)
        im = Image.fromarray((np.clip(cv.c, 0, 1) * 255).astype(np.uint8)).resize((240, 126), Image.LANCZOS)
        THUMB[art] = uri(im)
    return THUMB[art]


CW, CH_, GX, GY = 150, 104, 40, 34      # card size and gaps (px)


def chapter_map(c):
    d = DUMPS[c]
    grid = GRID[c]
    cols = max(x for x, y in grid.values()) + 1
    rows = max(y for x, y in grid.values()) + 1
    W, H = cols * CW + (cols - 1) * GX, rows * CH_ + (rows - 1) * GY

    def centre(r):
        x, y = grid[r]
        return x * (CW + GX) + CW / 2, y * (CH_ + GY) + CH_ / 2
    pairs = {}
    for a, b, lab in d['edges']:
        if a in grid and b in grid:
            pairs.setdefault(tuple(sorted((a, b))), set()).add((a, b))
    lines = ''
    for (a, b), dirs in pairs.items():
        (x1, y1), (x2, y2) = centre(a), centre(b)
        one_way = len(dirs) == 1
        lines += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{"#ff8cc0" if one_way else "#ffd560"}" '
                  f'stroke-width="{3 if one_way else 5}" {"stroke-dasharray=\"8 6\"" if one_way else ""} '
                  f'stroke-linecap="round"/>')
    cards = ''
    for r, art, desc in d['rooms']:
        if r not in grid:
            continue
        x, y = grid[r]
        cards += (f'<div class="card" style="left:{x * (CW + GX)}px;top:{y * (CH_ + GY)}px">'
                  f'<img src="{thumb(art)}"><div>{NAMES.get(r, r)}</div></div>')
    num, name = CHAPTERS[c]
    return (f'<div class="chap"><div class="ct"><span>DISK {c}</span> {num}: {name}</div>'
            f'<div class="field" style="width:{W}px;height:{H}px"><svg width="{W}" height="{H}">{lines}</svg>{cards}</div></div>')


MAP_CSS = '''
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0b0a26; color: #e8e4ff; font-family: Inter, 'DejaVu Sans', sans-serif; padding: 34px 40px; width: 2480px; }
h1 { font-size: 64px; color: #ffd560; letter-spacing: .02em; } h1 span { color: #5ad8ec; }
.sub { font-size: 22px; color: #ff8cc0; margin: 4px 0 26px; }
.maps { display: flex; flex-wrap: wrap; gap: 34px 46px; align-items: flex-start; }
.chap { background: #14123a; border: 3px solid #3a2d7a; border-radius: 14px; padding: 16px 20px 22px; }
.ct { font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 14px; }
.ct span { background: #7a3ad0; border-radius: 6px; padding: 2px 10px; margin-right: 8px; font-size: 18px; }
.field { position: relative; } .field svg { position: absolute; left: 0; top: 0; }
.card { position: absolute; width: 150px; height: 104px; background: #0b0a26; border: 3px solid #ffd560; border-radius: 8px;
        overflow: hidden; box-shadow: 4px 4px 0 #000; }
.card img { width: 144px; height: 76px; display: block; image-rendering: auto; }
.card div { font-size: 12.5px; font-weight: 700; text-align: center; padding: 3px 2px; color: #fff; white-space: nowrap;
            overflow: hidden; }
.legend { margin-top: 26px; font-size: 18px; color: #b8b0d8; display: flex; gap: 40px; align-items: center; }
.legend i { display: inline-block; width: 60px; height: 0; vertical-align: middle; margin-right: 10px; }
'''


def make_map():
    from playwright.sync_api import sync_playwright
    body = ''.join(chapter_map(c) for c in range(1, 8))
    html = (f'<html><head><style>{MAP_CSS}</style></head><body><h1>WORLD OF STRONKIE <span>remake</span>: THE MAP</h1>'
            f'<div class="sub">Every room of all seven disks, and the ways between them. Created By Mark Stronks, Stronkie Soft.</div>'
            f'<div class="maps">{body}</div><div class="legend"><span><i style="border-top:5px solid #ffd560"></i>a way '
            f'there and back</span><span><i style="border-top:3px dashed #ff8cc0"></i>one way only (a flight, a lift, a '
            f'jump, a story moment)</span></div></body></html>')
    png = os.path.join(OUTD, f'{PRE}_Map.png')
    pdfp = os.path.join(OUTD, f'{PRE}_Map.pdf')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 2560, 'height': 1000})
        pg.set_content(html, wait_until='load')
        h = pg.evaluate('document.body.scrollHeight')
        pg.set_viewport_size({'width': 2560, 'height': h + 40})
        pg.screenshot(path=png, full_page=True)
        pg.pdf(path=pdfp, width='2560px', height=f'{h + 40}px', print_background=True,
               margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        b.close()
    return png, pdfp


# ================================================================== the walkthrough
INTRO = """WORLD OF STRONKIE REMAKE - THE COMPLETE WALKTHROUGH
Created By Mark Stronks, Stronkie Soft. For all seven disks, V1.0.

How to read it: every line is one click (or a few). "Use the X with the Y": click Use,
then the X in your inventory, then the Y. "Talk to ...: say ...": pick those lines in
the conversation. Walk lines take you to the next room.

You can never die and never get stuck. This walkthrough takes every good choice and
finds all 16 star fragments, so you get the TRUE ENDING.

THE KEEPSAKES (the item check list): every disk gives you one thing you must keep:
  Disk 1 scrap of paper, 2 space ration, 3 rubber chicken, 4 singing shell,
  5 spiked boots, 6 silver horn. Every later disk checks they are in your inventory.

CHOICES THAT MATTER (all optional, they pay off on disk 7):
  Disk 3: give the napkin to Roger (after the burger) -> he gets you the keycard.
  Disk 3: kick (Push) the Astro Chicken machine     -> the guards are your fans.
  Disk 3: untie Ricky                                -> he brings the plasma spanner.
  Disk 3: answer LeChuckle's rematch                 -> the pirates stay out of it.
  Disk 4: find the wooden monkey in the bushes       -> the secret holodeck.
  Disk 4: put on the nose glasses                    -> a disguise at the checkpoint.
"""
CH_NOTES = {
    1: 'At the start: the title, then the letter from Uncle Edmund.',
    2: 'Put in disk 2: it reads your story from disk 1 (keep disk 1 at hand when playing from floppies).',
    3: 'Disk 3. The insults: the pirates in the bar teach you the first comeback, the parrot the second, Ricky the '
       'one for LeChuckle.',
    4: 'Disk 4. Until you listen to the singing shell, the Stronkies only chirp.',
    5: 'Disk 5. Wear the spiked boots before you try the ice bridge.',
    6: 'Disk 6. In the maze, ask Pip: north, east, then down the hole.',
    7: 'Disk 7. The Insult-O-Tron: the answers are on the poster in the break room and from the laundry robot; '
       'the first one is Pip\'s joke from disk 6.',
}


def walkthrough():
    txt = [INTRO]
    html = []
    for c in range(1, 8):
        num, name = CHAPTERS[c]
        txt.append(f'\n{"=" * 70}\nDISK {c} - {num.upper()}: {name.upper()}\n{"=" * 70}\n{CH_NOTES[c]}\n')
        html.append(f'<h2><span>DISK {c}</span> {num}: {name}</h2><p class="note">{CH_NOTES[c]}</p>')
        last = None
        for room, line in DUMPS[c]['walk']:
            if room != last:
                txt.append(f'\n  [{NAMES.get(room, room)}]')
                html.append(f'<h3>{NAMES.get(room, room)}</h3>')
                last = room
            txt.append(f'  - {line}')
            star = ' class="star"' if 'star fragment' in line else ''
            html.append(f'<div{star}>{line}</div>')
    txt.append('\nTHE END. With all 16 star fragments on Uncle Edmund\'s desk you see the TRUE ENDING.\n')
    tp = os.path.join(OUTD, f'{PRE}_Walkthrough.txt')
    open(tp, 'w').write('\n'.join(txt))
    css = '''* { margin:0; padding:0; box-sizing:border-box; } body { font-family: Inter, 'DejaVu Sans', sans-serif;
      font-size: 9pt; color: #1a1430; padding: 12mm 14mm; line-height: 1.38; }
      h1 { font-size: 18pt; color: #3b1f73; } pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.8pt;
      background: #f4eefc; padding: 3mm; border-radius: 1mm; margin: 3mm 0 4mm; white-space: pre-wrap; }
      h2 { font-size: 12pt; color: #3b1f73; margin: 5mm 0 1mm; page-break-after: avoid; }
      h2 span { background: #7a3ad0; color: #fff; font-size: 8pt; padding: .5mm 2mm; border-radius: 1mm; }
      h3 { font-size: 9.5pt; color: #6a2f9a; margin: 2.5mm 0 .5mm; page-break-after: avoid; }
      .note { font-style: italic; color: #6a5d86; } div { padding-left: 4mm; text-indent: -2.5mm; }
      div:before { content: '\\2022  '; color: #8a52d0; } .star { color: #b07800; font-weight: 700; }
      @page { size: A4; margin: 12mm 0; }'''
    from playwright.sync_api import sync_playwright
    page = (f'<html><head><style>{css}</style></head><body><h1>World of Stronkie remake: the walkthrough</h1>'
            f'<pre>{INTRO.split(chr(10), 2)[2]}</pre>{"".join(html)}<p style="margin-top:5mm"><b>THE END.</b> With all '
            f'16 star fragments on Uncle Edmund\'s desk you see the true ending. Created By Mark Stronks, Stronkie Soft.'
            f'</p></body></html>')
    pp = os.path.join(OUTD, f'{PRE}_Walkthrough.pdf')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content(page, wait_until='load')
        pg.pdf(path=pp, format='A4', print_background=True,
               margin={'top': '12mm', 'bottom': '12mm', 'left': '0', 'right': '0'})
        b.close()
    return tp, pp


if __name__ == '__main__':
    print(*make_map())
    print(*walkthrough())
