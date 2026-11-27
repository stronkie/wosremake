"""World of Stronkie remake - the pieces every chapter disk after the first uses.

Exec'd at the top of chapters/ch2.py .. ch7.py (in the namespace of game.py)."""
# ---------------------------------------------------------------- the people
ACTORS = [   # name, costume, talk colour (fixed palette), voice
    ('pilot', 'pilot', 17, ('rms', 1.0)),
    ('narrator', None, 30, ('rms', 0.95)),
    ('nova', None, 24, ('slt', 1.0)),          # NOVA has no body: a calm voice everywhere on the ship
]
EXTRA_COSTUMES = []
SOUNDS = ['pickup', 'door', 'thunder', 'zap', 'launch', 'score', 'drop', 'error', 'beep', 'hyper', 'click']
SPECIALS = {'pilot': ['reach', 'reachl'], 'suit': ['reach', 'reachl']}


def add_actor(name, colour, voice=('rms', 1.0)):
    """a person with no sprite: they are painted in the picture and talk at the top"""
    ACTORS.append((name, None, colour, voice))
    G.actors.append(name)


G = Game()
FLOOR = lambda y: [(0, y), (319, y), (319, 167), (0, 167)]          # noqa: E731
ROOM3D = lambda y0, x0=40: [(x0, y0), (319 - x0, y0), (319, 167), (0, 167)]   # noqa: E731
G.room('title', 'title', music='title')
G.room('cards', 'black')


def nova(s, text, sample=None, wait=True):
    """NOVA speaks; with the original's speech sample when it had one"""
    if sample:
        EXTRA_SPEECH[text] = sample
        text = '*' + text
    s.say('nova', text, wait=wait)
    return s


def spoken_card(s, text, sample):
    EXTRA_SPEECH[text] = sample
    s.card('*' + text, wait=True)
    return s


def hot(name, room, box, walk=None, face=BACK, verb='look', label=None, look=None, image=None, state=1):
    """a thing in a room; look = what the pilot says when looking at it"""
    G.thing(name, room, box, walk, face, verb, label=label, image=image, state=state)
    if look:
        simple(name, 'look', 'pilot', *([look] if isinstance(look, str) else look))
    return name


def door(name, room, box, walk, face, label, to, look=None, locked=None):
    """an exit: walk/open goes to the room 'to' = (room, x, y, dir);
    locked = (flag, line): only when the flag is set, else the pilot says the line"""
    G.thing(name, room, box, walk, face, 'walk', label=label)
    s = G.script()
    if locked:
        L = s.label()
        flag, line = locked
        s.iff(flag, L)
        s.say('pilot', line) if isinstance(line, str) else line(s)
        s.end()
        s.here(L)
    s.room(*to)
    G.on(name, 'walk', s)
    G.on(name, 'open', s)
    if look:
        simple(name, 'look', 'pilot', look)
    return s


def on(obj, verbs, script, other=None):
    for v in verbs.split():
        G.on(obj, v, script, other)


def line(obj, verbs, *texts, who='pilot'):
    s = G.script()
    for t in texts:
        s.say(who, t)
    on(obj, verbs, s)
    return s


def careful(obj, verbs, text):
    """the original's deaths: in the remake the pilot thinks twice"""
    return line(obj, verbs, text, 'No. That would be the end of me. I think twice and leave it.')


def first_visit(room, text, flag=None, extra=None):
    """the original's description of a room, the first time you come in"""
    s = G.script(f'{room}_enter')
    L = s.label()
    s.iff(flag or f'seen_{room}', L)
    s.setf(flag or f'seen_{room}')
    s.say('narrator', text)
    s.here(L)
    if extra:
        extra(s)
    G.rooms[room]['enter'] = s
    return s


# the star fragments: 16 tiny pieces of starlight in the whole game, carried from disk to disk
G.thing('fragments', None, label='star fragments', icon='fragment')
simple('fragments', 'look', 'pilot', 'Tiny pieces of starlight. They hum when I hold them together. '
       'Legend says there are sixteen of them, somewhere out there.')


def find_fragment(s, n, text, already='There is nothing else here.'):
    """the n-th star fragment (1-16)"""
    got, a = s.label(), s.label()
    s.iff(f'frag{n}', got)
    s.say('pilot', text)
    s.say('pilot', 'Something glitters... a tiny piece of starlight!')
    s.sound('score').setf(f'frag{n}')
    s.has('fragments', a)
    s.pickup('fragments')
    s.here(a).end()
    s.here(got)
    s.say('pilot', already)
    return s


def search(obj, n, text, already='There is nothing else here.', verbs='look pickup open'):
    s = G.script()
    find_fragment(s, n, text, already)
    on(obj, verbs, s)
    return s


def chapter_start(intro_cards, part_card, room, x, y, d=BACK, music=None):
    """title, the story check list, the intro and the first room"""
    st = G.script('start')
    st.cuton()
    st.put('pilot', None, 0, 0)
    st.room('title', 0, 0)
    st.put('pilot', None, 0, 0)
    st.music('title')
    st.say('narrator', '*Welcome to the World of Stronkie!', wait=False)
    st.waitkey()
    st.room('cards', 0, 0)
    story_start(st)
    st.cuton()
    if part_card:
        spoken_card(st, *part_card)
    for c in intro_cards:
        st.card(c, wait=True)
    if music:
        st.music(music)
    st.room(room, x, y, d)
    st.cutoff()
    return st


def chapter_end(s, cards, next_card=None):
    """the end of the disk: the story for the next disk"""
    s.fade(0)
    s.room('cards', 0, 0)
    s.put('pilot', None, 0, 0)
    s.music('title')
    for c in cards:
        s.card(c, wait=True)
    s.card('*Congratulations!', wait=True)
    story_end(s)
    if next_card:
        spoken_card(s, *next_card)
    nxt = CH_NAMES.get(CH + 1)
    if nxt:
        s.card(f'End of {CH_NAMES[CH]}. To be continued in {nxt}: put the {nxt} disk in the drive and reset.',
               wait=True)
    s.card('World of Stronkie remake. Created By Mark Stronks, Stronkie Soft.', wait=True)
    s.endgame()
    return s


keepsakes()
