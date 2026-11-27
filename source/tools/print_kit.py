#!/usr/bin/env python3
"""The print kit of The World of Stronkie II: the manual (an A5 booklet),
the disk labels (A4), the fold-up box (A3 and A4) and a 3D picture of the box.

    python3 print_kit.py SHOTS_DIR OUT_DIR

SHOTS_DIR holds the emulator screenshots (358 x 285, as tools/vtest.py makes them)."""
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

SHOTS, OUTD = sys.argv[1], sys.argv[2]
os.makedirs(OUTD, exist_ok=True)
VERSION = 'V0.1.4 - V0.5.4'
TITLE = 'The World of Stronkie II'
SUB = 'A Love on Stronkie'


# ------------------------------------------------------------------ pictures
def uri(im, fmt='PNG'):
    b = io.BytesIO()
    im.save(b, fmt)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()


def shot(name, panel=True):
    im = Image.open(os.path.join(SHOTS, name + '.png')).convert('RGB')
    return im.crop((31, 18, 351, 267 if panel else 186))


def loading_parts():
    a, full, soft = loading.make()
    ca, cf, pal = loading.quantize32(a, full, soft)
    img = Image.fromarray((pal[ca] * 255).astype(np.uint8))
    half = img.copy()
    hf = Image.fromarray((pal[cf] * 255).astype(np.uint8))
    x0, y0, x1, y1 = loading.BAR
    half.paste(hf.crop((0, y0, 200, y1)), (0, y0))
    title = img.crop((14, 8, 306, 46))
    x0, y0, x1, y1 = loading.SCENE
    scene = img.crop((x0, y0, x1, y1))
    return half, title, scene


def big(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def sprite(kind):
    pal = np.array([[int(c[i], 16) * 17 for i in (1, 2, 3)] for c in people.FIXED], np.uint8)
    if kind == 'pilot':
        s = loading.big_sprite(people.human, people.PILOT, 'front', None)
    elif kind == 'lyra':
        s = loading.big_sprite(people.human, people.LYRA, 'front', None)
    elif kind == 'pip':
        s = loading.big_sprite(people.stronkie, 'front')
    elif kind == 'bix':
        s = loading.big_sprite(people.stronkie, 'front', extra=people.bix_extra)
    elif kind == 'zooma':
        s = loading.big_sprite(people.stronkie, 'front', fur=people.SILVER, light=people.WHITE,
                               extra=people.zooma_extra, h=24)
    elif kind in ('edmund', 'vex', 'queen', 'roger'):
        s = loading.big_sprite(people.human, getattr(people, kind.upper()), 'front', None)
    elif kind == 'quill':
        s = loading.big_sprite(people.stronkie, 'front', fur=people.BLUE, light=people.LBLUE,
                               extra=people.quill_extra, h=24)
    elif kind == 'gobbo':
        s = loading.big_sprite(people.stronkie, 'front', extra=people.gobbo_extra)
    else:
        s = loading.big_sprite(people.rabbit)
    ys, xs = np.nonzero(s >= 0)
    s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    rgba = np.zeros(s.shape + (4,), np.uint8)
    m = s >= 0
    rgba[m, :3] = pal[s[m] - 16]
    rgba[m, 3] = 255
    return Image.fromarray(rgba)


def logo():
    return Image.open(os.path.join(SRC, 'images', 'stronkiesoft_logo.png')).convert('RGBA')


LOADING, TITLE_IMG, SCENE = loading_parts()
LOGO = logo()
U = {
    'title': uri(big(TITLE_IMG, 4)), 'scene': uri(big(SCENE, 4)), 'loading': uri(big(LOADING, 2)),
    'logo': uri(LOGO),
}
SH = {}
for n in ['x_title', 'x_card', 'x_intro', 'm_meadow', 'm_hatch', 'x_look', 'x_well', 's_bucket', 'w_chicken',
          'g_dialog', 'g_dialog2', 'o_gorge', 'c_cave', 'c_starwater', 'g_bloom', 's_ribbon', 'f_dance',
          'f_shard', 'x_guru', 'x_monkey', 'x_book', 'x_sword', 'x_deep', 'd_end'] + \
        sorted(f[:-4] for f in os.listdir(SHOTS) if f[:3] in ('c2_', 'c3_', 'c4_', 'c5_')):
    if os.path.exists(os.path.join(SHOTS, n + '.png')):
        SH[n] = uri(big(shot(n), 2))
        SH[n + '_room'] = uri(big(shot(n, False), 2))
SPR = {k: uri(big(sprite(k), 3)) for k in ['pilot', 'lyra', 'pip', 'bix', 'zooma', 'gobbo', 'rabbit',
                                            'edmund', 'vex', 'quill', 'queen', 'roger']}


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


def mpage(body, num=None, night=False, head=True):
    h = f'<div class="head"><span>{TITLE}</span><span>Instruction manual</span></div>' if head else ''
    f = f'<div class="foot">- {num} -</div>' if num else ''
    return f'<div class="page{" night" if night else ""}">{h}{body}{f}</div>'


CHAPTERS = [
    (1, 'The Festival of Two Moons', 'V0.1.4'),
    (2, 'The Star Shard', 'V0.2.4'),
    (3, 'The Red Door', 'V0.3.4'),
    (4, 'The Other World', 'V0.4.4'),
    (5, 'Two Moons, One Heart', 'V0.5.4'),
]
NUM = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}


def chapter_page(n, story, rooms, people_line, shots, num):
    name = CHAPTERS[n - 1][1]
    cells = ''.join(f'<div>{s(k)}<div class="cap">{c}</div></div>' for k, c in shots)
    return mpage(f'''<div class="chap">CHAPTER {NUM[n].upper()} &middot; DISK {n}</div>
      <h1>{name}</h1>
      <p>{story}</p>
      <p style="font-size:7.6pt;color:#6a5d86"><b>Places:</b> {rooms}<br><b>Who you meet:</b> {people_line}</p>
      <div class="two">{cells}</div>''', num)


def manual():
    P = []
    # 1 cover
    P.append(f'''<div class="page night" style="padding:0">
      <div style="background:#ffd560;color:#2a1450;text-align:center;font-weight:800;letter-spacing:.2em;
        font-size:8pt;padding:2.2mm">STRONKIE SOFT PRESENTS</div>
      <img src="{U['title']}" style="width:132mm;display:block;margin:6mm auto 0">
      <img src="{U['scene']}" style="width:132mm;display:block;margin:5mm auto;border:.8mm solid #5a6ad0">
      <div style="text-align:center;font-size:21pt;font-weight:800;color:#fff;margin-top:4mm">INSTRUCTION MANUAL</div>
      <div style="text-align:center;font-size:10pt;color:#ff8cc0;margin-top:1mm">The complete adventure in five chapters</div>
      <div style="text-align:center;font-size:7.4pt;color:#b8b0d8;margin-top:1.5mm;line-height:1.5">
        One: The Festival of Two Moons &middot; Two: The Star Shard &middot; Three: The Red Door<br>
        Four: The Other World &middot; Five: Two Moons, One Heart</div>
      <div style="margin:4mm 10mm 0;background:#d8202f;color:#fff;text-align:center;font-weight:800;font-size:8pt;padding:2mm;line-height:1.3">
        FOR THE AMIGA 500 WITH 1 MB (512K CHIP + 512K TRAPDOOR)<br>KICKSTART / WORKBENCH 3.1 &middot; NO ACCELERATOR NEEDED</div>
      <div style="position:absolute;bottom:20mm;left:0;right:0;text-align:center">
        <img src="{U['logo']}" style="width:40mm"></div>
      <div style="position:absolute;bottom:0;left:0;right:0;background:#7a3ad0;color:#fff;text-align:center;
        font-weight:800;font-size:12pt;letter-spacing:.15em;padding:3mm">AMIGA 500 &middot; 1 MB &middot; 5 DISKS</div></div>''')
    # 2 welcome + contents
    P.append(mpage(f'''<h1>Welcome back to Stronkie</h1>
      <p>Thank you for buying <b>{TITLE}: {SUB}</b>! A year ago you crossed the galaxy, beat the pirate captain
      Vex and brought the Star Heart home. This time the danger is much worse: you have fallen in love.</p>
      <p>This is a <b>point-and-click adventure</b> in the style of the great LucasArts games, told in
      <b>five chapters on five disks</b>. There is no typing: you point at things, pick a verb and click.
      You can never die, and you can never get stuck. Your story travels with you from one chapter to the
      next: what you carry, and what you choose.</p>
      <h2>In this manual</h2>
      <table><tr><td>A letter from Pip</td><td>3</td></tr><tr><td>What you need</td><td>4</td></tr>
      <tr><td>The five disks, playing from the hard drive</td><td>5</td></tr>
      <tr><td>Your story carries over</td><td>6</td></tr><tr><td>How to play</td><td>7</td></tr>
      <tr><td>The verbs, keys and the menu</td><td>8</td></tr><tr><td>The people of Stronkie</td><td>9</td></tr>
      <tr><td>New faces</td><td>11</td></tr><tr><td>The five chapters</td><td>12</td></tr>
      <tr><td>Choices that matter</td><td>17</td></tr><tr><td>Hints for new adventurers</td><td>18</td></tr>
      <tr><td>The great easter egg hunt</td><td>20</td></tr><tr><td>Funny facts</td><td>22</td></tr>
      <tr><td>The dev log</td><td>23</td></tr><tr><td>Credits</td><td>24</td></tr></table>
      {s('x_title')}<div class="cap">The title screen. Press a key and the adventure begins.</div>''', 2))
    # 3 the letter
    P.append(mpage(f'''<h1>A letter from Pip</h1>
      <div class="letter">Dear Pilot,<br><br>
      Remember me? Small, blue, very long ears, saved the galaxy with you? (Mostly you. I did the cheering.)<br><br>
      Tonight is the <b>Festival of Two Moons</b> on the World of Stronkie. Once a year both moons rise full at the
      same time, and everybody dances the Moon Dance in the village square. There is music. There is cake.
      There is MORE cake.<br><br>
      Please fly me home in the STARRAVEN. And bring your lucky coin, you never know.<br><br>
      Your best friend,<br><b>Pip</b><br><br>
      P.S. There is a girl called Lyra who looks after the Moonflower Garden. No reason. Just saying.</div>
      <p>And so the STARRAVEN lands in a meadow full of flowers that turn to watch you walk past.
      The Great Moonflower will not bloom, somewhere a white rabbit is late for something, and a girl with a
      glowing necklace is about to change your life. It will take you up a mountain, under the village, to
      another world and onto the flagship of an old enemy. Welcome home, Pilot.</p>
      {s('x_intro', True)}<div class="cap">"We are home! The World of Stronkie! Smell that air!"</div>''', 3))
    # 4 what you need
    P.append(mpage(f'''<h1>What you need</h1>
      <div style="border:.8mm solid #d8202f;background:#fde8ea;padding:2.5mm 3mm;margin-bottom:3mm;border-radius:1mm">
        <b style="color:#b0101c;font-size:10pt">An Amiga 500 with 1 MB is all you need.</b><br>
        No accelerator and no fast memory: the game runs on a plain 68000 with 512 KB chip memory and the
        512 KB trapdoor expansion. Not sure? Try the free demo first: if the demo runs, all five chapters run too.</div>
      <h2>Minimum system requirements</h2>
      <ul><li>An <b>Amiga 500</b> (68000, 7 MHz) with <b>Kickstart and Workbench 3.1</b></li>
      <li><b>1 MB memory</b>: 512 KB chip memory + the <b>512 KB trapdoor</b> expansion</li>
      <li>Also runs with an accelerator such as the ACA500 / ACA500plus, and on bigger Amigas</li><li>A mouse in port 1, and speakers for the music and the speech</li>
      <li>One floppy drive is enough. A hard drive or CF card makes it nicer (see page 5).</li></ul>
      <div class="box">The game checks the memory when it starts. If there is not enough, it says how much is
      free and goes back to the Workbench, without harm. Booting from the game disk leaves the most memory free.</div>
      <h2>Loading from the floppy</h2>
      <p>Put the disk of the chapter you want to play in DF0: and switch on (or reset) the Amiga. The loading screen
      appears and its bar fills up while the game loads. Hold on to the chicken: from a floppy this takes a little while.</p>
      <img class="shot" src="{U['loading']}" style="width:74mm;margin:1mm auto 0"><div class="cap" style="text-align:center">The loading screen: a sequel, and you can tell.</div>''', 4))
    # 5 the five disks + hard drive
    rows = ''.join(f'<tr><td><b>Disk {n}</b></td><td>Chapter {NUM[n]}: {nm}<br><span style="font-size:7pt">disk name: Stronkie World II Ch {n} {v}</span></td><td>{"WOS2" if n == 1 else f"WOS2C{n}"}</td><td>{v}</td></tr>'
                   for n, nm, v in CHAPTERS)
    P.append(mpage(f'''<h1>The five disks</h1>
      <p>Every chapter is a complete disk of its own, with its own rooms, music and saved games. Play them in order:
      each chapter starts where the last one ended.</p>
      <table><tr><th>Disk</th><th>Chapter</th><th>Program</th><th>Version</th></tr>{rows}</table>
      <p style="font-size:7.6pt;color:#6a5d86">Because every chapter is its own disk, a chapter can be updated later
      without touching the others. The version is printed on each disk label.</p>
      <h2>Playing from the hard drive or CF card</h2>
      <p>Make <b>one</b> drawer, for example <b>Games:WorldOfStronkieII</b>, and copy the files of <b>all</b> the
      disks into it: the program, its .DAT, .GFX and .STR files and its icon (for chapter three that is
      <b>WOS2C3</b>, <b>WOS2C3.DAT</b>, <b>WOS2C3.GFX</b>, <b>WOS2C3.STR</b> and <b>WOS2C3.info</b>). Double-click the icon of the
      chapter you want to play.</p>
      <div class="box"><b>Keep all chapters in the same drawer.</b> That is where each chapter leaves your story for the
      next one, and where the saved games live. Then the next chapter finds your story by itself, without asking.</div>
      <h2>WHDLoad</h2>
      <p>Every chapter also comes as a WHDLoad version. All five unpack into the same drawer,
      <b>WorldOfStronkieII</b>, so they share your story too. Start a chapter with its own icon.</p>''', 5))
    # 6 story carries over
    P.append(mpage(f'''<h1>Your story carries over</h1>
      <p>Nothing on Stronkie starts fresh. When you finish a chapter, the game writes your story into a small file:
      <b>the things you carry</b> and <b>the choices you made</b>. The next chapter reads it, and the people you meet
      remember. The file is called <b>WOS2.ST2</b> after chapter one, <b>WOS2.ST3</b> after chapter two, and so on.</p>
      <h2>From the hard drive, CF card or WHDLoad</h2>
      <p>Nothing to do: with all chapters in one drawer, the next chapter finds the story file and goes straight on.</p>
      <h2>From floppies</h2>
      <p>When you finish a chapter on floppy, the story is written to <b>that chapter's disk</b>, so leave it
      write-enabled. When you start the next chapter, it asks:</p>
      <ul><li><i>"Your story from Chapter One is not in this drawer. Put the Chapter One disk in the drive."</i>
      Swap disks and click <b>"The Chapter One disk is in. Read my story."</b></li>
      <li><i>"Your story is read! Now put the Chapter Two disk back in."</i> Swap back, click, and off you go.</li></ul>
      <h2>No story? Play the standard story</h2>
      <p>Lost the disk, or want to jump straight into a later chapter? Choose <b>the standard story</b>: the chapter starts
      with the things and choices most players end up with. You can still finish it, and you can never get stuck.</p>
      <div class="box">The story is written when a chapter ends. Wait for the card <i>"Your story is saved."</i>
      If the disk is write-protected, the game tells you, so you can fix it and try again, or go on without it.</div>''', 6))
    # 7 how to play
    P.append(mpage(f'''<h1>How to play</h1>
      <p>The screen has two parts: the <b>room</b> at the top, and the <b>panel</b> at the bottom with the
      sentence line, the nine verbs and your inventory.</p>
      {s('s_bucket')}<div class="cap">The village square. Point at the well and the sentence line says what you are looking at.</div>
      <ul><li><b>Walking:</b> click anywhere in the room. Click an exit to go to the next room.</li>
      <li><b>Doing things:</b> click a verb, then click a thing in the room or in your inventory. The Pilot walks
      there and does it. The sentence line shows what you are building, like <i>Look at Old Well</i>.</li>
      <li><b>Two things:</b> for <i>Use</i> and <i>Give</i>, click the verb, then the first thing, then the second:
      <i>Use rope with Old Well</i>, <i>Give lucky coin to Gobbo</i>.</li>
      <li><b>Right mouse button:</b> the obvious action. Doors open, people get talked to, items get looked at.</li>
      <li><b>Talking:</b> when you talk to someone, the panel shows what you can say. Click a line. Some lines are
      choices that stay with you for the rest of the game, so think before you click!</li></ul>''', 7))
    # 8 verbs and keys
    P.append(mpage(f'''<h1>The verbs</h1>
      <table><tr><th>Verb</th><th>What it does</th></tr>
      <tr><td>Give</td><td>Give an item to someone</td></tr><tr><td>Pick up</td><td>Take something along</td></tr>
      <tr><td>Use</td><td>Use a thing, or use an item with something</td></tr>
      <tr><td>Open / Close</td><td>Doors, hatches, washing machines</td></tr><tr><td>Look at</td><td>Always worth a try</td></tr>
      <tr><td>Push / Pull</td><td>Levers, bricks, plugs, your luck</td></tr><tr><td>Talk to</td><td>People (and sometimes legs)</td></tr></table>
      <h2>Keys</h2>
      <table><tr><td><b>G O C P L T U S Y</b></td><td>The verbs: Give, Open, Close, Pick up, Look at, Talk to, Use, puSh, pull (Y or Z)</td></tr>
      <tr><td><b>Cursor keys</b></td><td>Move the pointer (with Shift: slowly); <b>Return</b> = left click, <b>Del</b> = right click</td></tr>
      <tr><td><b>1 - 6</b></td><td>Choose an answer in a conversation</td></tr>
      <tr><td><b>Left click</b> or <b>.</b></td><td>Skip a line of text</td></tr>
      <tr><td><b>Esc</b></td><td>Skip a cutscene</td></tr><tr><td><b>Space</b></td><td>Pause (when nobody is talking)</td></tr>
      <tr><td><b>F5</b> or <b>MENU</b></td><td>The menu</td></tr></table>
      <h2>The menu (F5 or MENU)</h2>
      <p>Press <b>F5</b>, or click <b>MENU</b> under the verbs, any time (also on the title screen). The menu has
      <b>Save</b> and <b>Load</b> with four slots, <b>Music</b> (high, medium, low or off; the music always goes quiet
      when somebody speaks), <b>Dev mode</b> (jump to any room or get every item, for testers), <b>Resume</b> and
      <b>Quit</b>. Every chapter has its own four save slots. Saved games are written next to the game, so on a
      write-protected floppy you cannot save.</p>
      <img class="shot" src="{SH['g_dialog2_room']}" style="width:64%;margin:2mm auto 1mm"><div class="cap">Talking to Lyra. Choose your words carefully. Some of them she will remember.</div>''', 8))
    # 9-10 people
    ppl = [('pilot', 'The Pilot', 'That is you. Saved the galaxy last year, still parks the STARRAVEN badly. '
            'Never leaves home without a coil of tow rope and his lucky coin from Earth.'),
           ('lyra', 'Lyra', 'Looks after the Moonflower Garden. Silver hair, a blue dress, a laugh like a wind chime, '
            'and a necklace with a shard of the star-pod she arrived in as a baby. Where did that pod come from?'),
           ('pip', 'Pip', 'Your best friend, home at last. Tells everybody about Earth. Some of it is even true. '
            'Will want cake. Scared of the dark, but his ears can glow.'),
           ('zooma', 'Elder Zooma', 'The oldest Stronkie in the village. Knows the old flower lore, '
            'and has a stone tablet that nobody can read. Strange numbers on it.'),
           ('bix', 'Bix', 'The village inventor. His workshop is full of gears, junk and things that go '
            '"sproing". Does not throw anything away. Anything. Builds gliders. And maybe rings.'),
           ('gobbo', 'Gobbo', 'Trader. His stall sells festival ribbons, spare moons and moon cake. '
            'Loves coins. Especially foreign ones.'),
           ('rabbit', 'The White Rabbit', 'Runs past now and then, in every chapter. Always late. '
            'He says cartridges. And where did he leave his pocket watch?')]
    for page, group in ((9, ppl[:4]), (10, ppl[4:])):
        body = '<h1>The people of Stronkie</h1>' if page == 9 else '<h1>The people of Stronkie (2)</h1>'
        for k, name, txt in group:
            body += f'<div class="who"><img src="{SPR[k]}"><div><b>{name}</b><br>{txt}</div></div>'
        if page == 10:
            body += s('f_dance', True) + '<div class="cap">Everybody at the Moon Dance. But who dances with whom?</div>'
        P.append(mpage(body, page))
    # 11 new faces
    new = [('edmund', 'Uncle Edmund', 'Your uncle from Earth. Built a rocket in his garden shed to bring bad news. '
            'Remembers Ravenmoor Manor, and the red book.'),
           ('vex', 'Commander Vex', 'The pirate captain from the first game, also known as Victor, Edmund\'s brother. '
            'Escaped. Has a flagship, a plan with seven steps, and still no idea what step two is.'),
           ('quill', 'Quill', 'Keeper of the Museum of the Old Ones, high in the Sky Temple. Guards the Sacred Floppy, '
            'and asks hard questions about the first game.'),
           ('queen', 'Queen Aurelia', 'The Queen of Lumara, the silver world. Has been asleep for twenty years. '
            'Somebody must have a very good reason to wake her.'),
           ('roger', 'Roger', 'A space janitor who always ends up in the strangest places. This time: a dryer. '
            'Misses his bucket.')]
    body = '<h1>New faces</h1>'
    for k, name, txt in new:
        body += f'<div class="who"><img src="{SPR[k]}"><div><b>{name}</b><br>{txt}</div></div>'
    body += '<p style="font-size:7.6pt;color:#6a5d86">And on Lumara: Mira, Kestrel the gate guard and the old sage. ' \
            'In space: NOVA, the STARRAVEN\'s computer, and a robot that knows a very old door code.</p>'
    P.append(mpage(body, 11))
    # 12-16 the chapters
    P.append(chapter_page(1,
        'The Great Moonflower will not bloom, and without it there is no Moon Dance at the Festival of Two Moons. '
        'Help the village, find a ribbon, and find the courage to ask Lyra to dance.',
        'the landing meadow, the village square, Bix\'s workshop, the Elder\'s hut, the library, the Moonflower Garden, '
        'the gorge, the crystal cave, the forest path and the deep forest',
        'Lyra, Pip, Elder Zooma, Bix, Gobbo and the White Rabbit',
        [('m_meadow', 'The landing meadow, with the STARRAVEN.'), ('w_chicken', 'Bix\'s workshop. Mind the junk pile.'),
         ('x_monkey', 'The library. Look at the painting. Then look again.'), ('c_cave', 'The crystal cave. Somebody painted on the wall.')], 12))
    P.append(chapter_page(2,
        'The morning after the Moon Dance, Lyra\'s shard glows and points to the Crystal Mountains. Up there, in the '
        'Sky Temple, the Old Ones built an observatory. Bix has a new glider. It only needs a sail...',
        'the garden, the square, the workshop, the lookout tower, the snowy ledge, the ice cave, the temple gate, '
        'the Museum of the Old Ones, the lab and the observatory',
        'Quill the museum keeper, a very big sleeping beast, and old friends',
        [('c2_tower', 'The lookout tower. Glider Mark Two is ready.'), ('c2_beast', 'The ice cave. Shh. It is sleeping.'),
         ('c2_museum', 'The Museum of the Old Ones. Some of it looks familiar.'), ('c2_lab', 'The lab. Four old computers. One floppy.')], 13))
    P.append(chapter_page(3,
        'Uncle Edmund lands from Earth in a rocket he built in his garden shed, with bad news: his brother Victor, '
        'better known as Commander Vex, has escaped. And he is looking for the Red Door under the village too.',
        'the Star Heart chamber, the catacombs, a dead end, the hall of murals, a secret room, the mines, the maze, '
        'the red crystal vein and the Red Door',
        'Uncle Edmund, and an old enemy',
        [('c3_cat', 'The catacombs. He has been waiting a long time.'), ('c3_murals', 'The hall of murals. One brick is red.'),
         ('c3_vein', 'The red crystal vein, deep in the mines.'), ('c3_door', 'The Red Door. Somebody got there first.')], 14))
    P.append(chapter_page(4,
        'The STARRAVEN flies to Lumara, the silver world of Lyra\'s people. But Lumara has gone grey, and its Queen '
        'has been asleep for twenty years. Time for Lyra to learn who she really is.',
        'the cockpit and galley of the STARRAVEN, hyperspace, the landing platform, the grey city, the archive, the palace hall, '
        'the Queen\'s chamber and the chamber of the Moon Heart',
        'NOVA, Kestrel, Mira, the old sage and Queen Aurelia',
        [('c4_cockpit', 'The STARRAVEN\'s cockpit. Why is the throttle sticky?'), ('c4_landing', 'Lumara. Have your papers ready.'),
         ('c4_archive', 'The archive. The crystal remembers everything.'), ('c4_queen', 'The Queen\'s chamber.')], 15))
    P.append(chapter_page(5,
        'Vex has stolen the Moon Heart and hidden it on his flagship, the IRON RAVEN. Get it back, take it home to '
        'Lumara, and be back on Stronkie for the next Festival of Two Moons. With a ring.',
        'the hangar, the laundry, the corridor and the bridge of the IRON RAVEN, then Lumara, the village square, '
        'Bix\'s workshop and one room you were never meant to find',
        'Roger (partly), a security robot, Commander Vex, and everybody you ever met',
        [('c5_hangar', 'The hangar of the IRON RAVEN.'), ('c5_laundry', 'The laundry. Those legs look familiar.'),
         ('c5_bridge', 'The bridge. Vex is not happy to see you.'), ('c5_dance', 'One more Moon Dance.')], 16))
    # 17 choices that matter
    P.append(mpage(f'''<h1>Choices that matter</h1>
      <p>Some things you pick up in one chapter are still in your pocket in the next. And some lines you choose in a
      conversation change what happens later, sometimes three chapters later. There is no wrong story, but every
      story ends a little differently.</p>
      <h2>Worth keeping</h2>
      <ul><li><b>The rubber chicken.</b> It has a pulley in the middle. Who knows where it will come in handy.
      Maybe right at the very end.</li>
      <li><b>Anything a rabbit drops.</b> Somebody will miss it in every chapter.</li>
      <li><b>A little sky crystal.</b> It glows. Dark places are less scary with a light.</li>
      <li><b>Borrowed things.</b> Giving something back can make a friend. Friends bring maps.</li></ul>
      <h2>Worth thinking about</h2>
      <ul><li>What you promise Lyra at the end of the Moon Dance.</li>
      <li>Whether you ask for help or do it the hard way.</li>
      <li>What happens to an old enemy when he runs.</li>
      <li>What you answer when a mother asks about her daughter.</li></ul>
      <div class="box">Want to see every ending? Keep a copy of a story file (WOS2.ST2 to WOS2.ST5) before you try
      something else, or simply play a chapter again and choose differently. The last cards of the game are
      different for every story.</div>''', 17))
    # 18-19 hints
    def hints(lines):
        return ''.join(f'<p style="color:#a596bf;margin-bottom:1.3mm">{t}</p>' for t in lines)
    P.append(mpage(f'''<h1>Hints for new adventurers</h1>
      <ul><li><b>Look at everything.</b> Then look at it again with the item in your hand.</li>
      <li><b>Talk to everyone,</b> and try every line. People know more than they say at first.</li>
      <li><b>Strange items have strange uses.</b> In an adventure, nothing is junk. Especially not junk.</li>
      <li><b>Remember the first game.</b> Old passwords, old dates and old insults come back.</li>
      <li><b>Save now and then</b> (F5), in different slots, and try the silly answers too.</li></ul>
      <h2>Stuck? Read only one line at a time.</h2>
      <h2 style="font-size:9pt">Chapter One</h2>
      {hints(['The Moonflower is thirsty, but not for ordinary water.', 'The Old Well has water. You need something to lower.',
              'Crystals grow beyond the gorge. A pulley would get you across.', 'Bix\'s junk pile has the strangest pulley you have ever seen.',
              'Tradition says: no festival ribbon, no Moon Dance. Gobbo likes coins.'])}
      <h2 style="font-size:9pt">Chapter Two</h2>
      {hints(['A glider without a sail is a very heavy kite. The square is full of colourful cloth.',
              'Pip will climb anything for cake.', 'Big sleeping beasts like something to cuddle. Or a lullaby.',
              'Quill only lends the floppy to somebody who knows the first game. When did it all start?',
              'A telescope without its lens shows you nothing.'])}''', 18))
    P.append(mpage(f'''<h1>Hints (2)</h1>
      <h2 style="font-size:9pt">Chapter Three</h2>
      {hints(['At Ravenmoor you pulled a red book. Down here, look for something else that is red.',
              'Pip is scared of the dark. A song or a light helps.', 'Pip has a saying for mazes. He told you last year.',
              'The red crystal is too high. Boing.', 'Vex knows the oldest trick in the book. Pip can make it more convincing.'])}
      <h2 style="font-size:9pt">Chapter Four</h2>
      {hints(['Somebody ate moon cake in the cockpit. Sticky things need a wet cloth.',
              'Lumara likes paperwork. Look under the pilot\'s seat.', 'The archive knows the whole story. Read it.',
              'A sleeping Queen needs a very special song.', 'Light and mirrors opened a door in the first game, too.'])}
      <h2 style="font-size:9pt">Chapter Five</h2>
      {hints(['Talk to the legs. Really.', 'Nobody looks twice at somebody in uniform.',
              'Vex never won an insult duel in his life. You know the answers from the first game.',
              'Gobbo collects hats. Especially famous ones.', 'A ring needs a stone and some metal. You have both, somewhere.'])}''', 19))
    # 20-21 easter eggs
    P.append(mpage(f'''<h1>The great easter egg hunt</h1>
      <p>Old heroes of adventure games, and of the first World of Stronkie, have left things behind. Tick them off
      when you find them.</p>
      <h2>Chapter One</h2>
      <ul class="check"><li>A well that makes you want to throw valuable items into it</li>
      <li>A book about winning sword fights with words</li><li>Somebody who is late. Again.</li>
      <li>A stone tablet with a very familiar error number</li><li>A painting with one head too many. Or two.</li>
      <li>A chicken with something in the middle</li><li>An artist's work from around 1991</li>
      <li>A place that is a dead end. Literally. Give it time.</li><li>A sword that belongs to another franchise</li></ul>
      <h2>Chapter Two</h2>
      <ul class="check"><li>A box of disks that must never be lost</li><li>A glider you no longer have to type at</li>
      <li>An old tent with a book on ruling a galaxy</li><li>A sign that asks you not to shout</li>
      <li>A hall full of things from the first game, including your sandwich</li>
      <li>Four old computers and their four favourite error messages</li><li>A very high Astro Chicken score</li></ul>
      <div class="two" style="margin-top:2mm"><div>{s('x_book', True)}</div><div>{s('c2_lab', True)}</div></div>''', 20))
    P.append(mpage(f'''<h1>The egg hunt (2)</h1>
      <h2>Chapter Three</h2>
      <ul class="check"><li>A skeleton who should have brought a lamp</li><li>Somebody else was here. Three times.</li>
      <li>An Old One with a one-button joystick</li><li>A little green-haired fellow walking into a wall</li>
      <li>A warning about grues</li><li>A maze of twisty little passages</li></ul>
      <h2>Chapter Four</h2>
      <ul class="check"><li>A computer that remembers the airlock</li><li>A napkin with a familiar password</li>
      <li>Somebody late, even in hyperspace</li><li>A used starship dealer, back in twenty years</li>
      <li>Somebody asking about a famous burger</li><li>Shelf number 42</li><li>A WANTED poster</li></ul>
      <h2>Chapter Five</h2>
      <ul class="check"><li>The plans for step two</li><li>A rule about red socks</li><li>A door code that does not work any more</li>
      <li>A plug worth pulling, again</li><li>A captain on the radio</li><li>An engraving on a ring</li>
      <li>A rabbit who is on time. For once.</li><li>A secret room behind the junk, with a calendar full of Sundays</li></ul>
      <div class="two" style="margin-top:2mm"><div>{s('c3_secret', True)}</div><div>{s('c5_office', True)}</div></div>''', 21))
    # 22 funny facts
    facts = ['The game is written in 68000 assembler, the same language the classic Amiga games were written in. '
             'The rest (pictures, people, music) is made by little Python programs.',
             'Every person is drawn four times too big with simple shapes, then shrunk, so the pixels look '
             'hand-made. Nobody in the game has more than 16 colours to wear.',
             'All five chapters together have nearly fifty rooms and more than 1,400 lines of text.',
             'Roger only shows his legs in chapter five. The chip memory was full, and there was no room left for '
             'the rest of him. So he went in the dryer.',
             'For a while, playing the music box on Lumara made Mira start talking. The music routine borrowed a '
             'register the script was still using. One saved register later, the music box behaves.',
             'In one test, Lyra stood right in front of her own mother, so you could not click on the Queen. Lyra '
             'now politely steps aside.',
             'The Elder\'s tablet shows Guru Meditation #00000004. On a real Amiga that means an illegal '
             'instruction. On Stronkie it means "do not touch".',
             'In the first test run, pressing Space on the title screen paused the game instead of starting it. '
             'It waited very patiently.']
    body = '<h1>Funny facts</h1>' + ''.join(f'<div class="fact"><span>{i + 1}</span><div>{t}</div></div>'
                                          for i, t in enumerate(facts))
    P.append(mpage(body, 22))
    # 23 dev log
    P.append(mpage(f'''<h1>The dev log</h1>
      <div class="log"><div><b>The idea.</b> After The World of Stronkie came out with typed commands, part two had to be
      point and click, like the big adventure games of the time. And it had to be a love story.</div>
      <div><b>The engine.</b> Double-buffered 32-colour rooms, people drawn by the blitter, text over every head, a script
      language for all the puzzles, and the nine verbs. The first time it ran, it cleared its own variables. One line moved.</div>
      <div><b>Too much for chip memory.</b> The people first needed 726 KB. Cutting the empty edges off every picture
      brought chapter one down to 209 KB. Every chapter since has had to fit the same budget.</div>
      <div><b>Five disks.</b> One disk was never going to be enough for the whole story. So every chapter got its own disk,
      its own rooms and music, and a version number of its own, so it can be updated on its own.</div>
      <div><b>The story file.</b> To let the story carry on, each chapter now writes 36 bytes at the end: what you carry and
      what you chose. Small file, big difference: the people of Stronkie remember you.</div>
      <div><b>The walk test.</b> A test robot plays every chapter from start to finish in an emulator, clicking and waiting
      like a very patient player. It found the music box bug, the Queen nobody could click, and a lot of patience.</div></div>
      {s('c4_heart', True)}<div class="cap">The chamber of the Moon Heart.</div>''', 23))
    # 24 credits
    P.append(mpage(f'''<h1>Credits</h1>
      <table><tr><td>Game design, story and everything else</td><td><b>Mark Stronks</b></td></tr>
      <tr><td>Published by</td><td><b>Stronkie Soft</b></td></tr>
      <tr><td>Versions</td><td>Chapter One {CHAPTERS[0][2]} &middot; Two {CHAPTERS[1][2]} &middot; Three {CHAPTERS[2][2]}
      &middot; Four {CHAPTERS[3][2]} &middot; Five {CHAPTERS[4][2]}</td></tr></table>
      <p>Special thanks to everybody who tests the games, leaves a comment or a rating on itch.io, and to the
      adventure games of the eighties and nineties that made us all try to use a rubber chicken on everything.</p>
      <h2>Notes</h2><div class="lines">{'<div></div>' * 8}</div>
      <div style="text-align:center;margin-top:5mm"><img src="{U['logo']}" style="width:34mm"></div>
      <p style="text-align:center;font-size:7pt;color:#8a7aa8;margin-top:2mm">Created By Mark Stronks, Stronkie Soft
      &copy; 2026 &middot; stronkie.itch.io</p>''', 24))
    html = f'<html><head><style>{MAN_CSS}</style></head><body>{"".join(P)}</body></html>'
    out = os.path.join(OUTD, 'WorldOfStronkieII_Manual.pdf')
    pdf(html, out, '148mm', '210mm')
    return out


# ================================================================== disk labels
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


def labels():
    pics = {1: U['scene'], 2: SH.get('c2_obs_room'), 3: SH.get('c3_door_room'), 4: SH.get('c4_heart_room'),
            5: SH.get('c5_dance_room')}

    def lab(n, demo=False):
        if demo:
            d, nm, v, pic = 'DEMO DISK', 'Try it first: free!', 'V0.1.4', U['scene']
        else:
            nm, v = CHAPTERS[n - 1][1], CHAPTERS[n - 1][2]
            d, pic = f'DISK {n} OF 5', pics[n] or U['scene']
        ch = '' if demo else f'CHAPTER {NUM[n].upper()}: '
        return f'''<div class="lab"><div class="fold">THE WORLD OF STRONKIE II &middot; {d}</div>
          <img class="t" src="{U['title']}"><img class="sc" src="{pic}">
          <div class="n">{ch}{nm.upper()}</div>
          <div class="d{' demo' if demo else ''}">{d} &middot; {v}</div>
          <div class="c" style="font-size:5.5pt">Stronkie World II {"Demo" if demo else f"Ch {n}"} {v}</div>
          <div class="c">Amiga 500 &middot; 1 MB &middot; Kickstart 3.1 &middot; Stronkie Soft &copy; 2026</div></div>'''
    html = f'''<html><head><style>{LAB_CSS}</style></head><body><div class="sheet">
      <h1>{TITLE}: disk labels</h1>
      <div class="note">Print at 100% ("actual size", not "fit to page") on sticker paper, or on plain paper and glue.
      Cut along the dashed lines. Stick the label on the front of the disk and fold the top strip over to the back.</div>
      <div class="grid">{''.join(lab(n) for n in range(1, 6))}{lab(0, True)}</div></div></body></html>'''
    out = os.path.join(OUTD, 'WorldOfStronkieII_DiskLabels.pdf')
    pdf(html, out, '210mm', '297mm')
    return out


# ================================================================== the box
W, H, D, TUCK, GLUE = 140, 180, 34, 15, 12   # mm


def panels():
    """the HTML of each face (front, back, side, top, bottom), sized in mm"""
    front = f'''<div class="face night" style="width:{W}mm;height:{H}mm">
      <div style="background:#ffd560;color:#2a1450;text-align:center;font-weight:800;letter-spacing:.2em;font-size:6.5pt;padding:1.6mm">STRONKIE SOFT PRESENTS</div>
      <img src="{U['title']}" style="width:132mm;display:block;margin:3mm auto 0">
      <img src="{U['scene']}" style="width:132mm;display:block;margin:4mm auto 0;border:.6mm solid #5a6ad0">
      <div style="text-align:center;margin-top:3mm;font-size:11pt;font-weight:800;color:#fff">A POINT &amp; CLICK ADVENTURE</div>
      <div style="text-align:center;font-size:8pt;color:#ff8cc0;margin-top:.6mm">The complete adventure &middot; five chapters on five disks</div>
      <img src="{SH.get('f_dance_room', '')}" style="width:96mm;display:block;margin:4mm auto 0;border:1.2mm solid #fff;
        transform:rotate(-2deg);box-shadow:1.5mm 1.5mm 0 #000">
      <div style="text-align:center;font-size:7pt;color:#e8e4ff;margin-top:2.5mm;font-style:italic">
        Tonight both moons rise full. Will she dance with you?</div>
      <div style="position:absolute;right:4mm;top:112mm;width:27mm;height:27mm;border-radius:50%;background:#ff4f8b;color:#fff;
        transform:rotate(12deg);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;
        font-size:6.6pt;line-height:1.15;box-shadow:0 0 0 .7mm #fff">5 DISKS!<br>SPEECH!<br>ROMANCE!</div>
      <div style="position:absolute;bottom:10.5mm;left:0;right:0;background:#d8202f;color:#fff;text-align:center;font-weight:800;
        font-size:6.4pt;line-height:1.25;padding:1.4mm 2mm">FOR THE AMIGA 500 WITH <span style="color:#ffd560">1 MB</span> (512K CHIP + 512K TRAPDOOR)<br>
        KICKSTART / WORKBENCH 3.1 &middot; NO ACCELERATOR NEEDED</div>
      <div style="position:absolute;bottom:0;left:0;right:0;background:#7a3ad0;color:#fff;text-align:center;font-weight:800;
        font-size:11pt;letter-spacing:.15em;padding:2.4mm">AMIGA 500 &middot; 1 MB &middot; 5 DISKS</div></div>'''
    shots = ''.join(s(n) for n in ['g_dialog2', 'c2_museum', 'c3_door', 'c4_landing', 'c5_laundry', 'c5_dance'])
    back = f'''<div class="face night" style="width:{W}mm;height:{H}mm;padding:4mm 5mm">
      <div style="background:#ffd560;color:#2a1450;font-weight:800;font-size:8.5pt;padding:1.6mm 2.5mm;margin:-4mm -5mm 3mm">
        "TONIGHT BOTH MOONS RISE FULL. AND I HAVE TO ASK HER."</div>
      <p style="font-size:7pt;line-height:1.35">One year after the adventure of the Star Heart, the Pilot flies Pip home
      to the World of Stronkie for the Festival of Two Moons, and meets Lyra, the girl with the glowing necklace.
      Her shard leads up the Crystal Mountains, under the village to the Red Door, to Lumara, the silver world
      of her people, and onto the flagship of an old enemy. Five chapters, one love story. Bring a ring.</p>
      <div class="bshots">{shots}</div>
      <ul style="font-size:6.8pt;line-height:1.4;margin:2.5mm 0 0 3.5mm">
      <li>Point and click with nine verbs, like the classic LucasArts adventures</li>
      <li>Five chapters on five disks, nearly fifty hand-painted rooms in 32 colours</li>
      <li>Your story carries over: what you carry and what you choose change the ending</li>
      <li>Speech, music for every place, cutscenes. You can never die and never get stuck</li>
      <li>Dozens of easter eggs, with nods to the first World of Stronkie</li></ul>
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
    side = f'''<div class="face night" style="width:{D}mm;height:{H}mm">
      <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-90deg);white-space:nowrap;
        text-align:center"><div style="font-size:13pt;font-weight:800;color:#5ad8ec;letter-spacing:.02em">THE WORLD OF STRONKIE <span class="gold">II</span></div>
        <div style="font-size:6.5pt;color:#ff8cc0">A Love on Stronkie &middot; 5 disks &middot; Amiga 500 &middot; Stronkie Soft</div></div></div>'''
    spec = f'''<div class="face night" style="width:{D}mm;height:{H}mm;padding:5mm 2.5mm;font-size:6pt;line-height:1.45">
      <img src="{U['logo']}" style="width:28mm;display:block;margin:0 auto 4mm">
      <div style="background:#d8202f;color:#fff;font-weight:800;font-size:6.6pt;padding:1.2mm;text-align:center;margin-bottom:2mm">AMIGA 500<br>1 MB</div>
      <div class="gold" style="font-weight:800;font-size:7pt;margin-bottom:1.5mm">MINIMUM SYSTEM</div>
      Amiga 500<br>68000, 7 MHz<br>512 KB chip<br>512 KB trapdoor<br>Kickstart 3.1<br>Mouse
      <div style="color:#ff5060;font-weight:800;margin-top:2mm">No accelerator<br>needed</div>
      <div class="gold" style="font-weight:800;font-size:7pt;margin:3mm 0 1.5mm">IN THE BOX</div>
      5 disks<br>Instruction manual<br>Disk labels
      <div class="gold" style="font-weight:800;font-size:7pt;margin:3mm 0 1.5mm">ALSO RUNS</div>
      From hard drive, CF card or WHDLoad
      <div style="position:absolute;bottom:4mm;left:0;right:0;text-align:center;font-weight:800;color:#fff;font-size:5.4pt">{VERSION}</div></div>'''
    top = f'''<div class="face night" style="width:{W}mm;height:{D}mm;display:flex;align-items:center;justify-content:space-around">
      <img src="{U['title']}" style="width:96mm"><img src="{U['logo']}" style="width:26mm"></div>'''
    bottom = f'''<div class="face night" style="width:{W}mm;height:{D}mm;display:flex;align-items:center;justify-content:center;
      font-size:7pt;color:#b8b0d8;text-align:center">5 disks &middot; Amiga 500 &middot; 1 MB (512K chip + 512K trapdoor) &middot; Kickstart / Workbench 3.1<br>
      Created By Mark Stronks &middot; Stronkie Soft &copy; 2026</div>'''
    return front, back, side, spec, top, bottom


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


def box_pdfs():
    a3 = os.path.join(OUTD, 'WorldOfStronkieII_Box_A3.pdf')
    pdf(box_net(420, 297, 'The box (A3, full size)', 'For A3 card.'), a3, '420mm', '297mm')
    a4 = os.path.join(OUTD, 'WorldOfStronkieII_Box_A4.pdf')
    pdf(box_net(297, 210, 'The box (A4, smaller)', 'A smaller box that fits on A4 card.'), a4, '297mm', '210mm')
    return a3, a4


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
    p = os.path.join(OUTD, 'WorldOfStronkieII_Box_3D.png')
    bg.save(p)
    return p


if __name__ == '__main__':
    print(manual())
    print(labels())
    print(*box_pdfs())
    print(box_3d(faces_png()))
