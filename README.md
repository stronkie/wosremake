# World of Stronkie remake

The original **The World of Stronkie** (Amiga 500, V2.4) as a point-and-click adventure
on the engine of **The World of Stronkie II**: no more typing. Same story, same puzzles,
the same pictures, music, sound effects and speech - played with the mouse and the nine
LucasArts-style verbs. Created By Mark Stronks, Stronkie Soft.

The text adventure stays as it is: it is still on itch.io and in its own repo.

## The chapters

| Disk | Chapter | Original parts | Version |
|---|---|---|---|
| 1 | Chapter One: the Prologue | Prologue 1-3: The Grounds, The Manor, The Launch Pad | V0.1.0 |
| 2 | Chapter Two: Into Space | Chapter 1 of the original | (to come) |

Every chapter is its own disk and boots by itself. When you finish a chapter the game
writes your story (`WOSR.ST2`: the star fragments you found, what you carry), and the
next chapter continues from there, like World of Stronkie II.

**Free demo:** `WorldOfStronkieRemake_Chapter1_Demo_V0.1.0.adf` - Part 1, The Grounds,
up to the front door of Ravenmoor Manor.

## What you need

- Amiga 500, 68000 (7 MHz), Kickstart / Workbench 3.1
- 1 MB chip memory (8372A Agnus: 512 KB + the 512 KB trapdoor). No fast memory needed.

## Starting the game

**From the floppy:** write `WorldOfStronkieRemake_Chapter1_V0.1.0.adf` to a disk (disk
name `Stronkie Remake Ch 1 V0.1.0`) and boot from it.

**From the hard drive:** copy `WOSR`, `WOSR.DAT`, `WOSR.GFX`, `WOSR.STR` and
`WOSR.info` into a drawer and double-click the icon.

**WHDLoad:** `WorldOfStronkieRemake_Chapter1_V0.1.0_WHDLoad.zip` (needs WHDLoad and
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

### V0.1.0 (2026-11-27) - Chapter One: the Prologue, and the free demo
- The first chapter of the remake: Prologue parts 1-3 (The Grounds, The Manor,
  The Launch Pad), 17 rooms, point and click, no typing.
- Runs on the default Amiga 500: 68000, Kickstart / Workbench 3.1, 1 MB chip memory.
- The free demo: Part 1, The Grounds (only the rooms of Part 1 are on the demo disk).
- Engine (from WoS II V0.x.4): *Use* + the same item twice uses it on its own.
- Tested in vAmigaWeb (AROS ROM): the whole chapter played through with the mouse, and the demo.
