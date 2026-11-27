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


ROOM_ART.update({'cockpit': cockpit, 'galley': galley, 'engine': engine, 'cargo': cargo, 'airlock': airlock,
                 'stcorr': stcorr, 'maproom': maproom})
