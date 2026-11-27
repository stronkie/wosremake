"""Inventory icons of the chapter disks 2-7 (32 x 24, the 16 panel colours)."""
from icons import IPen, ICONS, BG, DARK, MID, GREY, VERB, WHITE, SENT, HI, BROWN, LBROWN, GOLD, RED, BLUE, CYAN, PINK, GREEN


def ration():
    P = IPen()
    P.poly([(5, 9), (26, 6), (28, 14), (7, 17)], GREY)
    P.poly([(5, 9), (26, 6), (26, 9), (6, 12)], SENT)
    P.rect(13, 7, 15, 16, MID)
    return P.finish()


def crowbar():
    P = IPen()
    P.limb(6, 20, 25, 5, 2.4, RED)
    P.limb(25, 5, 29, 8, 2.2, RED)
    P.limb(6, 20, 3, 18, 2.2, RED)
    return P.finish()


def crystal(col=CYAN, hi=WHITE):
    P = IPen()
    P.poly([(16, 2), (23, 9), (19, 22), (13, 22), (9, 9)], col)
    P.poly([(16, 2), (18, 9), (16, 21), (13, 9)], hi)
    return P.finish()


def boots():
    P = IPen()
    for x in (4, 17):
        P.rect(x + 2, 4, x + 8, 16, MID)
        P.rect(x, 16, x + 11, 21, GREY)
        P.rect(x, 20, x + 11, 21, DARK)
        P.rect(x + 2, 6, x + 8, 7, GREY)
    return P.finish()


def disc():
    P = IPen()
    P.ellipse(16, 12, 10, 10, SENT)
    P.ellipse(16, 12, 9, 9, CYAN)
    P.ellipse(13, 9, 3, 2, WHITE)
    P.ellipse(16, 12, 2.5, 2.5, BG)
    return P.finish()


def feather():
    P = IPen()
    P.poly([(5, 21), (14, 9), (26, 2), (22, 12), (10, 19)], BLUE)
    P.poly([(14, 9), (26, 2), (17, 10)], CYAN)
    P.limb(4, 22, 22, 6, 0.8, WHITE)
    return P.finish()


def shell():
    P = IPen()
    P.ellipse(15, 12, 11, 9, PINK)
    P.ellipse(13, 11, 7, 6, SENT)
    P.ellipse(12, 11, 4, 3.5, PINK)
    P.ellipse(11, 11, 1.5, 1.5, BROWN)
    return P.finish()


def medal():
    P = IPen()
    P.poly([(10, 1), (15, 1), (17, 9), (13, 10)], RED)
    P.poly([(22, 1), (17, 1), (15, 9), (19, 10)], BLUE)
    P.ellipse(16, 15, 7, 7, LBROWN)
    P.ellipse(16, 15, 5, 5, GOLD)
    P.dot(15, 14, HI)
    return P.finish()


def compass():
    P = IPen()
    P.ellipse(16, 12, 10, 10, GOLD)
    P.ellipse(16, 12, 8, 8, SENT)
    P.poly([(16, 5), (18, 12), (16, 13), (14, 12)], RED)
    P.poly([(16, 19), (18, 12), (16, 11), (14, 12)], MID)
    return P.finish()


def burger():
    P = IPen()
    P.ellipse(16, 9, 11, 6, LBROWN)
    P.rect(5, 12, 27, 14, GREEN)
    P.rect(5, 14, 27, 16, BROWN)
    P.ellipse(16, 18, 11, 3, LBROWN)
    P.dot(12, 6, SENT)
    P.dot(19, 7, SENT)
    return P.finish()


def coin(n=1):
    P = IPen()
    for i in range(n):
        x, y = 16 - 4 * i, 13 - 3 * i
        P.ellipse(x, y, 7, 7, GOLD)
        P.ellipse(x, y, 5, 5, HI)
        P.rect(x - 1, y - 3, x + 1, y + 3, GOLD)
    return P.finish()


def napkin():
    P = IPen()
    P.poly([(5, 6), (26, 4), (27, 19), (6, 21)], WHITE)
    P.poly([(18, 12), (24, 10), (25, 16)], SENT)
    P.limb(8, 9, 18, 8, 0.6, BLUE)
    P.limb(8, 13, 16, 12, 0.6, BLUE)
    return P.finish()


def fuelcell():
    P = IPen()
    P.rect(10, 4, 22, 22, GREY)
    P.rect(12, 7, 20, 19, GREEN)
    P.rect(13, 8, 15, 18, HI)
    P.rect(13, 2, 19, 4, MID)
    return P.finish()


def chicken():
    P = IPen()
    P.ellipse(14, 14, 9, 6, GOLD)
    P.ellipse(23, 8, 4, 4, GOLD)
    P.poly([(27, 7), (31, 8), (27, 10)], LBROWN)
    P.poly([(22, 3), (24, 1), (25, 5)], RED)
    P.dot(23, 7, DARK)
    P.limb(10, 19, 9, 23, 0.8, LBROWN)
    P.limb(16, 19, 17, 23, 0.8, LBROWN)
    P.ellipse(14, 14, 2.5, 2.5, GREY)
    P.ellipse(14, 14, 1, 1, DARK)
    return P.finish()


def extinguisher():
    P = IPen()
    P.rect(11, 6, 19, 22, RED)
    P.rect(12, 7, 13, 21, PINK)
    P.rect(13, 2, 17, 6, DARK)
    P.limb(17, 3, 25, 6, 1.0, DARK)
    P.rect(11, 12, 19, 15, WHITE)
    return P.finish()


def fruit():
    P = IPen()
    P.ellipse(16, 14, 8, 8, BLUE)
    P.ellipse(13, 11, 3, 3, CYAN)
    P.limb(16, 6, 18, 2, 0.8, BROWN)
    P.ellipse(21, 4, 3, 1.5, GREEN)
    return P.finish()


def monkey():
    P = IPen()
    P.ellipse(16, 17, 6, 6, BROWN)
    P.ellipse(16, 8, 6, 5, LBROWN)
    P.ellipse(16, 9, 3.5, 2.5, SENT)
    P.ellipse(9, 7, 2.5, 2.5, LBROWN)
    P.ellipse(23, 7, 2.5, 2.5, LBROWN)
    P.dot(14, 7, DARK)
    P.dot(18, 7, DARK)
    P.limb(21, 20, 27, 14, 1.0, BROWN)
    return P.finish()


def scroll_map():
    P = IPen()
    P.poly([(4, 5), (28, 4), (28, 20), (4, 21)], SENT)
    P.poly([(8, 18), (14, 9), (19, 16), (23, 8), (27, 18)], GREY)
    P.poly([(14, 9), (16, 12), (12, 12)], WHITE)
    P.limb(6, 19, 26, 12, 0.6, RED)
    return P.finish()


def banner():
    P = IPen()
    P.poly([(4, 4), (28, 6), (26, 14), (28, 20), (4, 19)], PINK)
    P.poly([(4, 4), (28, 6), (27, 9), (4, 8)], RED)
    return P.finish()


def glider():
    P = IPen()
    P.poly([(2, 12), (16, 6), (30, 12), (16, 10)], PINK)
    P.limb(16, 8, 16, 20, 1.0, LBROWN)
    P.limb(8, 18, 24, 18, 1.0, LBROWN)
    return P.finish()


def glasses():
    P = IPen()
    P.ellipse(10, 9, 5, 4, DARK)
    P.ellipse(22, 9, 5, 4, DARK)
    P.ellipse(10, 9, 3.5, 2.5, CYAN)
    P.ellipse(22, 9, 3.5, 2.5, CYAN)
    P.poly([(14, 10), (18, 10), (19, 17), (13, 17)], PINK)
    P.rect(9, 18, 23, 20, BROWN)
    return P.finish()


def snowball():
    P = IPen()
    P.ellipse(16, 12, 8, 8, WHITE)
    P.ellipse(13, 9, 3, 3, SENT)
    P.ellipse(19, 15, 3, 2, GREY)
    return P.finish()


def spikes():
    P = IPen()
    for x in (4, 17):
        P.rect(x + 2, 4, x + 8, 15, BROWN)
        P.rect(x, 15, x + 11, 19, LBROWN)
        for k in range(4):
            P.rect(x + k * 3, 19, x + k * 3 + 1, 22, WHITE)
    return P.finish()


def stardust():
    P = IPen()
    P.ellipse(16, 15, 9, 6, GREY)
    for x, y in ((12, 13), (17, 11), (21, 15), (14, 17), (19, 18), (16, 14)):
        P.dot(x, y, HI)
    P.dot(9, 8, GOLD)
    P.dot(24, 6, GOLD)
    return P.finish()


ICONS.update({'snowball': snowball, 'spikes': spikes, 'stardust': stardust})
ICONS.update({'extinguisher': extinguisher, 'fruit': fruit, 'monkey': monkey, 'map': scroll_map, 'banner': banner,
              'glider': glider, 'glasses': glasses, 'powercrystal': lambda: crystal(PINK, WHITE)})
ICONS.update({'burger': burger, 'coin': coin, 'cash': lambda: coin(3), 'napkin': napkin, 'fuelcell': fuelcell,
              'chicken': chicken, 'ration': ration, 'crowbar': crowbar, 'crystal': crystal, 'boots': boots, 'disc': disc,
              'feather': feather, 'shell': shell, 'medal': medal, 'compass': compass})
