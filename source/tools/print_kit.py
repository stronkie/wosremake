#!/usr/bin/env python3
"""The print kit of World of Stronkie remake: the manual (an A5 booklet), the
disk labels (A4), the fold-up box (A3 and A4) and a 3D picture of the box.

    python3 tools/print_kit.py SHOTS_DIR OUT_DIR

SHOTS_DIR holds emulator screenshots (1024 x 900, as tools/webplay.py makes them),
named cN_something.png (N = disk)."""
import base64
import io
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..')
sys.path.insert(0, SRC)
sys.path.insert(0, os.path.join(SRC, 'art'))
import loading            # noqa: E402
import people             # noqa: E402
import orig               # noqa: E402

SHOTS, OUTD = sys.argv[1], sys.argv[2]
os.makedirs(OUTD, exist_ok=True)
VERSION = 'V1.0'
TITLE = 'World of Stronkie remake'
PRE = 'WorldOfStronkieRemake'


def uri(im, fmt='PNG'):
    b = io.BytesIO()
    im.save(b, fmt)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()


def shot(name, panel=True):
    """an emulator screenshot: the game screen, 640 wide"""
    im = Image.open(os.path.join(SHOTS, name + '.png')).convert('RGB')
    im = im.crop((23, 67, 1003, 857 if panel else 581))
    return im.resize((640, int(im.height * 640 / im.width)), Image.LANCZOS)


def room(name):
    """a clean picture of a room, straight from the art (640 x 336)"""
    cv = orig.ROOM_ART[name]()
    return Image.fromarray((np.clip(cv.c, 0, 1) * 255).astype(np.uint8))


def loading_parts():
    a, full, soft = loading.make(1)
    ca, cf, pal = loading.quantize32(a, full, soft)
    img = Image.fromarray((pal[ca] * 255).astype(np.uint8))
    title = img.crop((14, 8, 306, 54))
    x0, y0, x1, y1 = loading.SCENE
    return img, title, img.crop((x0, y0, x1, y1))


def big(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def sprite(look):
    pal = np.array([[int(c[i], 16) * 17 for i in (1, 2, 3)] for c in people.FIXED], np.uint8)
    if look in ('pip', 'bix', 'zooma'):
        kw = {'bix': dict(extra=people.bix_extra),
              'zooma': dict(fur=people.SILVER, light=people.WHITE, extra=people.zooma_extra, h=24)}.get(look, {})
        s = loading.big_sprite(people.stronkie, 'front', **kw)
    else:
        s = loading.big_sprite(people.human, getattr(people, look.upper()), 'front', None)
    ys, xs = np.nonzero(s >= 0)
    s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    rgba = np.zeros(s.shape + (4,), np.uint8)
    m = s >= 0
    rgba[m, :3] = pal[s[m] - 16]
    rgba[m, 3] = 255
    return Image.fromarray(rgba)


LOADING, TITLE_IMG, SCENE = loading_parts()
LOGO = Image.open(os.path.join(SRC, 'images', 'stronkiesoft_logo.png')).convert('RGBA')
U = {'title': uri(big(TITLE_IMG, 4)), 'scene': uri(big(SCENE, 4)), 'loading': uri(big(LOADING, 2)), 'logo': uri(LOGO)}
SH = {}
for f in sorted(os.listdir(SHOTS)):
    if f.endswith('.png'):
        SH[f[:-4]] = uri(shot(f[:-4]))
        SH[f[:-4] + '_room'] = uri(shot(f[:-4], False))
for r in ('road', 'hall', 'hangar', 'cockpit', 'stcorr', 'bar', 'deck', 'jungle', 'vsquare', 'tgate', 'statues',
          'heart', 'mineentry', 'fbridge', 'egarden', 'cabin', 'starbridge', 'pad', 'icebridge', 'cellblock'):
    SH['r_' + r] = uri(room(r))
SPR = {k: uri(big(sprite(k), 3)) for k in ['pilot', 'edmund', 'vex', 'roger', 'pip', 'bix', 'zooma']}


def s(n, room=False, cls='shot'):
    key = n + ('_room' if room else '')
    return f'<img class="{cls}" src="{SH[key]}">' if key in SH else ''


# ------------------------------------------------------------------ shared CSS
CSS = '''
@font-face { font-family: X; src: local('Inter'); }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Inter, 'DejaVu Sans', sans-serif; color: #1a1430; -webkit-print-color-adjust: exact; }
img { image-rendering: pixelated; }
.night { background: #0b0a26; color: #e8e4ff; }
.gold { color: #ffd560; }
.pink { color: #ff8cc0; }
'''


def pdf(html, path, width, height, landscape=False):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content(html, wait_until='load')
        pg.pdf(path=path, width=width, height=height, print_background=True,
               margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        b.close()


def png(html, path, w, h):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.set_content(html, wait_until='load')
        pg.screenshot(path=path, omit_background=True)
        b.close()


# ================================================================== the manual
MAN_CSS = CSS + '''
@page { size: 148mm 210mm; margin: 0; }
.page { width: 148mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always;
        background: #fbf6ea; padding: 13mm 12mm 14mm 12mm; font-size: 8.6pt; line-height: 1.38; }
.page.night { background: #0b0a26; }
.head { position: absolute; top: 5mm; left: 12mm; right: 12mm; font-size: 6.5pt; letter-spacing: .08em;
        text-transform: uppercase; color: #8a7aa8; display: flex; justify-content: space-between;
        border-bottom: .3mm solid #d8cde8; padding-bottom: 1mm; }
.foot { position: absolute; bottom: 6mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #8a7aa8; }
h1 { font-size: 17pt; color: #3b1f73; margin-bottom: 3mm; letter-spacing: -.01em; }
h2 { font-size: 10.5pt; color: #6a2f9a; margin: 3.5mm 0 1.5mm; }
p { margin-bottom: 2mm; }
ul { margin: 0 0 2mm 4.5mm; } li { margin-bottom: .8mm; }
.shot { width: 100%; border: .6mm solid #2a1d55; border-radius: .8mm; display: block; margin: 2mm 0 1mm; }
.cap { font-size: 7pt; color: #6a5d86; font-style: italic; margin-bottom: 2mm; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.two .shot { margin: 0; }
table { width: 100%; border-collapse: collapse; font-size: 8pt; margin: 1mm 0 2mm; }
td, th { border-bottom: .25mm solid #ddd2ea; padding: 1mm 1.2mm; text-align: left; vertical-align: top; }
th { background: #3b1f73; color: #fff; font-weight: 600; }
.box { background: #efe6fb; border-left: 1.2mm solid #8a52d0; padding: 2mm 3mm; margin: 2mm 0; border-radius: .8mm; }
.letter { font-family: 'DejaVu Serif', serif; font-size: 8.8pt; background: #fffdf5; border: .3mm solid #e4d8b8;
          padding: 4mm 5mm; box-shadow: 1mm 1mm 0 #e9dfc4; transform: rotate(-.6deg); margin: 2mm 0 4mm; }
.who { display: grid; grid-template-columns: 22mm 1fr; gap: 3mm; align-items: center; margin-bottom: 2.6mm; }
.who img { max-width: 22mm; max-height: 30mm; justify-self: center; }
.who b { color: #3b1f73; font-size: 9.5pt; }
.fact { display: grid; grid-template-columns: 8mm 1fr; gap: 2mm; margin-bottom: 2.2mm; }
.fact span { background: #ffd560; color: #3b1f73; border-radius: 50%; width: 7mm; height: 7mm; display: flex;
             align-items: center; justify-content: center; font-weight: 800; }
.log { border-left: .6mm solid #c9b2ec; margin-left: 2mm; padding-left: 4mm; }
.log div { margin-bottom: 2.4mm; } .log b { color: #6a2f9a; }
.check { list-style: none; margin-left: 0; } .check li:before { content: '\\2610  '; color: #6a2f9a; }
.chap { font-size: 7pt; font-weight: 800; letter-spacing: .14em; color: #fff; background: #7a3ad0;
        display: inline-block; padding: .8mm 2.4mm; border-radius: .8mm; margin-bottom: 1.5mm; }
.lines div { border-bottom: .3mm solid #cbbfdc; height: 7.5mm; }
'''


LAB_CSS = CSS + '''
@page { size: 210mm 297mm; margin: 0; }
.sheet { width: 210mm; height: 297mm; padding: 12mm 14mm; position: relative; }
.grid { display: grid; grid-template-columns: repeat(2, 70mm); gap: 8mm 14mm; justify-content: center; margin-top: 4mm; }
.lab { width: 70mm; height: 70mm; border: .25mm dashed #999; position: relative; overflow: hidden; background: #0b0a26;
       color: #fff; }
.fold { height: 13mm; background: #0b0a26; border-bottom: .3mm dashed #ffd560; transform: rotate(180deg);
        display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 7.5pt;
        color: #ffd560; letter-spacing: .06em; }
.lab .t { width: 64mm; display: block; margin: 2mm auto 0; }
.lab .sc { width: 50mm; display: block; margin: 1.5mm auto 0; border: .3mm solid #5a6ad0; }
.lab .d { position: absolute; bottom: 7.5mm; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 8pt;
          background: #7a3ad0; padding: .8mm 0; letter-spacing: .1em; }
.lab .demo { background: #d03a5a; }
.lab .c { position: absolute; bottom: 1.6mm; left: 0; right: 0; text-align: center; font-size: 5.2pt; color: #b8b0d8; }
.lab .n { text-align: center; font-weight: 800; font-size: 6.4pt; color: #ffd560; margin-top: 1.4mm; letter-spacing: .04em; }
.lab .lg { position: absolute; top: 15mm; right: 2mm; width: 14mm; }
h1 { font-size: 13pt; } .note { font-size: 8pt; color: #555; margin-top: 1mm; }
'''



def mpage(body, num=None, night=False, head=True):
    h = f'<div class="head"><span>{TITLE}</span><span>Instruction manual</span></div>' if head else ''
    f = f'<div class="foot">- {num} -</div>' if num else ''
    return f'<div class="page{" night" if night else ""}">{h}{body}{f}</div>'


CHAPTERS = [
    (1, 'The Prologue', 'Ravenmoor Manor, the grounds and the launch pad', 'scrap of paper'),
    (2, 'Into Space', 'the STARRAVEN and the derelict station KX-9', 'space ration'),
    (3, 'Asteroid 42', 'the space port and the pirate ship SPACE MONKEY', 'rubber chicken'),
    (4, 'Landfall', 'the crash, the jungle and the village of the Stronkies', 'singing shell'),
    (5, 'The Crystal Mountains', "the ice caves, Vex's camp and the Sky Temple", 'spiked boots'),
    (6, 'The Star Heart', 'the heart of the temple and the old crystal mines', 'silver horn'),
    (7, "Vex's Flagship", 'the IRON RAVEN, the prison deck, the bridge... and home', '-'),
]
NUM = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven'}
STORY = {
    1: 'A letter from your Uncle Edmund brought you to Ravenmoor on a stormy night: "Come at once. I have found it." '
       'Nobody has seen him since. Dig, crank and sneak your way into the manor, free your uncle from the hidden '
       'chamber and launch the STARRAVEN from the secret hangar under the house.',
    2: 'NOVA, the ship\'s computer, wakes up. The navigation crystal is cracked, there is no gravity in the cargo hold, '
       'and the star chart to Stronkie lies on station KX-9, where a security robot still asks for the access code.',
    3: 'Out of fuel at the most wretched hive of scum and villainy this side of Andromeda. Feed a hungry janitor, win '
       'big at SLOTS-O-DEATH and buy a fuel cell (free chicken included). Then space pirates grab the STARRAVEN: '
       'time for a sword fight. With insults.',
    4: 'A crash landing on the World of Stronkie. Put out the fire, swing across the glowing river, find a power '
       'crystal, and make friends with the Stronkies. If only you could understand a word they say...',
    5: 'Someone stole the amulet! Cross the ice bridge, sneak into Vex\'s tent, and climb the endless crystal stairs '
       'to the Sky Temple, where a mirror, a sunbeam and a handful of star dust open the way.',
    6: 'Commander Vex wants the power of the Star Heart. A silver horn, a pulled plug and an old lever turn the tables. '
       'Then the STARRAVEN needs a new engine, and the way to the star crystal leads through a maze of twisty '
       'little passages. Bring a friend with glowing ears.',
    7: 'Uncle Edmund is a prisoner on the IRON RAVEN. Get past the checkpoint, out-insult the Insult-O-Tron 3000, free '
       'the prisoners and stop the star cannon. Then learn who Vex really is, and bring everybody home.',
}
SHOTS2 = {1: [('c1_shed', 'The garden shed.'), ('c1_library', 'The library of Ravenmoor Manor.')],
          2: [('c2_galley', 'The galley of the STARRAVEN.'), ('c2_robot', '"ACCESS CODE REQUIRED."')],
          3: [('c3_bar', 'The SCUMM BAR.'), ('c3_deck', 'An insult sword fight on the SPACE MONKEY.')],
          4: [('c4_gate', 'The guard of the village is hungry.'), ('c4_bix', 'Bix the inventor in his workshop.')],
          5: [('c5_camp', "Vex's camp in the snow."), ('c5_statues', 'The Hall of Statues.')],
          6: [('c6_vex', 'Commander Vex at the Star Heart.'), ('c6_mine', 'Pip and his kite.')],
          7: [('c7_tron', 'The Insult-O-Tron 3000.'), ('c7_bridge', 'The bridge of the IRON RAVEN.')]}
ROOMPIC = {1: 'r_hall', 2: 'r_cockpit', 3: 'r_bar', 4: 'r_vsquare', 5: 'r_statues', 6: 'r_heart', 7: 'r_fbridge'}


def pic(key, cap=''):
    if key in SH:
        return f'<div><img class="shot" src="{SH[key]}"><div class="cap">{cap}</div></div>'
    return ''


def chapter_page(n, num):
    nm, where, keep = CHAPTERS[n - 1][1:]
    cells = ''.join(pic(k, c) for k, c in SHOTS2[n])
    if not cells.strip():
        cells = pic(ROOMPIC[n], where.capitalize() + '.')
    keepline = f'<div class="box"><b>Keepsake of this disk:</b> the {keep}. Keep it: the next disks check for it.</div>' \
        if keep != '-' else '<div class="box"><b>The last disk.</b> With all 16 star fragments you see the true ending.</div>'
    return mpage(f'''<div class="chap">CHAPTER {NUM[n].upper()} &middot; DISK {n}</div>
      <h1>{nm}</h1><p style="font-size:7.6pt;color:#6a5d86"><b>Where:</b> {where}</p>
      <p>{STORY[n]}</p><div class="two">{cells}</div>{keepline}''', num)


def manual():
    P = []
    P.append(f'''<div class="page night" style="padding:0">
      <div style="background:#ffd560;color:#2a1450;text-align:center;font-weight:800;letter-spacing:.2em;
        font-size:8pt;padding:2.2mm">STRONKIE SOFT PRESENTS</div>
      <img src="{U['title']}" style="width:132mm;display:block;margin:6mm auto 0">
      <img src="{U['scene']}" style="width:132mm;display:block;margin:5mm auto;border:.8mm solid #5a6ad0">
      <div style="text-align:center;font-size:21pt;font-weight:800;color:#fff;margin-top:3mm">INSTRUCTION MANUAL</div>
      <div style="text-align:center;font-size:10pt;color:#ff8cc0;margin-top:1mm">The classic adventure, now point &amp; click</div>
      <div style="text-align:center;font-size:7.4pt;color:#b8b0d8;margin-top:1.5mm;line-height:1.5">
        The complete game: seven chapters on seven disks</div>
      <div style="margin:4mm 10mm 0;background:#d8202f;color:#fff;text-align:center;font-weight:800;font-size:8pt;padding:2mm;line-height:1.3">
        FOR THE AMIGA 500 WITH 1 MB (512K CHIP + 512K TRAPDOOR)<br>KICKSTART / WORKBENCH 3.1 &middot; NO ACCELERATOR NEEDED</div>
      <div style="position:absolute;bottom:20mm;left:0;right:0;text-align:center"><img src="{U['logo']}" style="width:40mm"></div>
      <div style="position:absolute;bottom:0;left:0;right:0;background:#7a3ad0;color:#fff;text-align:center;
        font-weight:800;font-size:12pt;letter-spacing:.15em;padding:3mm">AMIGA 500 &middot; 1 MB &middot; 7 DISKS</div></div>''')
    P.append(mpage(f'''<h1>Welcome to Ravenmoor</h1>
      <p>Thank you for buying <b>{TITLE}</b>! This is the original <b>World of Stronkie</b>, the text adventure,
      rebuilt from the ground up as a <b>point-and-click adventure</b> on the engine of World of Stronkie II.
      The same story, the same puzzles, the same pictures, music and speech. But no more typing: you point,
      pick a verb and click.</p>
      <p>The game comes on <b>seven disks</b>, one for every chapter. Your story travels with you from disk to disk.
      You can never die, and you can never get stuck.</p>
      <h2>In this manual</h2>
      <table><tr><td>A letter from Uncle Edmund</td><td>3</td></tr><tr><td>What you need, loading</td><td>4</td></tr>
      <tr><td>The seven disks, hard drive, WHDLoad</td><td>5</td></tr><tr><td>Your story and the item check list</td><td>6</td></tr>
      <tr><td>How to play, the verbs and keys</td><td>7</td></tr><tr><td>Who is who</td><td>8</td></tr>
      <tr><td>The seven chapters</td><td>9</td></tr><tr><td>Star fragments and choices</td><td>16</td></tr>
      <tr><td>Hints</td><td>17</td></tr><tr><td>Credits</td><td>18</td></tr></table>
      {pic('c1_control', 'The control room under the manor.')}''', 2))
    P.append(mpage(f'''<h1>A letter from Uncle Edmund</h1>
      <div class="letter">My dear nephew,<br><br>
      Come to Ravenmoor at once. I have found it.<br><br>
      For forty years the old legends were all I had: a lost world, a heart of starlight, and a ship built to find
      them. Tonight the amulet glows. Others know it too, and they are coming.<br><br>
      Come at once. Trust nobody. And if I am not here when you arrive... look under the doormat.<br><br>
      Your uncle,<br><b>Edmund Ravenmoor</b></div>
      <p>And so, on a stormy night, you stand at the gates of Ravenmoor Manor. Lightning flashes. For a moment you
      see a pale face at an upstairs window. The adventure begins.</p>
      <img class="shot" src="{SH['r_road']}"><div class="cap">The road to Ravenmoor Manor.</div>''', 3))
    P.append(mpage(f'''<h1>What you need</h1>
      <div style="border:.8mm solid #d8202f;background:#fde8ea;padding:2.5mm 3mm;margin-bottom:3mm;border-radius:1mm">
        <b style="color:#b0101c;font-size:10pt">An Amiga 500 with 1 MB is all you need.</b><br>
        No accelerator and no fast memory: 512 KB chip memory plus the 512 KB trapdoor expansion. Try the free
        demo first: if the demo runs, all seven disks run too.</div>
      <ul><li>An <b>Amiga 500</b> (68000, 7 MHz) with <b>Kickstart and Workbench 3.1</b></li>
      <li><b>1 MB memory</b>: 512 KB chip + 512 KB trapdoor</li>
      <li>A mouse in port 1, and speakers for the music and the speech</li>
      <li>One floppy drive is enough. A hard drive, CF card or WHDLoad is nicer.</li></ul>
      <h2>Loading from the floppy</h2>
      <p>Put the disk of the chapter in DF0: and switch on (or reset) the Amiga. The loading screen appears and the
      bar fills while the game loads.</p>
      <img class="shot" src="{U['loading']}" style="width:80mm;margin:1mm auto 0"><div class="cap" style="text-align:center">The loading screen.</div>''', 4))
    rows = ''.join(f'<tr><td><b>Disk {n}</b></td><td>Chapter {NUM[n]}: {nm}</td><td>{"WOSR" if n == 1 else f"WOSRC{n}"}</td></tr>'
                   for n, nm, w, k in CHAPTERS)
    P.append(mpage(f'''<h1>The seven disks</h1>
      <p>Every chapter is a complete disk of its own. Play them in order: each chapter starts where the last one ended.
      Disk names: <b>Stronkie Remake Ch 1 {VERSION}</b> ... <b>Ch 7 {VERSION}</b>.</p>
      <table><tr><th>Disk</th><th>Chapter</th><th>Program</th></tr>{rows}</table>
      <h2>Playing from the hard drive or CF card</h2>
      <p>Make <b>one</b> drawer, for example <b>Games:WorldOfStronkieRemake</b>, and copy the files of <b>all</b> seven
      disks into it: the program, its .DAT, .GFX and .STR files and its icon. Double-click the icon of a chapter.</p>
      <div class="box"><b>Keep all chapters in the same drawer.</b> That is where each chapter leaves your story for
      the next one. Then the next chapter finds it by itself.</div>
      <h2>WHDLoad</h2>
      <p>The WHDLoad version holds all seven chapters in one drawer, <b>WorldOfStronkieRemake</b>, each with its own
      icon. F10 quits back to the Workbench.</p>''', 5))
    P.append(mpage(f'''<h1>Your story and the item check list</h1>
      <p>When you finish a chapter, the game writes your story into a small file: <b>the star fragments you found,
      the choices you made and the things you carry</b>. The next chapter reads it.</p>
      <h2>From floppies</h2>
      <p>The story is written to <b>the disk you just finished</b>, so keep it write-enabled. The next disk asks:
      <i>"Put the Chapter One disk in the drive."</i> Swap disks, click, then put the new disk back when it asks.</p>
      <h2>The item check list</h2>
      <p>Every disk gives you one <b>keepsake</b>: a thing you keep for the rest of the game. At the start of every
      disk the game checks the keepsakes of <b>all</b> the disks before it. If one is missing, the disk says
      <b>ITEM CHECK FAILED</b> and goes no further: play the disk before it to the end.</p>
      <table><tr><th>Disk</th><th>Keepsake</th></tr>
      {''.join(f'<tr><td>{n}</td><td>{k}</td></tr>' for n, nm, w, k in CHAPTERS if k != '-')}</table>
      <div class="box">The story file has a check code. A story file made or changed by hand is refused.</div>''', 6))
    P.append(mpage(f'''<h1>How to play</h1>
      <p>The <b>room</b> is at the top; the <b>panel</b> at the bottom has the sentence line, the nine verbs and your
      inventory (the arrows scroll it when you carry more than eight things).</p>
      {pic('c4_square', 'The village square. The sentence line says what you point at.')}
      <ul><li><b>Walk:</b> click anywhere in the room. Click an exit to go to the next room.</li>
      <li><b>Do things:</b> click a verb, then a thing. <i>Use</i> and <i>Give</i> take two things:
      <i>Use rubber chicken with outer door</i>.</li>
      <li><b>Use an item on its own:</b> <i>Use</i>, then the same item twice (put on the boots).</li>
      <li><b>Right mouse button:</b> the obvious action: doors open, people get talked to.</li>
      <li><b>Talk:</b> pick a line. Codes, passwords and insults are lines too: find the clue first!</li></ul>
      <table><tr><td>G O C P L T U S Y</td><td>the verbs from the keyboard</td></tr>
      <tr><td>Click / . / ESC</td><td>skip a line of text</td></tr><tr><td>SPACE</td><td>pause</td></tr>
      <tr><td>F5 or MENU</td><td>save and load (4 slots), music, dev mode, quit</td></tr></table>''', 7))
    who = ''.join(f'<div class="who"><img src="{SPR[k]}"><div><b>{n}</b><br>{t}</div></div>' for k, n, t in (
        ('pilot', 'You, the pilot', 'Nephew of Uncle Edmund. Good with a shovel, better with a rubber chicken.'),
        ('edmund', 'Uncle Edmund', 'Inventor, explorer, collector of legends, and builder of the STARRAVEN.'),
        ('vex', 'Commander Vex', 'A raven on his helmet, a cannon on his flagship, and a secret in his past.'),
        ('roger', 'Roger', 'Janitor, 2nd class. Has saved the galaxy a few times and got a mop for it.'),
        ('pip', 'Pip', 'A little Stronkie with glowing ears. Knows the old mines. Loves his kite.'),
        ('zooma', 'Elder Zooma', 'The wise old Stronkie of the village. Knows about the Sky Temple.'),
        ('bix', 'Bix', 'Young inventor with goggles. Can make anything fly, given a big enough sail.')))
    P.append(mpage(f'<h1>Who is who</h1>{who}<p style="font-size:7.6pt;color:#6a5d86">And NOVA, the calm voice of '
                   f'the STARRAVEN, who has no body but always an opinion.</p>', 8))
    for n in range(1, 8):
        P.append(chapter_page(n, 8 + n))
    P.append(mpage(f'''<h1>Star fragments and choices</h1>
      <p>Sixteen tiny <b>star fragments</b> are hidden in the whole game: three on disk 1, two on every disk after it,
      three on disk 7. Look closely at tables, beds, barrels, crates and statues. Collect all sixteen and lay them on
      Uncle Edmund's desk at the very end for the <b>true ending</b>.</p>
      <h2>Choices that matter</h2>
      <p>Some things you do on disks 3 and 4 come back on disk 7. You can finish either way.</p>
      <ul><li>Was Roger the janitor fed, and did he get a napkin?</li><li>Did you beat Stronkie's Astro Chicken high score?</li>
      <li>Did you untie the crewman in the red shirt?</li><li>Did you win LeChuckle's rematch?</li>
      <li>Did you find the wooden monkey? Did you try on the nose glasses?</li></ul>
      {pic('c4_jungle', 'Something is hiding in the bushes...')}''', 16))
    P.append(mpage('''<h1>Hints</h1>
      <ul><li><b>Look at everything.</b> Descriptions hold the clues: codes, passwords, insults.</li>
      <li><b>Talk twice.</b> People say new things after something happened.</li>
      <li><b>Combine.</b> Many puzzles are <i>Use X with Y</i>: a crowbar with a crate, a chicken with a cable.</li>
      <li><b>Stuck?</b> Go back to a room you have not visited for a while. Something may have changed.</li>
      <li><b>The Stronkies</b> only chirp until you have the right thing to listen with.</li>
      <li><b>Insult fights:</b> the right answer is only on the list once somebody has taught it to you.</li>
      <li><b>The maze:</b> ask your little friend. He can smell crystals.</li></ul>
      <h2>Still stuck?</h2><p>A complete walkthrough and a map of every room are free downloads on the itch.io page.</p>
      <div class="lines"><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="cap">Your own notes.</div>''', 17))
    P.append(mpage(f'''<h1>Credits</h1>
      <table><tr><td>Game, story, pictures, music</td><td>Mark Stronks</td></tr>
      <tr><td>The original</td><td>The World of Stronkie (C64 and Amiga)</td></tr>
      <tr><td>Engine</td><td>The World of Stronkie II engine</td></tr>
      <tr><td>Version</td><td>{VERSION}: seven disks</td></tr></table>
      <p>Thank you to everybody who tested, commented and played the text adventure first.</p>
      <div style="text-align:center;margin-top:8mm"><img src="{U['logo']}" style="width:46mm"></div>
      <p style="text-align:center;font-size:7pt;color:#8a7aa8;margin-top:2mm">Created By Mark Stronks, Stronkie Soft
      &copy; 2026 &middot; stronkie.itch.io</p>''', 18))
    html = f'<html><head><style>{MAN_CSS}</style></head><body>{"".join(P)}</body></html>'
    out = os.path.join(OUTD, f'{PRE}_Manual.pdf')
    pdf(html, out, '148mm', '210mm')
    return out


def labels():
    def lab(n, demo=False):
        if demo:
            d, nm, pic_ = 'FREE DEMO', 'Part 1: The Grounds', U['scene']
        else:
            nm = CHAPTERS[n - 1][1]
            d, pic_ = f'DISK {n} OF 7', SH[ROOMPIC[n]]
        ch = '' if demo else f'CHAPTER {NUM[n].upper()}: '
        return f'''<div class="lab"><div class="fold">WORLD OF STRONKIE REMAKE &middot; {d}</div>
          <img class="t" src="{U['title']}"><img class="sc" src="{pic_}">
          <div class="n">{ch}{nm.upper()}</div>
          <div class="d{' demo' if demo else ''}">{d} &middot; {VERSION}</div>
          <div class="c">Amiga 500 &middot; 1 MB &middot; Kickstart 3.1 &middot; Stronkie Soft &copy; 2026</div></div>'''
    html = f'''<html><head><style>{LAB_CSS}
      .grid {{ grid-template-columns: repeat(3, 58mm); gap: 5mm 6mm; }}
      .lab {{ width: 58mm; height: 58mm; }} .fold {{ height: 10mm; font-size: 5.6pt; }}
      .lab .t {{ width: 53mm; margin-top: 1.5mm; }} .lab .sc {{ width: 40mm; }}
      .lab .n {{ font-size: 5.6pt; }} .lab .d {{ font-size: 6.6pt; bottom: 5mm; }} .lab .c {{ font-size: 4.4pt; bottom: 1mm; }}
      </style></head><body><div class="sheet">
      <h1>{TITLE}: disk labels</h1>
      <div class="note">Print at 100% ("actual size") on sticker paper, or on plain paper and glue.
      Cut along the dashed lines. Stick the label on the disk and fold the top strip over to the back.</div>
      <div class="grid">{''.join(lab(n) for n in range(1, 8))}{lab(0, True)}</div></div></body></html>'''
    out = os.path.join(OUTD, f'{PRE}_DiskLabels.pdf')
    pdf(html, out, '210mm', '297mm')
    return out


W, H, D, TUCK, GLUE = 140, 180, 40, 15, 12   # mm


def panels():
    front = f'''<div class="face night" style="width:{W}mm;height:{H}mm">
      <div style="background:#ffd560;color:#2a1450;text-align:center;font-weight:800;letter-spacing:.2em;font-size:6.5pt;padding:1.6mm">STRONKIE SOFT PRESENTS</div>
      <img src="{U['title']}" style="width:132mm;display:block;margin:3mm auto 0">
      <img src="{U['scene']}" style="width:132mm;display:block;margin:4mm auto 0;border:.6mm solid #5a6ad0">
      <div style="text-align:center;margin-top:3mm;font-size:11pt;font-weight:800;color:#fff">THE CLASSIC, NOW POINT &amp; CLICK</div>
      <div style="text-align:center;font-size:8pt;color:#ff8cc0;margin-top:.6mm">The complete adventure &middot; seven chapters on seven disks</div>
      <img src="{SH.get('c3_deck_room', SH['r_deck'])}" style="width:96mm;display:block;margin:4mm auto 0;border:1.2mm solid #fff;
        transform:rotate(-2deg);box-shadow:1.5mm 1.5mm 0 #000">
      <div style="text-align:center;font-size:7pt;color:#e8e4ff;margin-top:2.5mm;font-style:italic">
        "You fight like a dairy farmer!"</div>
      <div style="position:absolute;right:4mm;top:112mm;width:27mm;height:27mm;border-radius:50%;background:#ff4f8b;color:#fff;
        transform:rotate(12deg);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;
        font-size:6.6pt;line-height:1.15;box-shadow:0 0 0 .7mm #fff">7 DISKS!<br>SPEECH!<br>NO TYPING!</div>
      <div style="position:absolute;bottom:10.5mm;left:0;right:0;background:#d8202f;color:#fff;text-align:center;font-weight:800;
        font-size:6.4pt;line-height:1.25;padding:1.4mm 2mm">FOR THE AMIGA 500 WITH <span style="color:#ffd560">1 MB</span> (512K CHIP + 512K TRAPDOOR)<br>
        KICKSTART / WORKBENCH 3.1 &middot; NO ACCELERATOR NEEDED</div>
      <div style="position:absolute;bottom:0;left:0;right:0;background:#7a3ad0;color:#fff;text-align:center;font-weight:800;
        font-size:11pt;letter-spacing:.15em;padding:2.4mm">AMIGA 500 &middot; 1 MB &middot; 7 DISKS</div></div>'''
    shots = ''.join(f'<img src="{SH[k]}">' for k in ['c2_robot_room', 'c4_bix_room', 'c5_statues_room', 'c6_vex_room',
                                                     'c7_tron_room', 'c1_library_room'] if k in SH)
    back = f'''<div class="face night" style="width:{W}mm;height:{H}mm;padding:4mm 5mm">
      <div style="background:#ffd560;color:#2a1450;font-weight:800;font-size:8.5pt;padding:1.6mm 2.5mm;margin:-4mm -5mm 3mm">
        "COME TO RAVENMOOR AT ONCE. I HAVE FOUND IT."</div>
      <p style="font-size:7pt;line-height:1.35">A letter from your uncle Edmund brings you to Ravenmoor Manor on a stormy
      night. Behind its doors: a hidden chamber, a secret hangar and the STARRAVEN, a ship built to find the lost World
      of Stronkie. Across derelict stations, pirate ships, purple jungles and crystal mountains to the Star Heart,
      with an old enemy close behind. The classic adventure, rebuilt as point and click.</p>
      <div class="bshots">{shots}</div>
      <ul style="font-size:6.8pt;line-height:1.4;margin:2.5mm 0 0 3.5mm">
      <li>Point and click with nine verbs. No more typing</li>
      <li>Seven chapters on seven disks, the original pictures, music and speech</li>
      <li>Your story carries over, with an item check list from disk to disk</li>
      <li>16 hidden star fragments, choices that matter, a true ending</li>
      <li>You can never die and never get stuck</li></ul>
      <div style="display:flex;gap:3mm;align-items:stretch;margin-top:2.5mm">
      <div style="flex:1;border:.6mm solid #d8202f;background:#2a0a14;padding:1.6mm 2.2mm;font-size:6.2pt;line-height:1.4">
        <div style="color:#ff5060;font-weight:800;font-size:7.4pt;margin-bottom:.6mm">MINIMUM SYSTEM REQUIREMENTS</div>
        &bull; Amiga 500 (68000) with <b style="color:#ffd560">1 MB</b> memory<br>
        &bull; 512 KB chip memory + 512 KB trapdoor expansion<br>
        &bull; Kickstart / Workbench 3.1 &middot; mouse<br>
        <b style="color:#fff">No accelerator needed.</b> Try the free demo first.</div>
      <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:center;width:26mm">
        <img src="{U['logo']}" style="width:24mm">
        <div style="font-size:5pt;color:#b8b0d8;text-align:center">Created By Mark Stronks<br>Stronkie Soft &copy; 2026</div></div>
      </div></div>'''
    spec = f'''<div class="face night" style="width:{D}mm;height:{H}mm;padding:5mm 2.5mm;font-size:6pt;line-height:1.45">
      <img src="{U['logo']}" style="width:32mm;display:block;margin:0 auto 4mm">
      <div style="background:#d8202f;color:#fff;font-weight:800;font-size:6.6pt;padding:1.2mm;text-align:center;margin-bottom:2mm">AMIGA 500<br>1 MB</div>
      <div class="gold" style="font-weight:800;font-size:7pt;margin-bottom:1.5mm">MINIMUM SYSTEM</div>
      Amiga 500<br>68000, 7 MHz<br>512 KB chip<br>512 KB trapdoor<br>Kickstart 3.1<br>Mouse
      <div style="color:#ff5060;font-weight:800;margin-top:2mm">No accelerator<br>needed</div>
      <div class="gold" style="font-weight:800;font-size:7pt;margin:3mm 0 1.5mm">IN THE BOX</div>
      7 disks<br>Instruction manual<br>Disk labels<br>Map
      <div class="gold" style="font-weight:800;font-size:7pt;margin:3mm 0 1.5mm">ALSO RUNS</div>
      From hard drive, CF card or WHDLoad
      <div style="position:absolute;bottom:4mm;left:0;right:0;text-align:center;font-weight:800;color:#fff;font-size:5.4pt">{VERSION}</div></div>'''
    side = spec
    top = f'''<div class="face night" style="width:{W}mm;height:{D}mm;display:flex;align-items:center;justify-content:space-around">
      <img src="{U['title']}" style="width:96mm"><img src="{U['logo']}" style="width:26mm"></div>'''
    bottom = f'''<div class="face night" style="width:{W}mm;height:{D}mm;display:flex;align-items:center;justify-content:center;
      font-size:7pt;color:#b8b0d8;text-align:center">7 disks &middot; Amiga 500 &middot; 1 MB (512K chip + 512K trapdoor) &middot; Kickstart / Workbench 3.1<br>
      Created By Mark Stronks &middot; Stronkie Soft &copy; 2026</div>'''
    sidebar = f'''<div class="face night" style="width:{D}mm;height:{H}mm">
      <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-90deg);white-space:nowrap;
        text-align:center"><div style="font-size:14pt;font-weight:800;color:#5ad8ec">WORLD OF STRONKIE <span class="gold">remake</span></div>
        <div style="font-size:6.5pt;color:#ff8cc0">7 disks &middot; Amiga 500 &middot; Stronkie Soft</div></div></div>'''
    return front, back, sidebar, spec, top, bottom


def box_pdfs():
    a3 = os.path.join(OUTD, f'{PRE}_Box_A3.pdf')
    pdf(box_net(420, 297, 'The box (A3, full size)', 'For A3 card.'), a3, '420mm', '297mm')
    a4 = os.path.join(OUTD, f'{PRE}_Box_A4.pdf')
    pdf(box_net(297, 210, 'The box (A4, smaller)', 'A smaller box that fits on A4 card.'), a4, '297mm', '210mm')
    return a3, a4


BOX_CSS = CSS + '''
.face { position: relative; overflow: hidden; background: #0b0a26; color: #e8e4ff; }
.bshots { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.6mm; margin-top: 2.5mm; }
.bshots img { width: 100%; border: .3mm solid #5a6ad0; }
.net { position: absolute; }
.cut { position: absolute; border: .25mm solid #222; }
.flap { position: absolute; background: #0b0a26; }
.lbl { position: absolute; font-size: 6pt; color: #777; }
'''


def box_net(paper_w, paper_h, title, note, margin=8):
    """the fold-up box as one die-cut net: solid black = cut, white dashes = fold"""
    front, back, side, spec, top, bottom = panels()
    DF = D - 6                                   # dust flap height
    tw = GLUE + D + W + D + W
    th = TUCK + D + H + D + TUCK
    sc = min(1.0, (paper_w - 2 * margin) / tw, (paper_h - 2 * margin) / th)
    ox = (paper_w - tw * sc) / 2
    oy = (paper_h - th * sc) / 2
    xs1, xf, xs2, xb, xe = GLUE, GLUE + D, GLUE + D + W, GLUE + 2 * D + W, tw
    yt, yb = TUCK + D, TUCK + D + H
    out = [(xs1, yt), (xs1, yt + 4), (0, yt + 10), (0, yb - 10), (xs1, yb - 4), (xs1, yb),
           (xs1 + 3, yb + DF), (xf - 3, yb + DF), (xf, yb),
           (xs2, yb), (xs2 + 3, yb + DF), (xb - 3, yb + DF), (xb, yb),
           (xb, yb + D), (xb + 8, yb + D + TUCK), (xe - 8, yb + D + TUCK), (xe, yb + D),
           (xe, yt), (xb, yt), (xb - 3, yt - DF), (xs2 + 3, yt - DF), (xs2, yt),
           (xs2, TUCK), (xs2 - 8, 0), (xf + 8, 0), (xf, TUCK), (xf, yt),
           (xf - 3, yt - DF), (xs1 + 3, yt - DF)]
    path = 'M ' + ' L '.join(f'{x} {y}' for x, y in out) + ' Z'
    folds = [(xs1, yt, xs1, yb), (xf, yt, xf, yb), (xs2, yt, xs2, yb), (xb, yt, xb, yb),
             (xf, yt, xs2, yt), (xf, TUCK, xs2, TUCK),
             (xb, yb, xe, yb), (xb, yb + D, xe, yb + D),
             (xs1, yt, xf, yt), (xs1, yb, xf, yb), (xs2, yt, xb, yt), (xs2, yb, xb, yb)]
    fl = ''.join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#fff" stroke-width="0.35" '
                 f'stroke-dasharray="2.2 1.6"/>' for a, b, c, d in folds)
    under = (f'<svg style="position:absolute;left:0;top:0" width="{tw}mm" height="{th}mm" viewBox="0 0 {tw} {th}">'
             f'<path d="{path}" fill="#0b0a26"/></svg>')
    over = (f'<svg style="position:absolute;left:0;top:0" width="{tw}mm" height="{th}mm" viewBox="0 0 {tw} {th}">'
            f'{fl}<path d="{path}" fill="none" stroke="#000" stroke-width="0.4"/></svg>')

    def put(x, y, html):
        return f'<div style="position:absolute;left:{x}mm;top:{y}mm">{html}</div>'

    def lab(x, y, w, h, text, rot=0):
        return (f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm;display:flex;'
                f'align-items:center;justify-content:center;color:#8a86b8;font-size:5.5pt;font-weight:700;'
                f'letter-spacing:.1em;transform:rotate({rot}deg)">{text}</div>')
    parts = [under, put(xs1, yt, side), put(xf, yt, front), put(xs2, yt, spec), put(xb, yt, back),
             put(xf, TUCK, top), put(xb, yb, bottom),
             lab(xf, 0, W, TUCK, 'TUCK IN'), lab(xb, yb + D, W, TUCK, 'TUCK IN'),
             lab(-(H - 8) / 2 + GLUE / 2, yt + H / 2 - GLUE / 2, H - 8, GLUE, 'GLUE', -90)]
    for x in (xs1, xs2):
        parts.append(lab(x, yt - DF, D, DF, 'FLAP'))
        parts.append(lab(x, yb, D, DF, 'FLAP'))
    full = sc > 0.999
    size = f'{W * sc:.0f} x {H * sc:.0f} x {D * sc:.0f} mm'
    howto = f'''<div style="position:absolute;left:{xb + 2}mm;top:2mm;width:{W - 4}mm;font-size:6.6pt;line-height:1.4;color:#333">
      <b style="font-size:9pt;color:#3b1f73">{title}</b><br>{note}<br>
      <b>1.</b> Print at <b>100% / actual size</b> (not "fit to page"), on card of 200-300 g/m&sup2;.<br>
      <b>2.</b> Cut along the solid black outline.<br>
      <b>3.</b> Score and fold all white dashed lines, print side out.<br>
      <b>4.</b> Glue the GLUE tab inside the right edge of the back panel.<br>
      <b>5.</b> Fold in the flaps, close the lids and tuck them in.<br>
      Finished box: <b>{size}</b>{"" if full else f" ({sc * 100:.0f}% of the full {W} x {H} x {D} mm box)"}.</div>'''
    parts.append(howto)
    parts.append(over)
    net = (f'<div style="position:absolute;left:{ox}mm;top:{oy}mm;width:{tw}mm;height:{th}mm;'
           f'transform:scale({sc});transform-origin:0 0">{"".join(parts)}</div>')
    return (f'<html><head><style>{BOX_CSS} @page {{ size: {paper_w}mm {paper_h}mm; margin: 0; }} '
            f'html,body {{ width:{paper_w}mm; height:{paper_h}mm; overflow:hidden; background:#fff; }}</style></head>'
            f'<body><div style="position:relative;width:{paper_w}mm;height:{paper_h}mm">{net}</div></body></html>')


def faces_png():
    """the three faces of the box as pictures (for the 3D view), 6 px a mm"""
    front, back, side, spec, top, bottom = panels()
    k = 6
    res = {}
    for name, html, w, h in (('front', front, W, H), ('side', spec, D, H), ('top', top, W, D)):
        p = os.path.join(OUTD, f'_face_{name}.png')
        page = f'<html><head><style>{BOX_CSS} body{{zoom:{k * 25.4 / 96}}}</style></head><body>{html}</body></html>'
        png(page, p, int(w * k * 25.4 / 25.4 * 96 / 96 * 3.7795 / 3.7795), int(h * k))
        res[name] = Image.open(p).convert('RGB')
        os.remove(p)
    return res


def box_3d(faces):
    """a big box standing at an angle, with a shadow"""
    f, sd, tp = faces['front'], faces['side'], faces['top']
    Wp, Hp = f.size
    Dp = sd.size[0]
    out = Image.new('RGBA', (1600, 1500), (0, 0, 0, 0))

    def warp(img, quad):
        # quad: target corners tl, tr, br, bl -> perspective transform
        w, h = img.size
        src = [(0, 0), (w, 0), (w, h), (0, h)]
        A, B = [], []
        for (x, y), (u, v) in zip(quad, src):
            A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
            A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
        coef = np.linalg.solve(np.array(A, float), np.array(B, float))
        layer = img.convert('RGBA').transform(out.size, Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)
        mask = Image.new('L', out.size, 0)
        ImageDraw.Draw(mask).polygon(quad, fill=255)
        out.paste(layer, (0, 0), mask)
    sc = 1150 / Hp
    fw, fh, dw = Wp * sc, Hp * sc, Dp * sc
    x0, y0 = 330, 230
    tl, bl = (x0, y0), (x0, y0 + fh)
    tr, br = (x0 + fw * 0.93, y0 + fh * 0.04), (x0 + fw * 0.93, y0 + fh * 0.97)
    # the side on the left, going back
    stl, sbl = (x0 - dw * 0.62, y0 - dw * 0.30), (x0 - dw * 0.62, y0 + fh - dw * 0.18)
    # shadow
    sh = Image.new('L', out.size, 0)
    ImageDraw.Draw(sh).polygon([bl, br, (br[0] + 60, br[1] + 50), (sbl[0] + 80, sbl[1] + 70), sbl], fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    out.paste((10, 8, 30, 255), (0, 0), sh)
    side_dark = Image.blend(sd.convert('RGB'), Image.new('RGB', sd.size, (0, 0, 0)), 0.35)
    warp(side_dark, [stl, tl, bl, sbl])
    ttl, ttr = (stl[0] + fw * 0.93 * 0.98, stl[1] + fh * 0.04 - 4), tr
    top_l = Image.blend(tp.convert('RGB'), Image.new('RGB', tp.size, (255, 255, 255)), 0.12)
    warp(top_l, [stl, (stl[0] + (tr[0] - tl[0]), stl[1] + (tr[1] - tl[1])), tr, tl])
    warp(f, [tl, tr, br, bl])
    # a soft highlight on the front edge
    d = ImageDraw.Draw(out)
    d.line([tl, bl], fill=(255, 255, 255, 90), width=3)
    bbox = out.getbbox()
    out = out.crop((bbox[0] - 40, bbox[1] - 40, bbox[2] + 40, bbox[3] + 40))
    bg = Image.new('RGB', out.size, (24, 18, 52))
    g = Image.linear_gradient('L').resize(out.size)
    bg = Image.composite(Image.new('RGB', out.size, (60, 30, 100)), bg, g)
    bg.paste(out, (0, 0), out)
    p = os.path.join(OUTD, f'{PRE}_Box_3D.png')
    bg.save(p)
    return p


if __name__ == '__main__':
    print(manual())
    print(labels())
    print(*box_pdfs())
    print(box_3d(faces_png()))
