"""The rooms of World of Stronkie remake: the original World of Stronkie
pictures (Amiga V2.4, 320 x 192, 32 colours, painted by Mark Stronks's
art scripts), cut to the 320 x 168 room of the World of Stronkie II engine.

Every room is a Canvas like the painted rooms of WoS II, so build.py reduces
it to 16 room colours in the same way. Things that change (a dug-up mound,
an open door, the bucket at the top of the well...) are painted over the
original picture with keyword arguments: build.py turns the difference into
an object picture (game.VARIANTS).
"""
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paint import Canvas, rgb, W, H              # noqa: E402

ORIG = os.path.join(HERE, '..', 'orig')
CROP = {}                                       # room -> first line of the original picture (default 16)


def base(name, top=None):
    """the original picture, lines top .. top+167, as a canvas"""
    top = CROP.get(name, 16) if top is None else top
    im = Image.open(os.path.join(ORIG, name + '.png')).convert('RGB')
    a = np.asarray(im, np.float32)[top:top + H] / 255
    cv = Canvas()
    cv.c = np.repeat(np.repeat(a, 2, 0), 2, 1).copy()
    return cv


def copy(cv, x0, y0, x1, y1, dx, dy):
    """copy the box (x0,y0)-(x1,y1) of the picture to dx,dy (picture coordinates)"""
    s = cv.c[y0 * 2:y1 * 2, x0 * 2:x1 * 2].copy()
    cv.c[dy * 2:dy * 2 + s.shape[0], dx * 2:dx * 2 + s.shape[1]] = s


def orig_box(cv, name, x0, y0, x1, y1):
    """put the original pixels of the box back"""
    o = base(name)
    cv.c[y0 * 2:y1 * 2, x0 * 2:x1 * 2] = o.c[y0 * 2:y1 * 2, x0 * 2:x1 * 2]


def dark_door(cv, pts, deep='#07060a', rim='#2a2018', glow=None):
    m = cv.poly(pts)
    cv.fill(m, deep)
    if glow:
        cv.fill(m * np.clip((cv.Y - min(y for _, y in pts)) / 60, 0, 1), glow, 0.35)
    edge = np.clip(cv.blur(m, 1.2) - m, 0, 1)
    cv.fill(edge, rim, 0.8)
    return m


# ------------------------------------------------------------------ Part 1: the grounds
def road():
    return base('road')


def garden(dug=False, handle=False):
    cv = base('garden')
    # the original picture has the shovel stuck in the mound already: in the
    # remake the shovel is in the shed, so paint grass and earth over it
    copy(cv, 4, 92, 24, 124, 170, 92)         # grass over the handle
    copy(cv, 148, 124, 160, 136, 172, 124)       # earth over the blade on the mound
    copy(cv, 4, 136, 20, 150, 170, 136)       # grass under the mound
    if dug:
        m = cv.ellipse(158, 129, 15, 5)
        cv.fill(m, '#1a0f08')
        cv.fill(cv.ellipse(158, 128, 11, 3), '#0a0604')
        cv.fill(cv.ellipse(186, 136, 9, 3.5), '#5a3418')      # the dug-out earth
        cv.fill(cv.ellipse(185, 135, 6, 2), '#7a4a24')
        orig_box(cv, 'garden', 170, 92, 190, 150)               # the shovel, stuck in the earth
        if handle:                                              # the iron handle, half out of the hole
            cv.fill(cv.rect(150, 126, 160, 128), '#8a8c94')
            cv.fill(cv.rect(158, 121, 160, 128), '#8a8c94')
    return cv


def shed(shovel=False):
    cv = base('shed')
    copy(cv, 104, 50, 118, 86, 150, 50)          # bare planks
    copy(cv, 104, 50, 118, 74, 150, 26)          # (where the shovel hangs)
    if shovel:
        orig_box(cv, 'shed', 150, 26, 164, 86)
    return cv


def well(bucket=False, key=False):
    cv = base('well')
    if bucket:
        cv.fill(cv.line([(160, 50), (160, 64)], 1.0), '#c8b070')
        m = cv.poly([(151, 64), (169, 64), (167, 80), (153, 80)])
        cv.fill(m, '#6a4422')
        cv.fill(cv.rect(152, 67, 168, 69), '#3a3a40')
        cv.fill(cv.rect(153, 76, 167, 78), '#3a3a40')
        cv.fill(cv.line([(151, 64), (160, 58), (169, 64)], 0.8), '#3a3a40')
        cv.fill(cv.ellipse(160, 65, 8, 1.6), '#20140a')
        if key:
            cv.fill(cv.rect(157, 62, 164, 65), '#f0c040')       # the brass key in it
        # the handle on the winch
        cv.fill(cv.line([(216, 48), (226, 48), (226, 58)], 1.4), '#56575c')
    return cv


def porch(open_door=False):
    cv = base('porch')
    if open_door:
        dark_door(cv, [(126, 28), (194, 28), (194, 140), (126, 140)], glow='#402010')
        m = cv.poly([(194, 26), (208, 18), (208, 146), (194, 140)])            # the door, swung in
        cv.fill(m, '#4a2a14')
        cv.fill(cv.rect(196, 60, 199, 66), '#c0a060')
    return cv


# ------------------------------------------------------------------ Part 2: the manor
def hall(small_open=False):
    cv = base('hall')
    if small_open:
        dark_door(cv, [(97, 75), (111, 75), (111, 101), (97, 101)], glow='#302010')
    return cv


def library(passage=False):
    cv = base('library')
    if passage:
        dark_door(cv, [(18, 26), (56, 40), (56, 118), (18, 132)], glow='#203040')
        cv.fill(cv.poly([(56, 40), (70, 34), (70, 112), (56, 118)]), '#3a2410')   # the shelf, swung open
    return cv


def kitchen(candle=False, matches=False, knife=False):
    cv = base('kitchen')
    # a little wooden shelf on the left wall
    cv.fill(cv.rect(64, 78, 104, 81), '#5a3a1c')
    cv.fill(cv.rect(64, 81, 104, 82), '#2a1a0c')
    cv.fill(cv.poly([(68, 82), (72, 82), (72, 88)]), '#4a2a14')
    cv.fill(cv.poly([(96, 82), (100, 82), (96, 88)]), '#4a2a14')
    if candle:
        cv.fill(cv.rect(72, 66, 76, 78), '#f0e8d0')
        cv.fill(cv.rect(72, 66, 73, 78), '#c8c0a8')
        cv.fill(cv.rect(73, 64, 75, 66), '#202020')
    if matches:
        cv.fill(cv.rect(86, 73, 96, 78), '#c03020')
        cv.fill(cv.rect(86, 73, 96, 74), '#f0d040')
        cv.fill(cv.rect(88, 75, 94, 77), '#f0e8d0')
    if knife:
        cv.fill(cv.poly([(238, 100), (256, 98), (258, 100), (238, 101)]), '#d0d8e0')
        cv.fill(cv.rect(258, 98, 266, 101), '#3a2210')
    return cv


def cellar(key=False):
    cv = base('cellar')
    if key:
        cv.fill(cv.ellipse(108, 152, 3, 2), '#d8dce8')
        cv.fill(cv.ellipse(108, 152, 1.3, 0.8), '#30281c')
        cv.fill(cv.rect(110, 151, 118, 153), '#d8dce8')
        cv.fill(cv.rect(115, 153, 116, 155), '#d8dce8')
        cv.fill(cv.rect(117, 153, 118, 155), '#d8dce8')
    return cv


def study():
    cv = base('study')
    cv.keep = ['#8855cc']                  # the purple tentacle's jar stays purple
    return cv


def secret(amulet=False, freed=False):
    cv = base('secret')
    if freed:                                    # Uncle Edmund is free: an empty chair, cut ropes
        cv.fill(cv.rect(146, 80, 174, 112), '#4a2c14')
        cv.fill(cv.rect(146, 80, 174, 84), '#5a3818')
        cv.fill(cv.rect(148, 108, 172, 116), '#3a2210')
        for x0, y0, x1, y1 in ((134, 132, 146, 136), (176, 130, 190, 133), (150, 136, 164, 139)):
            cv.fill(cv.line([(x0, y0), (x1, y1)], 1.0), '#a08a5a')
    if amulet:
        cv.glow(cv.ellipse(206, 151, 3, 3), '#ff4020', 6, 0.7)
        cv.fill(cv.ellipse(206, 151, 4, 3), '#e0b030')
        cv.fill(cv.ellipse(206, 151, 2, 1.5), '#e02010')
        cv.fill(cv.line([(202, 149), (199, 144), (213, 144), (210, 149)], 0.6), '#e0b030')
    return cv


# ------------------------------------------------------------------ Part 3: the launch pad
def stairs():
    return base('stairs')


def bunker(open_door=False):
    cv = base('bunker')
    if open_door:
        m = cv.rect(110, 34, 210, 104)
        cv.fill(m, '#0c0e12')
        cv.fill(cv.rect(110, 34, 210, 104) * np.clip((cv.Y - 34) / 70, 0, 1), '#405060', 0.5)
        cv.fill(cv.rect(110, 30, 210, 36), '#c8b020')                         # the door, rolled up
        cv.fill(cv.rect(110, 34, 210, 35), '#2a2a2a')
        for x in range(116, 206, 16):
            cv.fill(cv.rect(x, 94, x + 8, 96), '#ffd040')                    # the hangar lights beyond
    return cv


def lockers(open_locker=False):
    cv = base('lockers')
    if open_locker:
        dark_door(cv, [(186, 31), (206, 31), (206, 104), (186, 104)], deep='#101418', rim='#2a3040')
        cv.fill(cv.poly([(206, 30), (222, 24), (222, 110), (206, 104)]), '#6878a0')   # the open door
        cv.fill(cv.poly([(208, 34), (220, 30), (220, 34), (208, 38)]), '#20283a')
        cv.fill(cv.rect(188, 50, 204, 51), '#505868')                         # the empty shelf
    return cv


def hangar(hatch=False, roof=False, flame=False):
    cv = base('hangar')
    # the door of the launch control room, in the rock on the right
    dark_door(cv, [(228, 88), (252, 88), (252, 122), (228, 122)], deep='#1c2a30', rim='#606878', glow='#80c0e0')
    cv.fill(cv.rect(231, 82, 249, 86), '#30c060')
    if roof:
        m = cv.poly([(60, 0), (260, 0), (240, 12), (80, 12)])
        cv.fill(m, '#050818')
        for x, y in ((90, 4), (130, 8), (170, 3), (205, 7), (235, 3), (150, 6)):
            cv.fill(cv.rect(x, y, x + 1, y + 1), '#ffffff')
    if hatch:
        dark_door(cv, [(150, 96), (168, 96), (168, 114), (150, 114)], deep='#1a1410', rim='#606070', glow='#ffc060')
        cv.fill(cv.poly([(150, 114), (168, 114), (180, 140), (140, 140)]), '#8a8a96')   # the ramp
        cv.fill(cv.poly([(150, 114), (168, 114), (170, 118), (148, 118)]), '#5a5a66')
    if flame:
        m = cv.poly([(140, 118), (178, 118), (172, 132), (166, 162), (158, 140), (152, 162), (146, 132)])
        cv.fill(m, '#ff9020')
        cv.fill(cv.poly([(148, 118), (170, 118), (164, 130), (159, 148), (154, 130)]), '#ffe080')
        cv.glow(m, '#ff6010', 14, 0.6)
    return cv


def control(amulet=False, lever=False):
    cv = base('control')
    if amulet:
        cv.glow(cv.ellipse(160, 111, 10, 3), '#ff3010', 8, 0.6)
        cv.fill(cv.ellipse(160, 111, 9, 3), '#e0b030')
        cv.fill(cv.ellipse(160, 111, 4, 1.5), '#e02010')
        for x0 in (70, 120, 166, 214):                                       # the screens flash
            cv.fill(cv.rect(x0, 30, x0 + 34, 52) * 0.25, '#ffffff', 0.3)
    if lever:
        orig_box(cv, 'control', 280, 50, 310, 104)
        copy(cv, 250, 50, 280, 92, 280, 50)                                  # (wall where the lever was)
        cv.fill(cv.line([(292, 92), (304, 100)], 1.4), '#70d0a0')            # the lever, pulled down
        cv.fill(cv.ellipse(305, 100, 4, 3.5), '#a06020')
    return cv


def shipin():
    return base('shipin')


# ------------------------------------------------------------------ the title
def title():
    """the title room (32 colours): the top of the painted title screen (keyart.py);
    the game shows the painted screen itself in HAM over it"""
    from rooms import text_mask
    import keyart
    pic = keyart.cached('title', keyart.title_art)[:168]
    cv = base('road', 8)
    cv.c = np.repeat(np.repeat(pic, 2, 0), 2, 1).astype(np.float32)[:cv.h, :cv.w]
    if os.environ.get('WOS2_DEMO'):
        t4 = text_mask(cv, 160, 72, 'DEMO', 1.6, True)
        cv.fill(cv.blur(t4, 0.6), '#200a30', 0.9)
        cv.fill(t4, '#ff6060')
    t5 = text_mask(cv, 160, 156, 'Press a key   -   F5: menu', 1.0, True)
    cv.fill(cv.blur(t5, 0.6), '#100518', 0.9)
    cv.fill(t5, '#e0d0ff')
    return cv


ROOM_ART = {
    'road': road, 'garden': garden, 'shed': shed, 'well': well, 'porch': porch,
    'hall': hall, 'library': library, 'kitchen': kitchen, 'cellar': cellar, 'study': study, 'secret': secret,
    'stairs': stairs, 'bunker': bunker, 'lockers': lockers, 'hangar': hangar, 'control': control,
    'shipin': shipin, 'title': title,
}
import orig2  # noqa: E402,F401  (the rooms of the chapter disks 2-7)
