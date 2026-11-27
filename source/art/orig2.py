"""The rooms of the chapter disks 2-7: the original pictures, with the things
the remake needs painted over them (see orig.py)."""
import os
import numpy as np
from orig import base, copy, orig_box, dark_door, ORIG, ROOM_ART


def _plain(name):
    return lambda: base(name)


for _f in sorted(os.listdir(ORIG)):
    if _f.endswith('.png') and _f[:-4] not in ROOM_ART:
        ROOM_ART[_f[:-4]] = _plain(_f[:-4])


def robot(cv, x, y, on=True):
    """a tall security robot standing at x (centre), feet at y"""
    body = cv.rect(x - 14, y - 52, x + 14, y - 14)
    cv.fill(body, cv.lgrad((x - 14, 0), (x + 14, 0), '#9aa4b4', '#4a5260'))
    cv.bevel(body, 2, 0.6)
    head = cv.ellipse(x, y - 60, 11, 9)
    cv.fill(head, cv.lgrad((x - 11, 0), (x + 11, 0), '#aab4c4', '#545c6a'))
    cv.bevel(head, 1.5, 0.6)
    eye = cv.ellipse(x, y - 61, 4, 3)
    cv.fill(eye, '#ff2020' if on else '#301010')
    if on:
        cv.glow(eye, '#ff3030', 5, 0.8)
    for dx in (-17, 17):
        arm = cv.rect(x + dx - 3, y - 50, x + dx + 3, y - 22)
        cv.fill(arm, '#6a7282')
        cv.bevel(arm, 1, 0.5)
    base_ = cv.rect(x - 16, y - 14, x + 16, y)
    cv.fill(base_, '#30343c')
    cv.fill(cv.rect(x - 16, y - 4, x + 16, y), '#e0b000')
    cv.fill(cv.rect(x - 7, y - 44, x + 7, y - 36), '#202428')
    cv.fill(cv.rect(x - 5, y - 43, x + 5, y - 37), '#e0e0e0' if on else '#707070')   # 001


def amulet_on_console(cv, x, y):
    cv.fill(cv.ellipse(x, y, 6, 4), '#c8a020')
    cv.fill(cv.ellipse(x, y, 3, 2.2), '#ff3020')
    cv.glow(cv.ellipse(x, y, 3, 2.2), '#ff4030', 6, 0.7)


# ------------------------------------------------------------- disk 2: Into Space, the Derelict Station
def cockpit():
    cv = base('cockpit')
    amulet_on_console(cv, 160, 108)
    lever = cv.line([(212, 150), (206, 122)], 3)          # the hyperdrive throttle
    cv.fill(lever, '#9098a8')
    cv.bevel(lever, 1, 0.6)
    cv.fill(cv.ellipse(206, 121, 4, 4), '#e03020')
    cv.fill(cv.rect(200, 148, 222, 154), '#2a3038')
    return cv


def galley(ration=False):
    cv = base('galley')
    if ration:
        r = cv.rect(208, 75, 224, 80)
        cv.fill(r, '#9aa0aa')
        cv.fill(cv.rect(208, 75, 224, 76.5), '#d8dce4')
    return cv


def engine(crowbar=False):
    cv = base('engine')
    if crowbar:
        bar = cv.line([(226, 88), (232, 50)], 2.4)
        cv.fill(bar, '#d02818')
        cv.fill(cv.line([(232, 50), (236, 47)], 2.2), '#d02818')
    return cv


def cargo(open_=False, crystal=False):
    cv = base('cargo')
    if open_:
        lid = cv.poly([(112, 96), (208, 96), (204, 106), (116, 106)])
        cv.fill(lid, '#140c06')
        cv.fill(cv.poly([(108, 94), (210, 94), (230, 76), (128, 76)]), '#8a5a2a')     # the lid, open
        cv.bevel(cv.poly([(108, 94), (210, 94), (230, 76), (128, 76)]), 1.5, 0.6)
        if crystal:
            c = cv.poly([(158, 92), (164, 98), (161, 106), (155, 106), (152, 98)])
            cv.fill(c, '#40b0ff')
            cv.glow(c, '#60c0ff', 6, 0.8)
    return cv


def airlock(boots=False):
    cv = base('airlock')
    if boots:
        for x in (258, 274):
            b = cv.rect(x, 92, x + 10, 108)
            cv.fill(b, '#505868')
            cv.fill(cv.rect(x - 1, 106, x + 12, 110), '#8a92a2')
    return cv


def stcorr(robot_on=False, robot_off=False):
    cv = base('stcorr')
    if robot_on:
        robot(cv, 236, 140, True)
    if robot_off:
        robot(cv, 280, 124, False)
    return cv


def maproom(chart=False):
    cv = base('maproom')
    if chart:
        d = cv.ellipse(132, 116, 8, 2.5)
        cv.fill(d, '#a0e8ff')
        cv.glow(d, '#80d0ff', 4, 0.6)
    return cv


# ------------------------------------------------------------- disk 3: Asteroid 42, Space Pirates
def bar(napkin=False):
    cv = base('bar')
    if napkin:
        n = cv.poly([(196, 125), (210, 123), (214, 128), (199, 130)])
        cv.fill(n, '#e8e4d8')
        cv.fill(cv.line([(200, 126), (208, 125)], 0.6), '#5060c0')
    return cv


def stan(chicken=False):
    cv = base('stan')
    if chicken:
        b = cv.ellipse(86, 88, 9, 4)
        cv.fill(b, '#f0c020')
        cv.fill(cv.ellipse(96, 84, 3, 3), '#f0c020')
        cv.fill(cv.poly([(98, 83), (102, 84), (98, 85)]), '#d07010')
        cv.fill(cv.ellipse(86, 88, 2, 2), '#909090')
    return cv


def deck():
    cv = base('deck')
    # the green space parrot on the rail
    body = cv.ellipse(56, 92, 5, 8)
    cv.fill(body, '#30c040')
    cv.fill(cv.ellipse(58, 82, 4, 4), '#40d050')
    cv.fill(cv.poly([(61, 81), (65, 83), (61, 85)]), '#f0c020')
    cv.fill(cv.ellipse(59, 81, 1, 1), '#000000')
    cv.fill(cv.poly([(52, 96), (48, 106), (54, 100)]), '#2080e0')
    return cv


def pengine(ricky_gone=False):
    cv = base('pengine')
    if ricky_gone:
        copy(cv, 0, 96, 34, 168, 262, 96)
    return cv


ROOM_ART.update({'bar': bar, 'stan': stan, 'deck': deck, 'pengine': pengine})
# ------------------------------------------------------------- disk 4: Landfall, the Village
def wreck(extinguisher=False):
    cv = base('wreck')
    if extinguisher:
        b = cv.rect(26, 120, 38, 152)
        cv.fill(b, cv.lgrad((26, 0), (38, 0), '#ff4030', '#901810'))
        cv.fill(cv.rect(29, 114, 35, 120), '#202020')
        cv.fill(cv.line([(35, 116), (42, 124)], 1.5), '#202020')
        cv.fill(cv.rect(27, 132, 37, 138), '#f0f0f0')
    return cv


def crash(fire_out=False):
    cv = base('crash')
    if fire_out:
        copy(cv, 0, 80, 56, 148, 218, 80)
        copy(cv, 290, 80, 319, 148, 262, 80)
        for x, y in ((236, 132), (252, 126), (264, 136)):          # the white foam
            cv.fill(cv.ellipse(x, y, 10, 5), '#f4f4ff')
    return cv


def jungle(fruit=True, monkey=False):
    cv = base('jungle')
    if not fruit:
        for dx in (158, 170, 182):
            copy(cv, 138, 61, 150, 80, dx, 61)
    if monkey:
        m = cv.ellipse(96, 132, 5, 6)
        cv.fill(m, '#8a5a2a')
        cv.fill(cv.ellipse(96, 124, 4, 4), '#9a6a3a')
        cv.fill(cv.ellipse(96, 125, 2.5, 2), '#d8b080')
        cv.fill(cv.ellipse(91, 123, 1.5, 1.5), '#9a6a3a')
        cv.fill(cv.ellipse(101, 123, 1.5, 1.5), '#9a6a3a')
    return cv


def market(glasses=False):
    cv = base('market')
    if glasses:
        for x in (252, 262):
            cv.fill(cv.ellipse(x, 72, 4, 3), '#202020')
            cv.fill(cv.ellipse(x, 72, 2.5, 1.8), '#a0c0e0')
        cv.fill(cv.poly([(255, 73), (259, 73), (258, 80), (256, 80)]), '#f0b090')
        cv.fill(cv.rect(252, 80, 262, 82), '#302010')
    return cv


def tower(banner=True):
    cv = base('tower')
    if not banner:
        copy(cv, 4, 4, 48, 46, 57, 4)
        copy(cv, 4, 4, 30, 46, 96, 4)
    return cv


ROOM_ART.update({'wreck': wreck, 'crash': crash, 'jungle': jungle, 'market': market, 'tower': tower})
# ------------------------------------------------------------- disk 5: the Crystal Mountains, the Sky Temple
def icecave(boots=False):
    cv = base('icecave')
    if boots:
        for x in (66, 78):
            cv.fill(cv.rect(x, 140, x + 8, 154), '#5a3a20')
            cv.fill(cv.rect(x - 1, 152, x + 11, 156), '#909090')
            for k in range(4):
                cv.fill(cv.rect(x + k * 3, 156, x + k * 3 + 1, 158), '#d0d0d0')
    return cv


def soldier(cv, x, y):
    cv.fill(cv.rect(x - 5, y - 26, x + 5, y - 8), '#141418')
    cv.fill(cv.ellipse(x, y - 30, 4.5, 5), '#1c1c22')
    cv.fill(cv.rect(x - 2, y - 31, x + 2, y - 29), '#c03020')
    cv.fill(cv.rect(x - 5, y - 8, x - 1, y), '#101014')
    cv.fill(cv.rect(x + 1, y - 8, x + 5, y), '#101014')
    cv.fill(cv.line([(x + 5, y - 20), (x + 12, y - 26)], 1.5), '#606870')


def camp(soldiers=False):
    cv = base('camp')
    if soldiers:
        soldier(cv, 188, 128)
        soldier(cv, 236, 128)
    return cv


def tent(amulet=False):
    cv = base('tent')
    if amulet:
        amulet_on_console(cv, 136, 112)
    return cv


def statues(mirror=True):
    cv = base('statues')
    if not mirror:
        m = cv.ellipse(238, 93, 11, 15)
        cv.fill(m, '#44444e')
        cv.fill(cv.ellipse(235, 88, 5, 6), '#55555f')
    return cv


def mirrors(mirror=False):
    cv = base('mirrors')
    if mirror:
        ring = cv.ellipse(160, 108, 9, 10)
        cv.fill(ring, '#d0a030')
        cv.fill(cv.ellipse(160, 108, 7, 8), '#e8eef8')
        cv.glow(cv.ellipse(160, 108, 7, 8), '#ffffff', 8, 0.6)
    return cv


def starbridge(bridge=False):
    cv = base('starbridge')
    if bridge:
        for k in range(40):
            t = k / 39
            x, y = 104 + t * 150, 138 - t * 46
            cv.fill(cv.ellipse(x, y, 4, 2), '#f0d060')
            cv.glow(cv.ellipse(x, y, 2, 1), '#fff0a0', 3, 0.5)
    return cv


ROOM_ART.update({'icecave': icecave, 'camp': camp, 'tent': tent, 'statues': statues, 'mirrors': mirrors,
                 'starbridge': starbridge})
# ------------------------------------------------------------- disk 6: the Star Heart, Repairs
def heart(machine=True):
    cv = base('heart')
    if machine:
        m = cv.rect(214, 92, 244, 120)
        cv.fill(m, cv.lgrad((214, 0), (244, 0), '#2a2a34', '#0c0c10'))
        cv.bevel(m, 1.5, 0.6)
        for k, c in enumerate(('#ff3030', '#30ff60', '#ffc020')):
            cv.fill(cv.ellipse(220 + k * 9, 98, 1.6, 1.6), c)
        cv.fill(cv.line([(244, 116), (300, 150), (319, 152)], 2.5), '#101014')
        cv.fill(cv.line([(214, 110), (184, 90)], 2), '#101014')
    return cv


def westgal(horn=False):
    cv = base('westgal')
    if horn:
        h = cv.poly([(220, 132), (246, 124), (252, 116), (256, 126), (248, 132), (222, 138)])
        cv.fill(h, '#d8dce8')
        cv.fill(cv.ellipse(252, 121, 4, 6), '#a0a8b8')
        cv.fill(cv.line([(222, 136), (246, 128)], 0.8), '#ffffff')
    return cv


def eastgal(soldier_=False):
    cv = base('eastgal')
    if soldier_:
        soldier(cv, 228, 128)
        cv.fill(cv.ellipse(228, 97, 7, 5), '#1c1c22')         # a big helmet
    return cv


def catacomb(bars=False):
    cv = base('catacomb')
    if bars:
        for x in range(252, 282, 6):
            b = cv.rect(x, 46, x + 3, 136)
            cv.fill(b, '#80d0f0')
            cv.glow(b, '#a0e8ff', 3, 0.4)
    return cv


def workshop(hammer=False):
    cv = base('workshop')
    if hammer:
        cv.fill(cv.line([(48, 118), (72, 112)], 2), '#8a5a2a')
        cv.fill(cv.rect(70, 106, 80, 116), '#a0b0c0')
    return cv


def mineentry(kite=True, pip=True):
    cv = base('mineentry')
    if not kite:
        copy(cv, 60, 8, 84, 40, 96, 8)
    if not pip:
        copy(cv, 156, 116, 184, 160, 126, 116)
    return cv


def maze3():
    cv = base('maze')
    hole = cv.ellipse(160, 150, 24, 7)
    cv.fill(hole, '#020204')
    cv.fill(cv.ellipse(160, 150, 27, 9) * (1 - hole), '#3a4a60')
    return cv


ROOM_ART.update({'heart': heart, 'westgal': westgal, 'eastgal': eastgal, 'catacomb': catacomb, 'workshop': workshop,
                 'mineentry': mineentry, 'maze3': maze3})
ROOM_ART.update({'cockpit': cockpit, 'galley': galley, 'engine': engine, 'cargo': cargo, 'airlock': airlock,
                 'stcorr': stcorr, 'maproom': maproom})
