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


ICONS.update({'ration': ration, 'crowbar': crowbar, 'crystal': crystal, 'boots': boots, 'disc': disc,
              'feather': feather, 'shell': shell, 'medal': medal, 'compass': compass})
