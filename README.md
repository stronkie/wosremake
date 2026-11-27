# World of Stronkie remake

The original **The World of Stronkie** (Amiga 500, V2.4) as a point-and-click adventure
on the engine of **The World of Stronkie II**: no more typing. Same story, same puzzles,
the same pictures, music, sound effects and speech - played with the mouse and the nine
LucasArts-style verbs. Created By Mark Stronks, Stronkie Soft.

The text adventure stays as it is: it is still on itch.io and in its own repo.

## The chapters

| Disk | Chapter | Original chapters | Keepsake | Version |
|---|---|---|---|---|
| 1 | Chapter One: the Prologue | Prologue 1-3: The Grounds, The Manor, The Launch Pad | scrap of paper | V0.1.1 |
| 2 | Chapter Two: Into Space | 1 Into Space, 2 The Derelict Station | space ration | V0.2.0 |
| 3 | Chapter Three: Asteroid 42 | 3 Asteroid 42, 4 Space Pirates | rubber chicken | V0.3.0 |
| 4 | Chapter Four: Landfall | 5 Landfall, 6 The Village | singing shell | V0.4.0 |
| 5 | Chapter Five: The Crystal Mountains | 7 The Crystal Mountains, 8 The Sky Temple | spiked boots | V0.5.0 |
| 6 | Chapter Six: The Star Heart | 9 The Star Heart, 10 Repairs | silver horn | V0.6.0 |
| 7 | Chapter Seven: Vex's Flagship | 11 Vex's Flagship, 12 The Prison Deck, 13 The Bridge, Epilogue | - | V0.7.0 |

Every chapter is its own disk and boots by itself. When you finish a chapter the game
writes your story on that disk (`WOSR.ST2` ... `WOSR.ST7`: the star fragments you found,
the choices that matter, what you carry), and the next chapter reads it from there.

**The item check list.** Every disk gives you one keepsake that you keep for the rest of
the game (see the table). At the start of a disk the game checks the keepsakes of ALL the
disks before it: if one is missing from your story, the disk says ITEM CHECK FAILED and
does not go on. The story file has a check code, so a story file made or changed by hand
is refused too. Dev mode (F5) skips the check.

**Choices that matter** (as in the original): the napkin for Roger, the kick for Astro
Chicken, untying Ricky and LeChuckle's rematch (disk 3), the wooden monkey and the nose
glasses (disk 4) come back on disk 7. With all 16 star fragments you get the true ending.

**Free demo:** `WorldOfStronkieRemake_Chapter1_Demo_V0.1.1.adf` - Part 1, The Grounds,
up to the front door of Ravenmoor Manor.

## What you need

- Amiga 500, 68000 (7 MHz), Kickstart / Workbench 3.1
- 1 MB chip memory (8372A Agnus: 512 KB + the 512 KB trapdoor). No fast memory needed.

## Starting the game

**From the floppy:** write `WorldOfStronkieRemake_ChapterN_V0.N.x.adf` to a disk (disk
name `Stronkie Remake Ch N V0.N.x`) and boot from it. Keep the disks writable: the end
of a chapter writes your story on it. At the start of the next disk the game asks for
the disk before it, reads the story and asks for its own disk back.

**From the hard drive:** copy the files of a disk (`WOSR`, `WOSR.DAT`, ... for disk 1,
`WOSRC2`, `WOSRC2.DAT`, ... for disk 2 and so on) into ONE drawer and double-click the
icon: then the story goes from chapter to chapter in that drawer by itself.

**WHDLoad:** `WorldOfStronkieRemake_ChapterN_V0.N.x_WHDLoad.zip` (needs WHDLoad and
kick40063.A600 in DEVS:Kickstarts; F10 quits).

## Playing

| | |
|---|---|
| Left mouse button | walk, choose a verb, use the verb on something |
| Right mouse button | the obvious action (open a door, talk to someone, look at an item) |
| Click on an item, then on something else | *Use* or *Give* with two things |
| *Use*, then the same item twice | use an item on its own (put on the spacesuit) |
| `G O C P L T U S Y` | the verbs from the keyboard |
| Cursor keys, `Return`, `Del` | move the pointer, left click, right click |
| Click / `.` / `Space` | skip a line of text |
| `F5` or click `MENU` | save and load (4 slots), music, dev mode (jump to any room, get the items), quit |

You can never die and never get stuck. The deaths of the text adventure are still
there, but now your hero thinks twice. The three star fragments of the Prologue are
hidden in the same places as in the original: look for them.

## What came over from the original

- **Story and puzzles:** every room, object and puzzle of Prologue parts 1-3, with the
  original texts (room descriptions, examine texts, Uncle Edmund's lines, the jokes).
- **Pictures:** the 17 original Amiga pictures (320 x 192, 32 colours), cut to the
  320 x 168 room of the engine and reduced to its 16 room colours. Things that change
  (the dug-up mound, the bucket, open doors, the hatch, the roof, the lift-off) are
  painted over them.
- **Music:** the original tunes (title, The Grounds, The Manor, The Launch Pad), note for
  note: the SID-style voices and envelopes became sampled instruments.
- **Sound and speech:** the original's sampled effects and its speech ("Welcome to the
  World of Stronkie!", the spoken title cards, "Congratulations!").

## Building

```sh
. /home/claude/amiga-toolkit/setup.sh          # vasm, the packer, the adf tools
cd source
python3 build.py all                           # out/: the program, the data, the ADF, WHDLoad
WOS2_DEMO=1 python3 build.py all               # out_demo/: the free demo
python3 tools/sim.py                           # plays chapters/ch1_walk.py: every puzzle can be solved
python3 tools/webplay.py disk.adf outdir steps # plays the disk in vAmigaWeb with the mouse
```

`source/orig/` holds the original pictures, tunes (`songs.json`) and sampled sounds.
The engine (`*.s`) is World of Stronkie II's.

## Changelog

### V0.2.0 - V0.7.0 (2026-11-27) - Chapters Two to Seven: the whole game
- Disks 2-7: all the original chapters 1-13 and the epilogue, with the original
  pictures, music (the SID songs of every part) and speech (NOVA and the chapter cards).
- Every typed puzzle is now a point-and-click one: the codes, passwords and insult
  sword fights are conversations, the deaths are lines where your hero thinks twice.
- The item check list: one keepsake per disk, checked on every later disk (see above).
- The choices that matter, the wooden monkey bonus and the true ending, as in the original.

### V0.1.1 (2026-11-27) - Chapter One
- Music softer, speech louder (the original samples, made about twice as loud).
- The scrap of paper is the keepsake of disk 1: you always get it at the front door.
- The story file has a check code; it is checked by the next disk.
- Fix: writing the story at the end of the chapter could hang the game (the disk needs
  the blitter during the DOS call).

### V0.1.0 (2026-11-27) - Chapter One: the Prologue, and the free demo
- The first chapter of the remake: Prologue parts 1-3 (The Grounds, The Manor,
  The Launch Pad), 17 rooms, point and click, no typing.
- Runs on the default Amiga 500: 68000, Kickstart / Workbench 3.1, 1 MB chip memory.
- The free demo: Part 1, The Grounds (only the rooms of Part 1 are on the demo disk).
- Engine (from WoS II V0.x.4): *Use* + the same item twice uses it on its own.
- Tested in vAmigaWeb (AROS ROM): the whole chapter played through with the mouse, and the demo.
