"""World of Stronkie remake - Chapter One: the Prologue (Ravenmoor).

The three parts of the original game's Prologue, with the same story, rooms,
pictures, puzzles, music and speech, but played with the mouse:
  Part 1 The Grounds    road, garden, shed, well, porch
  Part 2 The Manor      hall, library, kitchen, cellar, study, hidden chamber
  Part 3 The Launch Pad stairway, corridor, locker room, hangar, control room, STARRAVEN
The free demo is Part 1 (up to the front door of the manor).

Only the lines the original game spoke are spoken here (a '*' in front):
the title, and the title cards of the next parts."""
# ---------------------------------------------------------------- the people
ACTORS = [   # name, costume, talk colour (fixed palette), voice
    ('pilot', 'pilot', 17, ('rms', 1.0)),
    ('edmund', 'edmund', 19, ('awb', 0.95)),
    ('narrator', None, 30, ('rms', 0.95)),
]
VOICES = {a[0]: a[3] for a in ACTORS}
EXTRA_COSTUMES = ['suit']
SOUNDS = ['pickup', 'door', 'thunder', 'zap', 'launch', 'score', 'drop', 'error', 'beep', 'hyper', 'click']
SONGS = ['title', 'grounds', 'manor', 'launchpad']
SPECIALS = {'pilot': ['reach', 'reachl'], 'suit': ['reach', 'reachl'], 'edmund': []}

G = Game()

# =================================================================== rooms
FLOOR = lambda y: [(0, y), (319, y), (319, 167), (0, 167)]          # noqa: E731
# part 1: the grounds
G.room('road', 'road', music='grounds',
       walk=[[(0, 126), (122, 126), (140, 100), (180, 100), (198, 126), (319, 126), (319, 167), (0, 167)]])
G.room('garden', 'garden', music='grounds', walk=[FLOOR(104)])
G.room('shed', 'shed', music='grounds', walk=[[(40, 124), (280, 124), (300, 167), (20, 167)]])
G.room('well', 'well', music='grounds', walk=[FLOOR(130)])
G.room('porch', 'porch', music='grounds', walk=[[(8, 146), (312, 146), (319, 167), (0, 167)]])
G.room('title', 'title', music='title')
G.room('cards', 'black')

BLOCK = {
    'road': [[(88, 124), (118, 124), (118, 146), (88, 146)], [(202, 124), (232, 124), (232, 146), (202, 146)]],
    'garden': [[(26, 100), (86, 100), (86, 122), (26, 122)], [(234, 100), (308, 100), (308, 128), (234, 128)],
               [(126, 118), (196, 118), (196, 140), (126, 140)]],
    'shed': [[(38, 108), (80, 108), (80, 162), (38, 162)]],
    'well': [[(94, 122), (224, 122), (224, 162), (94, 162)]],
    'library': [[(248, 120), (312, 120), (312, 167), (248, 167)]],
    'kitchen': [[(226, 104), (294, 104), (294, 136), (226, 136)]],
    'study': [[(82, 104), (238, 104), (238, 154), (82, 154)]],
    'secret': [[(138, 110), (182, 110), (182, 136), (138, 136)]],
    'lockers': [[(86, 120), (234, 120), (234, 134), (86, 134)]],
    'hangar': [[(120, 96), (200, 96), (200, 132), (120, 132)]],
}

# =================================================================== things you carry
G.thing('shovel', None, label='shovel', icon='shovel')
G.thing('crank', None, label='iron handle', icon='crank')
G.thing('brasskey', None, label='brass key', icon='brasskey')
G.thing('paper', None, label='scrap of paper', icon='paper')
G.thing('candle', None, label='wax candle', icon='candle')
G.thing('litcandle', None, label='burning candle', icon='litcandle')
G.thing('matches', None, label='box of matches', icon='matches')
G.thing('knife', None, label='kitchen knife', icon='knife')
G.thing('silverkey', None, label='silver key', icon='silverkey')
G.thing('amulet', None, label='amulet', icon='amulet')
G.thing('keycard', None, label='keycard', icon='keycard')
G.thing('suit', None, label='spacesuit', icon='suit')
G.thing('fragments', None, label='star fragments', icon='fragment')

for t, lines in {
    'shovel': ['A sturdy shovel. Good for digging.'],
    'crank': ['A bent iron crank handle with a square end. It must fit something.'],
    'brasskey': ['A large brass key. Its bow is shaped like a raven.'],
    'paper': ['It reads: "I buried the winch handle so they cannot raise the key. - E."'],
    'candle': ['An unlit wax candle.'],
    'litcandle': ['The flame flickers in the draught.'],
    'matches': ['A small box with a few matches left.'],
    'knife': ['A sharp kitchen knife.'],
    'silverkey': ['A small silver key.'],
    'amulet': ['A golden amulet with a glowing red stone. Tiny stars seem to move inside it.'],
    'keycard': ['A plastic keycard. It says: HANGAR ACCESS.'],
}.items():
    simple(t, 'look', 'pilot', *lines)

# the star fragments: 16 tiny pieces of starlight in the whole game (3 in the Prologue)
s = G.script('look_fragments')
c2, c3 = s.label(), s.label()
s.iff('fcount3', c3)
s.iff('fcount2', c2)
s.say('pilot', 'One tiny piece of starlight. It glows in my hand. I wonder how many more there are.')
s.end()
s.here(c2).say('pilot', 'Two tiny pieces of starlight. They hum when I hold them together.')
s.end()
s.here(c3).say('pilot', 'Three tiny pieces of starlight. Legend says there are sixteen of them, somewhere out there.')
G.on('fragments', 'look', s)


def find_fragment(s, n, text):
    """the n-th star fragment (1-16): it goes with the other fragments"""
    got, a, b, done = s.label(), s.label(), s.label(), s.label()
    s.iff(f'frag{n}', got)
    s.say('pilot', text)
    s.say('pilot', 'Something glitters... a tiny piece of starlight!')
    s.sound('score').setf(f'frag{n}')
    s.has('fragments', a)
    s.pickup('fragments')
    s.setf('fcount1').jmp(done)
    s.here(a)
    s.iff('fcount2', b)
    s.setf('fcount2').jmp(done)
    s.here(b).setf('fcount3')
    s.here(done).end()
    s.here(got)
    return s


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


def lightning(room, y):
    s = G.script()
    s.sound('thunder')
    s.say('narrator', 'Lightning flashes! For a moment you see a pale face at an upstairs window.', wait=False)
    return s


# =================================================================== PART 1: THE GROUNDS
# ---- the road
G.thing('manor_r', 'road', (116, 40, 204, 80), None, label='Ravenmoor Manor')
G.thing('trees_r', 'road', (0, 0, 88, 134), None, label='dead tree')
G.thing('trees_r2', 'road', (250, 0, 319, 134), None, label='dead tree')
G.thing('moon_r', 'road', (244, 2, 280, 30), None, label='moon')
G.thing('gate', 'road', (112, 80, 208, 120), (160, 106), BACK, 'walk', label='iron gates')
exit_to('gate', 'garden', 160, 160, BACK)
simple('gate', 'look', 'pilot', 'The iron gates are rusted and hang open on broken hinges.')
simple('gate', 'close', 'pilot', 'They won\'t close. The hinges are broken. Nobody is keeping anyone out here.')
simple('manor_r', 'look', 'pilot', 'Ravenmoor Manor, the house of my Uncle Edmund.',
       'A light burns in the windows. Somebody is home. Or something.')
simple('trees_r', 'look', 'pilot', 'A dead tree. It looks like it wants to grab me. Classic.')
simple('trees_r2', 'look', 'pilot', 'Another dead tree. The garden designer had a theme.')
simple('moon_r', 'look', 'pilot', 'A full moon. Of course it is a full moon.')
first_visit('road', 'You are on a muddy road before the iron gates of Ravenmoor Manor. The gates hang open.')
G.rooms['road'].update(random=lightning('road', 0), rmin=900, rmax=2200)

# ---- the garden
G.thing('to_road', 'garden', (100, 158, 220, 167), (160, 165), FRONT, 'walk', label='path to the gates')
G.thing('bushes', 'garden', (56, 100, 120, 122), None, label='bushes')
G.thing('mound', 'garden', (126, 114, 196, 140), (160, 148), BACK, 'look', label='mound of earth',
        image='dug', state=1)
G.thing('handle_o', 'garden', (146, 118, 166, 130), (160, 148), BACK, 'look', label='iron handle',
        image='handle', state=0)
G.thing('well_g', 'garden', (26, 52, 84, 120), (92, 124), LEFT, 'walk', label='old well')
G.thing('shed_g', 'garden', (236, 66, 308, 128), (230, 132), RIGHT, 'walk', label='garden shed')
G.thing('porch_g', 'garden', (122, 26, 200, 82), (160, 108), BACK, 'walk', label='porch of the manor')
exit_to('to_road', 'road', 160, 130, FRONT)
exit_to('well_g', 'well', 30, 150, RIGHT)
exit_to('shed_g', 'shed', 160, 160, BACK)
exit_to('porch_g', 'porch', 50, 160, RIGHT)
simple('well_g', 'look', 'pilot', 'An old stone well, to the west of the garden.')
simple('shed_g', 'look', 'pilot', 'A garden shed. The door is ajar.')
simple('porch_g', 'look', 'pilot', 'The porch of the manor lies to the north.')
simple('bushes', 'look', 'pilot', 'Bushes. Nothing hides in them. Probably.')

s = G.script()
L = s.label()
s.iff('dug', L)
s.say('pilot', 'The earth has been dug quite recently. Something may be buried here.')
s.end()
s.here(L).say('pilot', 'I have already dug up the mound.')
G.on('mound', 'look', s)
s = G.script()
L = s.label()
s.iff('dug', L)
s.say('pilot', 'I scrape at the earth with my hands. It is no use. I need a tool.')
s.end()
s.here(L).say('pilot', 'I have already dug up the mound.')
G.on('mound', 'pickup', s)
G.on('mound', 'use', s)
G.on('mound', 'pull', s)
s = G.script('dig')
L = s.label()
s.iff('dug', L)
s.say('pilot', 'I dig into the soft earth...')
s.sound('drop').wait(15)
s.sound('drop').wait(15)
s.setf('dug').drop('shovel')
s.imgon('mound').imgon('handle_o').show('handle_o')
s.sound('beep')
s.say('pilot', 'CLANG! I uncover an iron handle!')
s.say('pilot', 'I\'ll leave the shovel here. It has done its job.')
s.end()
s.here(L).say('pilot', 'I have already dug up the mound.')
G.on('shovel', 'use', s, other='mound')
s = G.script()
s.say('pilot', 'I take the iron handle I dug up.')
s.imgoff('handle_o').hide('handle_o').pickup('crank')
G.on('handle_o', 'pickup', s)
simple('handle_o', 'look', 'pilot', 'An iron handle, half out of the hole.')
first_visit('garden', 'You are in an overgrown garden. In the middle is a mound of freshly dug earth. '
            'A shed stands to the east, an old well to the west.')
G.rooms['garden'].update(random=lightning('garden', 0), rmin=1200, rmax=2600)

# ---- the shed
G.thing('shed_out', 'shed', (110, 158, 210, 167), (160, 165), FRONT, 'walk', label='way out')
G.thing('tools', 'shed', (96, 20, 200, 90), (156, 128), BACK, 'look', label='rusty tools')
G.thing('workbench', 'shed', (96, 90, 186, 106), (150, 130), BACK, 'look', label='workbench')
G.thing('barrel_s', 'shed', (40, 106, 78, 160), (86, 150), LEFT, 'look', label='barrel')
G.thing('lamp_s', 'shed', (200, 34, 226, 60), None, label='round window')
G.thing('cobweb', 'shed', (80, 20, 110, 50), None, label='cobwebs')
G.thing('shovel_o', 'shed', (148, 24, 166, 86), (156, 128), BACK, 'look', label='shovel', image='shovel', state=3)
exit_to('shed_out', 'garden', 230, 134, LEFT)
s = G.script()
L = s.label()
s.ifnf('shovel_taken', L)
s.say('pilot', 'All rusted beyond use.')
s.end()
s.here(L).say('pilot', 'All rusted beyond use, except for a shovel.')
G.on('tools', 'look', s)
s = G.script()
find_fragment(s, 1, 'I move the rusty tools aside...')
s.say('pilot', 'Just rusty tools. Nothing else is hiding in there.')
G.on('tools', 'pickup', s)
G.on('tools', 'push', s)
G.on('tools', 'pull', s)
G.on('tools', 'use', s)
G.on('tools', 'open', s)
simple('shovel_o', 'look', 'pilot', 'A sturdy shovel. Good for digging.')
s = G.script()
s.imgoff('shovel_o').hide('shovel_o').setf('shovel_taken').pickup('shovel')
s.say('pilot', 'A shovel. Every adventurer needs a shovel.')
G.on('shovel_o', 'pickup', s)
simple('workbench', 'look', 'pilot', 'A workbench with some old tins on it. Paint, nails, and something that used to be soup.')
simple('barrel_s', 'look', 'pilot', 'A rain barrel. Empty, apart from a very surprised spider.')
simple('lamp_s', 'look', 'pilot', 'Moonlight falls in through a round little window.')
simple('cobweb', 'look', 'pilot', 'Cobwebs fill every corner. The spiders here have been busy for years.')
first_visit('shed', 'You are inside a damp garden shed. Rusty tools hang on the walls and cobwebs fill every corner.')

# ---- the well
G.thing('well_out', 'well', (292, 90, 319, 167), (306, 150), RIGHT, 'walk', label='back to the garden')
G.thing('tree_w', 'well', (0, 0, 80, 112), None, label='dead tree')
G.thing('wellpit', 'well', (96, 84, 224, 160), (82, 150), RIGHT, 'look', label='well')
G.thing('rope_w', 'well', (154, 50, 166, 92), (82, 150), RIGHT, 'look', label='bucket')
G.thing('winch', 'well', (188, 38, 230, 62), (236, 150), LEFT, 'look', label='winch')
G.thing('bucket_o', 'well', (148, 58, 172, 84), (82, 150), RIGHT, 'look', label='bucket', image='bucket', state=0)
G.thing('wkey', 'well', (154, 58, 168, 68), (82, 150), RIGHT, 'look', label='brass key', image='wellkey', state=0)
exit_to('well_out', 'garden', 92, 126, RIGHT)
simple('wellpit', 'look', 'pilot', 'The well is deep and dark. The winch has a square hole where a handle should go.',
       'I half expect a king with a feather in his cap to climb out of it.')
simple('rope_w', 'look', 'pilot', 'The bucket hangs far down the well, out of reach.')
s = G.script()
s.say('pilot', 'The bucket is far too heavy to pull up by hand.')
G.on('rope_w', 'pull', s)
G.on('rope_w', 'pickup', s)
s = G.script()
s.say('pilot', 'Climb down the rope? It is old and rotten. It would snap, and I would plunge into the icy water far below.')
s.say('pilot', 'Not my brightest idea. Let\'s not.')
G.on('rope_w', 'use', s)
G.on('wellpit', 'use', s)
s = G.script()
s.say('pilot', 'Jump into the well? I have seen how that ends in other games.')
G.on('wellpit', 'pickup', s)
G.on('wellpit', 'open', s)
s = G.script()
L = s.label()
s.iff('bucket_up', L)
s.say('pilot', 'The winch has no handle. I cannot turn it.')
s.end()
s.here(L).say('pilot', 'The bucket is already up.')
G.on('winch', 'look', s)
G.on('winch', 'use', s)
G.on('winch', 'pull', s)
G.on('winch', 'push', s)
s = G.script('turn_winch')
L = s.label()
s.iff('bucket_up', L)
s.say('pilot', 'I fit the handle onto the winch and turn.')
s.drop('crank').setf('bucket_up').sound('door')
s.wait(30)
s.imgon('bucket_o').show('bucket_o').imgon('wkey').show('wkey')
s.say('pilot', 'With a creak the bucket rises out of the darkness. Inside it lies a brass key!')
s.end()
s.here(L).say('pilot', 'The bucket is already up.')
G.on('crank', 'use', s, other='winch')
G.on('crank', 'use', s, other='wellpit')
simple('bucket_o', 'look', 'pilot', 'The old bucket, up at last.')
simple('wkey', 'look', 'pilot', 'A large brass key, in the bucket.')
s = G.script()
s.say('pilot', 'I take the brass key out of the bucket.')
s.imgoff('wkey').hide('wkey').pickup('brasskey')
G.on('wkey', 'pickup', s)
simple('tree_w', 'look', 'pilot', 'A dead tree. Even the owls have moved out.')
first_visit('well', 'You stand by an old stone well. A bucket hangs far down on a rope. The winch is missing its handle.')
G.rooms['well'].update(random=lightning('well', 0), rmin=1400, rmax=3000)

# ---- the porch
G.thing('porch_out', 'porch', (0, 136, 30, 167), (12, 160), LEFT, 'walk', label='path to the garden')
G.thing('pillars', 'porch', (36, 0, 72, 140), None, label='pillar')
G.thing('pillars2', 'porch', (248, 0, 284, 140), None, label='pillar')
G.thing('plamp', 'porch', (218, 18, 242, 44), None, label='lamp')
G.thing('door', 'porch', (108, 0, 210, 144), (160, 152), BACK, 'open', label='front door', image='door', state=1)
G.thing('knocker', 'porch', (150, 44, 170, 68), (160, 152), BACK, 'look', label='door knocker')
G.thing('mat', 'porch', (112, 150, 214, 167), (96, 156), RIGHT, 'look', label='doormat')
exit_to('porch_out', 'garden', 160, 110, FRONT)
s = G.script()
L = s.label()
s.iff('door_open', L)
s.say('pilot', 'A heavy oak door with a brass lock shaped like a raven.')
s.end()
s.here(L).say('pilot', 'The front door stands open. The darkness inside waits for me.')
G.on('door', 'look', s)
s = G.script('door_open')
L, K = s.label(), s.label()
s.iff('door_open', L)
s.has('brasskey', K)
s.say('pilot', 'The door is locked. The lock is shaped like a raven.')
s.end()
s.here(K)
s.say('pilot', 'The brass key turns with a loud clunk.')
s.sound('door').drop('brasskey').setf('door_open').imgon('door')
s.say('pilot', 'The door creaks open.')
s.end()
s.here(L)
P = s.label()
s.iff('got_paper', P)
s.say('pilot', 'Wait. Something sticks out from under the doormat... a scrap of paper. I\'ll keep it.')
s.setf('got_paper').pickup('paper')
s.here(P)
if DEMO:
    s.cuton()
    s.walk('pilot', 160, 148)
    s.say('narrator', 'You step into the darkness of the manor. Behind you the door slams shut!')
    s.sound('door')
    s.fade(0)
    s.room('cards', 0, 0)
    s.card('This is where the mystery of Ravenmoor begins... End of the demo.', wait=True)
    s.card('Get the full game of World of Stronkie remake at stronkie.itch.io', wait=True)
    s.endgame()
else:
    s.jmp('enter_manor')
G.on('door', 'open', s)
G.on('door', 'walk', s)
G.on('brasskey', 'use', s, other='door')
G.on('brasskey', 'use', s, other='knocker')
s = G.script()
s.say('pilot', 'I knock. The sound echoes through the house, but nobody answers.')
G.on('knocker', 'use', s)
G.on('knocker', 'push', s)
G.on('knocker', 'pull', s)
G.on('door', 'push', s)
simple('knocker', 'look', 'pilot', 'A brass door knocker in the shape of a ring.')
s = G.script()
s.say('pilot', 'It\'s already open. The house wants me inside. That\'s not creepy at all.')
G.on('door', 'close', s)
s = G.script()
L = s.label()
s.iff('got_paper', L)
s.say('pilot', 'A worn doormat. It says WELCOME, but it does not mean it.')
s.end()
s.here(L).say('pilot', 'A worn doormat. Nothing else under it.')
G.on('mat', 'look', s)
s = G.script()
L = s.label()
s.iff('got_paper', L)
s.say('pilot', 'Under the mat I find a scrap of paper.')
s.setf('got_paper').pickup('paper')
s.end()
s.here(L).say('pilot', 'There is nothing else under the mat.')
G.on('mat', 'pickup', s)
G.on('mat', 'pull', s)
G.on('mat', 'push', s)
G.on('mat', 'open', s)
simple('pillars', 'look', 'pilot', 'A marble pillar. Uncle Edmund always liked to make an impression.')
simple('pillars2', 'look', 'pilot', 'The other pillar. Same impression.')
simple('plamp', 'look', 'pilot', 'A lamp burns beside the door. Somebody lit it, not long ago.')
first_visit('porch', 'You are on the porch of the manor. A heavy oak door leads north. A worn doormat lies at your feet.')

# =================================================================== PARTS 2 AND 3 (not in the demo)
if not DEMO:
    _f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'ch1_house.py')
    exec(compile(open(_f).read(), _f, 'exec'), globals())


# =================================================================== the start: title and intro
start = G.script('start')
start.cuton()
start.put('pilot', None, 0, 0)
start.room('title', 0, 0)
start.put('pilot', None, 0, 0)
start.music('title')
start.say('narrator', '*Welcome to the World of Stronkie!', wait=False)
start.waitkey()
start.room('cards', 0, 0)
start.card('A letter from your Uncle Edmund brought you here: "Come to Ravenmoor at once. I have found it."', wait=True)
start.card('Nobody has seen him since. Now, on a stormy night, you arrive at the gates of his manor.', wait=True)
start.card('Prologue, Part 1: The Grounds', wait=True)
start.music('grounds')
start.room('road', 160, 160, BACK)
start.cutoff()

default_answers()

START_ACTORS = {} if DEMO else {'edmund': ('control', 252, 162, 3)}
VARIANTS = {
    'dug': ('garden', {}, {'dug': True}),
    'handle': ('garden', {}, {'dug': True, 'handle': True}),
    'shovel': ('shed', {}, {'shovel': True}),
    'bucket': ('well', {}, {'bucket': True}),
    'wellkey': ('well', {}, {'bucket': True, 'key': True}),
    'door': ('porch', {}, {'open_door': True}),
    'smalldoor': ('hall', {}, {'small_open': True}),
    'passage': ('library', {}, {'passage': True}),
    'candle': ('kitchen', {}, {'candle': True}),
    'matches': ('kitchen', {}, {'matches': True}),
    'knife': ('kitchen', {}, {'knife': True}),
    'skey': ('cellar', {}, {'key': True}),
    'freed': ('secret', {}, {'freed': True}),
    'amulet': ('secret', {}, {'amulet': True}),
    'blast': ('bunker', {}, {'open_door': True}),
    'locker': ('lockers', {}, {'open_locker': True}),
    'roof': ('hangar', {}, {'roof': True}),
    'hatch': ('hangar', {}, {'hatch': True}),
    'flame': ('hangar', {}, {'hatch': True, 'flame': True}),
    'camulet': ('control', {}, {'amulet': True}),
    'lever': ('control', {}, {'lever': True}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('road', 'Road', 160, 150), ('shed', 'Shed', 160, 150), ('well', 'Well', 40, 150),
             ('porch', 'Porch', 60, 160), ('hall', 'Hall', 160, 150), ('cellar', 'Cellar', 160, 150),
             ('secret', 'Chamber', 100, 150), ('stairs', 'Stairway', 160, 130), ('lockers', 'Lockers', 260, 150),
             ('hangar', 'Hangar', 60, 150)]           # (at most 10: the menu has 12 places)
if DEMO:
    DEV_SPOTS = DEV_SPOTS[:4]
DEV_ITEMS = ['shovel', 'crank', 'brasskey', 'paper'] if DEMO else \
    ['brasskey', 'litcandle', 'matches', 'knife', 'silverkey', 'amulet', 'keycard', 'suit']
