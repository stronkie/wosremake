"""Inventory icons (32 x 24, the 16 panel colours) and the panel palette."""
import math
import numpy as np
from people import Pen

# panel colours
PANEL = ['#102', '#224', '#447', '#889', '#97d', '#fff', '#cdf', '#fe6',
         '#531', '#a73', '#fc3', '#d33', '#36c', '#8df', '#f8c', '#4c4']
BG, DARK, MID, GREY, VERB, WHITE, SENT, HI = range(8)
BROWN, LBROWN, GOLD, RED, BLUE, CYAN, PINK, GREEN = range(8, 16)


class IPen(Pen):
    def __init__(self):
        super().__init__(32, 24)
        self.ox, self.oy = 0, 0

    def finish(self, outline=True):
        out = super().finish(outline=False)
        if outline:
            body = out >= 0
            ring = np.zeros_like(body)
            ring[1:] |= body[:-1]
            ring[:-1] |= body[1:]
            ring[:, 1:] |= body[:, :-1]
            ring[:, :-1] |= body[:, 1:]
            out[ring & ~body] = DARK
        out[out < 0] = BG
        return out


def rope():
    P = IPen()
    for r, c in ((9, BROWN), (7, LBROWN), (5, BROWN), (3, LBROWN)):
        P.ellipse(16, 12, r * 1.3, r * 0.9, c)
    P.ellipse(16, 12, 1.5, 1, BG)
    P.limb(26, 13, 30, 20, 1.6, LBROWN)
    return P.finish()


def coin():
    P = IPen()
    P.ellipse(16, 12, 9, 9, GOLD)
    P.ellipse(16, 12, 7, 7, HI)
    P.ellipse(16, 10, 2.5, 2.5, GOLD)
    P.rect(13, 13, 19, 17, GOLD)
    P.ellipse(13, 9, 1.5, 2.5, WHITE)
    return P.finish()


def bucket(glow=False):
    P = IPen()
    P.poly([(8, 6), (24, 6), (22, 21), (10, 21)], GREY)
    P.poly([(10, 6), (13, 6), (12.5, 21), (10.5, 21)], WHITE)
    P.rect(8, 11, 24, 12.5, BROWN)
    P.rect(8, 17, 24, 18.5, BROWN)
    P.ellipse(16, 6, 8, 2.2, CYAN if glow else BLUE)
    if glow:
        P.ellipse(16, 6, 4, 1.2, HI)
        for x, y in ((6, 3), (27, 4), (4, 14), (28, 15)):
            P.dot(x, y, HI)
    P.limb(8, 6, 16, 1, 1, LBROWN)
    P.limb(16, 1, 24, 6, 1, LBROWN)
    return P.finish()


def chicken():
    P = IPen()
    P.ellipse(13, 15, 9, 6, HI)
    P.ellipse(23, 9, 4, 4, HI)
    P.poly([(26, 9), (31, 10), (26, 11.5)], GOLD)
    P.poly([(21, 5), (23, 2), (24, 5), (26, 3), (25.5, 6.5)], RED)
    P.dot(23.5, 8, DARK)
    P.limb(10, 20, 9, 23, 1, GOLD)
    P.limb(15, 20, 16, 23, 1, GOLD)
    P.ellipse(13, 13, 3, 3, GREY)                 # the pulley in the middle
    P.ellipse(13, 13, 1.2, 1.2, DARK)
    P.limb(13, 13, 13, 4, 0.8, GREY)
    return P.finish()


def crystal():
    P = IPen()
    P.poly([(16, 1), (22, 9), (19, 22), (13, 22), (10, 9)], CYAN)
    P.poly([(16, 1), (16, 22), (13, 22), (10, 9)], BLUE)
    P.poly([(16, 3), (19, 9), (16, 12)], WHITE)
    return P.finish()


def ribbon():
    P = IPen()
    P.poly([(16, 10), (4, 3), (6, 10), (3, 17)], PINK)
    P.poly([(16, 10), (28, 3), (26, 10), (29, 17)], CYAN)
    P.ellipse(16, 10, 3, 3, HI)
    P.poly([(14, 12), (10, 22), (13, 21), (15, 13)], PINK)
    P.poly([(18, 12), (22, 22), (19, 21), (17, 13)], CYAN)
    return P.finish()


def cake():
    P = IPen()
    P.poly([(4, 18), (28, 18), (26, 8), (6, 12)], LBROWN)
    P.poly([(6, 12), (26, 8), (24, 6), (8, 9)], PINK)
    P.rect(4, 17, 28, 20, BROWN)
    for x in (10, 16, 22):
        P.dot(x, 10, HI)
    P.ellipse(16, 4, 2, 2, GOLD)
    return P.finish()


def bunting():
    P = IPen()
    P.limb(1, 5, 31, 5, 0.8, BROWN)
    for i, c in enumerate((RED, GOLD, CYAN, GREEN, PINK)):
        x = 3 + i * 6
        P.poly([(x, 5), (x + 5, 5), (x + 2.5, 13 + (i % 2) * 2)], c)
    P.limb(1, 14, 31, 16, 0.8, BROWN)
    for i, c in enumerate((CYAN, PINK, GOLD, RED, GREEN)):
        x = 3 + i * 6
        P.poly([(x, 15), (x + 5, 15.5), (x + 2.5, 22)], c)
    return P.finish()


def lens():
    P = IPen()
    P.ellipse(16, 12, 12, 10, GOLD)
    P.ellipse(16, 12, 10, 8, CYAN)
    P.ellipse(13, 9, 4, 2.5, WHITE)
    P.ellipse(20, 15, 2, 1.5, SENT)
    return P.finish()


def floppy(label='STAR'):
    P = IPen()
    P.rect(7, 2, 25, 22, DARK)
    P.rect(8, 3, 24, 21, MID)
    P.rect(11, 3, 21, 9, GREY)
    P.rect(17, 4, 19, 8, MID)
    P.rect(10, 12, 22, 20, WHITE)
    P.rect(11, 14, 21, 15, RED)
    P.rect(11, 17, 18, 18, BLUE)
    return P.finish()


def printout():
    P = IPen()
    P.poly([(6, 3), (26, 3), (26, 21), (6, 21)], WHITE)
    for y in range(5, 21, 4):
        P.rect(8, y, 24, y + 1.5, GREEN)
    for y in range(4, 22, 3):
        P.dot(7, y, GREY)
        P.dot(25, y, GREY)
    P.rect(10, 9, 20, 10, DARK)
    P.rect(10, 13, 22, 14, DARK)
    return P.finish()


def pogo():
    P = IPen()
    P.limb(10, 22, 22, 2, 1.4, WHITE)
    P.limb(8, 9, 20, 13, 1.6, RED)
    P.ellipse(10, 22, 3, 1.5, DARK)
    P.limb(14, 16, 16, 12, 2.4, GREY)
    return P.finish()


def redcrystal():
    P = IPen()
    P.poly([(4, 14), (8, 10), (28, 12), (8, 18)], RED)
    P.poly([(8, 10), (28, 12), (10, 13)], PINK)
    return P.finish()


def handle(blade=False):
    P = IPen()
    P.ellipse(8, 12, 6, 6, RED)
    P.ellipse(8, 12, 2.5, 2.5, BG)
    P.rect(13, 10, 18, 14, RED)
    if blade:
        P.poly([(18, 9), (30, 11), (18, 15)], PINK)
        P.rect(23, 13, 25, 17, PINK)
    return P.finish()


def napkin():
    P = IPen()
    P.poly([(6, 4), (26, 4), (26, 20), (6, 20)], WHITE)
    P.poly([(26, 4), (26, 12), (18, 4)], GREY)
    P.rect(9, 9, 20, 10, BLUE)
    P.rect(9, 13, 23, 14, BLUE)
    return P.finish()


def chart():
    P = IPen()
    P.rect(4, 4, 28, 20, SENT)
    for x, y in ((8, 8), (14, 14), (20, 7), (25, 16), (11, 17)):
        P.dot(x, y, WHITE)
    P.limb(8, 8, 14, 14, 0.5, BLUE)
    P.limb(14, 14, 20, 7, 0.5, BLUE)
    P.ellipse(23, 16, 3.5, 3.5, RED)
    P.ellipse(23, 16, 2, 2, SENT)
    return P.finish()


def ration():
    P = IPen()
    P.rect(5, 8, 27, 18, GREY)
    P.rect(5, 8, 27, 10, MID)
    P.rect(10, 12, 22, 15, WHITE)
    return P.finish()


def songsheet():
    P = IPen()
    P.rect(6, 3, 26, 21, WHITE)
    for y in (7, 11, 15):
        P.limb(8, y, 24, y, 0.4, DARK)
    for x, y in ((11, 8), (15, 12), (19, 7), (22, 14)):
        P.ellipse(x, y, 1.4, 1.1, DARK)
        P.limb(x + 1.2, y, x + 1.2, y - 4, 0.4, DARK)
    return P.finish()


def mirror():
    P = IPen()
    P.ellipse(16, 9, 7, 8, GOLD)
    P.ellipse(16, 9, 5, 6, SENT)
    P.ellipse(14, 7, 2, 2.5, WHITE)
    P.limb(16, 17, 16, 23, 1.6, GOLD)
    return P.finish()


def uniform():
    P = IPen()
    P.poly([(6, 6), (12, 3), (20, 3), (26, 6), (24, 12), (22, 12), (22, 22), (10, 22), (10, 12), (8, 12)], MID)
    P.rect(15, 5, 17, 22, PINK)
    P.rect(11, 8, 14, 10, GOLD)
    return P.finish()


def keycard():
    P = IPen()
    P.rect(5, 6, 27, 19, WHITE)
    P.rect(5, 9, 27, 11, DARK)
    P.rect(8, 13, 14, 17, CYAN)
    P.rect(16, 14, 24, 15, GREY)
    return P.finish()


def moonheart():
    P = IPen()
    P.ellipse(16, 12, 9, 9, CYAN)
    P.ellipse(16, 12, 6, 6, SENT)
    P.ellipse(13, 9, 2.5, 2.5, WHITE)
    for x, y in ((4, 4), (28, 5), (3, 19), (29, 20)):
        P.dot(x, y, HI)
    return P.finish()


def hat():
    P = IPen()
    P.ellipse(16, 18, 13, 3, DARK)
    P.poly([(9, 18), (12, 6), (16, 3), (20, 6), (23, 18)], DARK)
    P.rect(10, 15, 22, 17, RED)
    return P.finish()


def sliver():
    P = IPen()
    P.poly([(12, 4), (20, 9), (18, 20), (11, 16)], SENT)
    P.poly([(12, 4), (20, 9), (15, 11)], WHITE)
    for x, y in ((6, 6), (25, 15), (8, 20)):
        P.dot(x, y, HI)
    return P.finish()


def ring():
    P = IPen()
    P.ellipse(16, 13, 9, 7, GOLD)
    P.ellipse(16, 13, 6, 4.5, BG)
    P.ellipse(16, 6, 4, 3.5, SENT)
    P.ellipse(15, 5, 1.5, 1.2, WHITE)
    return P.finish()


def watch():
    P = IPen()
    P.ellipse(16, 13, 8, 8, GOLD)
    P.ellipse(16, 13, 6, 6, WHITE)
    P.limb(16, 13, 16, 8, 0.8, DARK)
    P.limb(16, 13, 19, 14, 0.8, DARK)
    P.ellipse(16, 4, 2, 1.6, GOLD)
    P.limb(18, 4, 26, 2, 0.6, GOLD)
    return P.finish()


def smallcrystal():
    P = IPen()
    P.poly([(16, 6), (20, 11), (18, 20), (14, 20), (12, 11)], CYAN)
    P.poly([(16, 6), (16, 20), (14, 20), (12, 11)], BLUE)
    for x, y in ((8, 8), (24, 9), (7, 18), (25, 19)):
        P.dot(x, y, HI)
    return P.finish()


ICONS = {'rope': rope, 'coin': coin, 'bucket': bucket, 'starwater': lambda: bucket(True),
         'chicken': chicken, 'crystal': crystal, 'ribbon': ribbon,
         'cake': cake, 'bunting': bunting, 'lens': lens, 'floppy': floppy, 'printout': printout,
         'pogo': pogo, 'redcrystal': redcrystal, 'handle': handle, 'redkey': lambda: handle(True),
         'napkin': napkin, 'chart': chart, 'ration': ration, 'songsheet': songsheet, 'mirror': mirror,
         'uniform': uniform, 'keycard': keycard, 'moonheart': moonheart, 'hat': hat, 'sliver': sliver, 'ring': ring, 'watch': watch, 'smallcrystal': smallcrystal}


# ---------------------------------------------------------------- World of Stronkie remake
def shovel():
    P = IPen()
    P.limb(6, 4, 19, 15, 1.6, LBROWN)
    P.rect(4, 2, 9, 4, BROWN)
    P.poly([(17, 13), (25, 15), (28, 22), (22, 23), (15, 18)], GREY)
    P.poly([(17, 13), (22, 14), (19, 18), (15, 18)], WHITE)
    return P.finish()


def crank():
    P = IPen()
    P.limb(8, 18, 8, 7, 2.0, GREY)
    P.limb(8, 7, 22, 7, 2.0, GREY)
    P.limb(22, 7, 22, 15, 2.0, GREY)
    P.rect(19, 15, 25, 20, MID)
    P.rect(6, 17, 10, 22, BROWN)
    return P.finish()


def brasskey():
    P = IPen()
    P.ellipse(9, 12, 6, 6, GOLD)
    P.ellipse(9, 12, 2.5, 2.5, BG)
    P.poly([(5, 6), (9, 3), (12, 6)], GOLD)              # the raven's head
    P.rect(14, 11, 28, 13, GOLD)
    P.rect(23, 13, 25, 17, GOLD)
    P.rect(27, 13, 29, 16, GOLD)
    P.dot(8, 4, DARK)
    return P.finish()


def paper():
    P = IPen()
    P.poly([(7, 5), (24, 4), (26, 20), (9, 21), (6, 13)], SENT)
    for y in (8, 11, 14, 17):
        P.rect(10, y, 22, y, GREY)
    return P.finish()


def candle(lit=False):
    P = IPen()
    P.rect(13, 9, 19, 22, WHITE)
    P.rect(13, 9, 14, 22, SENT)
    P.ellipse(16, 22, 7, 2, GREY)
    P.rect(15, 6, 16, 9, DARK)
    if lit:
        P.ellipse(16, 4, 2.2, 3.5, GOLD)
        P.ellipse(16, 5, 1, 1.8, HI)
    return P.finish()


def matches():
    P = IPen()
    P.rect(6, 8, 26, 19, RED)
    P.rect(6, 8, 26, 10, GOLD)
    P.rect(10, 12, 22, 16, SENT)
    P.limb(20, 4, 27, 1, 0.8, LBROWN)
    P.ellipse(27, 1.5, 1.2, 1.2, RED)
    return P.finish()


def knife():
    P = IPen()
    P.poly([(4, 15), (20, 10), (22, 12), (6, 17)], SENT)
    P.poly([(4, 15), (20, 10), (20, 11)], WHITE)
    P.limb(21, 11, 28, 9, 2.2, BROWN)
    return P.finish()


def silverkey():
    P = IPen()
    P.ellipse(10, 12, 5, 5, SENT)
    P.ellipse(10, 12, 2, 2, BG)
    P.rect(14, 11, 27, 13, SENT)
    P.rect(22, 13, 24, 16, SENT)
    P.rect(25, 13, 27, 15, SENT)
    P.dot(9, 9, WHITE)
    return P.finish()


def amulet():
    P = IPen()
    P.limb(8, 3, 16, 9, 0.8, GOLD)
    P.limb(24, 3, 16, 9, 0.8, GOLD)
    P.ellipse(16, 15, 8, 7, GOLD)
    P.ellipse(16, 15, 5, 4.5, RED)
    P.ellipse(14, 13, 1.5, 1.2, PINK)
    for x, y in ((4, 18), (28, 17)):
        P.dot(x, y, HI)
    return P.finish()


def suit():
    P = IPen()
    P.ellipse(16, 6, 5, 5, SENT)
    P.ellipse(16, 6, 3, 2.5, BLUE)
    P.rect(9, 11, 23, 22, SENT)
    P.rect(5, 12, 9, 20, GREY)
    P.rect(23, 12, 27, 20, GREY)
    P.rect(13, 13, 19, 16, RED)
    return P.finish()


def fragment():
    P = IPen()
    P.poly([(16, 2), (19, 10), (28, 11), (21, 16), (23, 24), (16, 19), (9, 24), (11, 16), (4, 11), (13, 10)], HI)
    P.poly([(16, 2), (19, 10), (16, 12), (13, 10)], WHITE)
    return P.finish()


ICONS.update({'shovel': shovel, 'crank': crank, 'brasskey': brasskey, 'paper': paper, 'candle': candle,
              'litcandle': lambda: candle(True), 'matches': matches, 'knife': knife, 'silverkey': silverkey,
              'amulet': amulet, 'suit': suit, 'fragment': fragment})
import icons2  # noqa: E402,F401  (the icons of the chapter disks 2-7)
