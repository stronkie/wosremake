"""World of Stronkie remake - the rooms, things, people,
conversations and scripts of one chapter.

The chapter comes from the environment (WOS2_CHAPTER, 1-5): this file has the
pieces every chapter uses, chapters/chN.py the story. A line of text that
starts with '*' is spoken (key lines only)."""
import os
from wosdata import Script, Strings, V, RIGHT, LEFT, FRONT, BACK

CH = int(os.environ.get('WOS2_CHAPTER', '1'))
DEMO = bool(os.environ.get('WOS2_DEMO'))
START_ACTORS = {}          # actor -> (room, x, y, dir) at the start
VARIANTS = {}              # object picture -> (room art, base kwargs, variant kwargs)
DEV_SPOTS = []
DEV_ITEMS = []
BLOCK = {}
EXTRA_SPEECH = {}       # spoken text -> the original's speech sample (orig/sound/NAME.spk)


class Game:
    def __init__(self):
        self.strings = Strings()
        self.flags = {}
        self.objects = {}            # name -> dict
        self.obj_order = [None]      # 0 = nothing
        self.rooms = {}
        self.room_order = []
        self.scripts = []
        self.actors = [a[0] for a in ACTORS]
        self.specials = SPECIALS                           # costume -> special animations

    # ---- names -> numbers
    def act(self, a):
        return self.actors.index(a) if isinstance(a, str) else a

    def obj(self, o):
        return self.obj_order.index(o)

    def flag(self, f):
        if f not in self.flags:
            self.flags[f] = len(self.flags) + 1
            assert self.flags[f] < 256
        return self.flags[f]

    def room_no(self, r):
        return 0 if r is None else self.room_order.index(r) + 1

    def sound_no(self, s):
        return SOUNDS.index(s) + 1

    def song_no(self, s):
        return SONGS.index(s) + 1

    def special_no(self, a, spec):
        cost = ACTORS[self.act(a)][1]
        return self.specials[cost].index(spec)

    def voice_of(self, a):
        return self.actors[self.act(a)]

    # ---- building
    def script(self, name=None):
        s = Script(self, name)
        self.scripts.append(s)
        return s

    def thing(self, name, room, box=None, walk=None, face=FRONT, verb='look', label=None, actor=None,
              image=None, state=1, icon=None):
        """a thing in a room (room None: something you carry)"""
        self.objects[name] = dict(name=name, label=label or name, room=room, box=box, walk=walk, face=face,
                                  verb=V[verb], actor=actor, image=image, state=state, icon=icon, handlers=[])
        self.obj_order.append(name)
        if room:
            self.rooms[room]['objects'].append(name)
        return name

    def on(self, obj, verb, script, other=None):
        self.objects[obj]['handlers'].append((V[verb], other, script))

    def room(self, name, art, walk=None, music=None, image_variants=None):
        self.rooms[name] = dict(name=name, art=art, walk=walk or [], music=music, objects=[], enter=None,
                                timer=None, ticks=0, random=None, rmin=0, rmax=0)
        self.room_order.append(name)





def say(s, *lines):
    for who, text in lines:
        s.say(who, text)
    return s


def simple(obj, verb, who, *texts):
    s = G.script()
    for t in texts:
        s.say(who, t)
    G.on(obj, verb, s)


def exit_to(obj, room, x, y, d):
    s = G.script()
    s.room(room, x, y, d)
    G.on(obj, 'walk', s)
    G.on(obj, 'open', s)



def default_answers():
    """the answers for each verb when nothing else fits"""
    for verb, lines in DEFAULTS.items():
        s = G.script(f'def_{verb}')
        s.randsay('pilot', lines)


DEFAULTS = {
    'walk': ['I\'d rather not.'],
    'give': ['I don\'t think they want that.', 'I\'d better keep it.'],
    'pickup': ['I can\'t pick that up.', 'It\'s not mine to take.', 'Why would I want that?'],
    'use': ['That doesn\'t work.', 'I can\'t use that.', 'Hmm. No.',
            'A hollow voice says: wrong game. This isn\'t Colossal Cave.'],
    'open': ['It doesn\'t open.', 'I can\'t open that.'],
    'look': ['Nothing special.', 'It looks like it\'s supposed to look.'],
    'push': ['It won\'t budge.', 'Pushing it won\'t help.'],
    'close': ['It doesn\'t close.', 'I can\'t close that.'],
    'talk': ['It doesn\'t say much.', 'I\'d rather talk to people.',
             'I wave my hand. These aren\'t the droids... the commands I\'m looking for.'],
    'pull': ['It won\'t budge.', 'Pulling it won\'t help.'],
}

CH_NAMES = {1: 'Chapter One', 2: 'Chapter Two', 3: 'Chapter Three', 4: 'Chapter Four', 5: 'Chapter Five',
            6: 'Chapter Six', 7: 'Chapter Seven'}

import story as _story                           # noqa: E402
KEEP_INFO = {   # keepsake: (label, icon, look text)
    'paper': ('scrap of paper', 'paper', 'It reads: "I buried the winch handle so they cannot raise the key. - E." I keep it for luck.'),
    'ration': ('space ration', 'ration', 'A grey bar wrapped in foil. My lucky ration. I will never eat it.'),
    'chicken': ('rubber chicken', 'chicken', 'A rubber chicken with a pulley in the middle. Everybody needs one. I am never letting go of it.'),
    'shell': ('sea shell', 'shell', 'A spiral shell. If I hold it to my ear I hear an ocean on a world far away.'),
    'medal': ('bronze medal', 'medal', 'A bronze medal. I earned this one.'),
    'compass': ('star compass', 'compass', 'A little compass. Its needle always points to Stronkie.'),
}


def keepsakes():
    """the keepsakes of this disk and all disks before it: things the player carries"""
    for n in range(1, CH + 1):
        k = _story.KEEPSAKES.get(n)
        if not k or k in G.objects:
            continue
        lab, icon, txt = KEEP_INFO[k]
        G.thing(k, None, label=lab, icon=icon)
        s = G.script()
        s.say('pilot', txt)
        G.on(k, 'look', s)


def story_start(s):
    """the start of a chapter (disk): read the story of the last chapter (this drawer,
    or the last chapter's disk), then the item check list: every keepsake of every
    disk before this one must be in the inventory. Dev mode skips all of this."""
    prev, this = CH_NAMES[CH - 1], CH_NAMES[CH]
    ok, ask, back, again, volchk, go, stuck = (s.label() for _ in range(7))
    s.storyload(0, 'story_ok')
    s.iff('story_ok', ok)
    s.here(ask)
    s.cutoff()
    s.card(f'Your story from {prev} is not on this disk. Put the {prev} disk in the drive.', wait=False)
    s.dialog([(f'The {prev} disk is in. Read my story.', again, None)])
    s.here(again)
    s.storyload(1, 'story_ok')
    s.iff('story_ok', back)
    s.card(f'There is no story on that disk. Play {prev} to the end: the end writes your story.', wait=True)
    s.jmp(ask)
    s.here(back)
    s.card(f'Your story is read! Now put the {this} disk back in.', wait=False)
    s.dialog([(f'The {this} disk is back in.', volchk, None)])
    s.here(volchk)
    s.storyvol('story_vol')
    s.iff('story_vol', ok)
    s.card(f'That is not the {this} disk.', wait=True)
    s.jmp(back)
    s.here(ok)
    miss = []
    for n in range(1, CH):
        k = _story.KEEPSAKES[n]
        L = s.label()
        miss.append((L, n, k))
        s.nothas(k, L)
    s.cuton()
    s.card(f'Item check OK. Your story from {prev} continues...', wait=True)
    s.jmp(go)
    for L, n, k in miss:
        s.here(L)
        s.cutoff()
        s.card(f'ITEM CHECK FAILED! The {KEEP_INFO[k][0]} from {CH_NAMES[n]} is not in your inventory. '
               f'This story cannot go on.', wait=True)
        s.jmp(stuck)
    s.here(stuck)
    s.wait(50)
    s.jmp(stuck)
    s.here(go)
    return s


def story_end(s):
    """the end of a chapter: write the story for the next chapter"""
    nxt = CH_NAMES.get(CH + 1)
    if not nxt:
        return s
    ok, ask, skip = s.label(), s.label(), s.label()
    s.here(ask)
    s.storysave('story_saved')
    s.iff('story_saved', ok)
    s.cutoff()
    s.card('I could not write your story to the disk. Is it write-protected?', wait=False)
    s.dialog([('I fixed it. Try again.', ask, None), (f'Go on without it ({nxt} will not start without your story).', skip, None)])
    s.here(ok)
    s.cuton()
    s.card(f'Your story is saved. {nxt} will continue it.', wait=True)
    s.here(skip)
    s.cuton()
    return s


import story                                     # noqa: E402
_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', f'ch{CH}.py')
exec(compile(open(_f).read(), _f, 'exec'), globals())
for _n in story.FLAGS:
    G.flag(_n)
