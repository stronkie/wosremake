"""World of Stronkie remake - Chapter Six: The Star Heart (disk 6).

The original game's Chapter 9 (The Star Heart: Vex in the temple) and Chapter
10 (Repairs: the old crystal mines with Pip). Keepsake of this disk: the
silver horn."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p12', 'p13']
ACTORS.append(('vex', 'vex', 25, ('rms', 1.0)))
ACTORS.append(('edmund', 'edmund', 19, ('awb', 0.95)))
ACTORS.append(('pip', 'pip', 24, ('rms', 1.2)))
G.actors.extend(['vex', 'edmund', 'pip'])
SPECIALS.update({'vex': [], 'edmund': [], 'pip': []})
LITE = ('vex', 'edmund')
for n, c in (('soldier', 18), ('bix', 19)):
    add_actor(n, c)

# =================================================================== rooms
G.room('heart', 'heart', music='p12', walk=[FLOOR(122)])
G.room('westgal', 'westgal', music='p12', walk=[[(120, 100), (200, 100), (300, 167), (20, 167)]])
G.room('eastgal', 'eastgal', music='p12', walk=[[(120, 112), (200, 112), (300, 167), (20, 167)]])
G.room('altar', 'altar', music='p12', walk=[[(0, 150), (86, 150), (86, 167), (0, 167)],
                                             [(234, 150), (319, 150), (319, 167), (234, 167)]])
G.room('catacomb', 'catacomb', music='p12', walk=[FLOOR(136)])
G.room('deadend', 'deadend', music='p12', walk=[FLOOR(140)])
G.room('site', 'workshop', music='p13', walk=[[(0, 140), (222, 140), (222, 167), (0, 167)]])
G.room('mineentry', 'mineentry', music='p13', walk=[FLOOR(142)])
G.room('maze1', 'maze', music='p13', walk=[[(110, 132), (210, 132), (300, 167), (20, 167)]])
G.room('maze2', 'maze', music='p13', walk=[[(110, 132), (210, 132), (300, 167), (20, 167)]])
G.room('maze3', 'maze3', music='p13', walk=[[(110, 132), (210, 132), (300, 167), (20, 167)]])
G.room('vein', 'vein', music='p13', walk=[FLOOR(130)])
BLOCK = {'heart': [[(104, 118), (214, 118), (214, 126), (104, 126)]],
         'maze3': [[(134, 144), (186, 144), (186, 158), (134, 158)]]}

# =================================================================== things you carry
G.thing('amulet', None, label='amulet', icon='amulet')
simple('amulet', 'look', 'pilot', 'It is burning hot and glowing brightly.')
line('amulet', 'give', 'Not here, not now. I will need it.')
for nm, lab, ic, txt in (('hammer', 'crystal hammer', 'hammer', 'A heavy hammer for breaking crystal.'),
                         ('kite', 'kite', 'kite', 'A little blue kite with a long tail.'),
                         ('starcrystal', 'star crystal', 'starcrystal', 'A perfect star crystal. It hums softly in my hand.')):
    G.thing(nm, None, label=lab, icon=ic)
    simple(nm, 'look', 'pilot', txt)
line('starcrystal', 'use', 'It is not a candy.')
s = G.script()
s.say('pilot', 'TOOT!')
s.sound('beep')
s.say('narrator', 'The sound echoes through the temple.')
G.on('horn', 'use', s)

# =================================================================== CHAPTER 9: THE STAR HEART
# ---- the heart chamber
hot('starheart', 'heart', (108, 10, 212, 116), (160, 128), BACK, 'walk', label='altar with the Star Heart')
s = G.script()
L = s.label()
s.iff('vex_fled', L)
s.say('pilot', 'On a high altar floats the Star Heart: a crystal as bright as a sun... but growing dimmer every moment.')
s.end()
s.here(L).say('pilot', 'The Star Heart flickers weakly. The hollow for the amulet is up on the altar.')
G.on('starheart', 'look', s)
s = G.script()
L = s.label()
s.iff('vex_fled', L)
s.say('vex', 'One more step, pilot...')
s.say('narrator', 'Vex aims his ray gun at you.')
s.end()
s.here(L)
s.room('altar', 40, 160, RIGHT)
on('starheart', 'walk', s)
line('amulet', 'use', 'The hollow for the amulet is up on the altar.')
hot('vmach', 'heart', (212, 90, 246, 122), (200, 132), RIGHT, label='Vex\'s machine', image='machine', state=3,
    look='A humming black machine. Its cables run off to the east gallery.')
G.thing('vex_t', 'heart', (0, 0, 1, 1), (240, 150), LEFT, 'talk', label='Commander Vex', actor='vex')
simple('vex_t', 'look', 'pilot', 'Tall and thin in a black coat, with a raven on his helmet. His face looks strangely familiar.')
careful('vex_t', 'push pull', 'Vex is faster. ZAP!')
s = G.script()
L = s.label()
s.iff('vex_fled', L)
s.say('vex', 'Your uncle was just as stubborn. Give me the amulet!')
s.end()
s.here(L)
G.on('vex_t', 'talk', s)
careful('vex_t', 'give', 'If Vex gets the amulet, his machine roars and the Star Heart goes dark forever...')
door('hr_west', 'heart', (48, 24, 82, 118), (66, 128), LEFT, 'west gallery', ('westgal', 160, 150, FRONT))
door('hr_east', 'heart', (238, 24, 272, 118), (254, 128), RIGHT, 'east gallery', ('eastgal', 160, 150, FRONT))
hot('trapdoor', 'heart', (120, 132, 200, 150), (160, 156), BACK, 'walk', label='hidden trapdoor', state=0,
    look='A hidden trapdoor. Vex fled down there, into the catacombs.')
s = G.script()
s.room('catacomb', 160, 156, BACK)
on('trapdoor', 'walk open', s)
s = G.script('horn_heart')
A, B = s.label(), s.label()
s.iff('vex_fled', B)
s.iff('unplugged', A)
s.say('pilot', 'TOOT!')
s.say('vex', 'Nice tune! But my machine is still running.')
s.say('narrator', 'Vex covers his ears and laughs.')
s.end()
s.here(A)
s.cuton()
s.say('pilot', 'TOOOOT!')
s.sound('zap')
s.say('narrator', 'The note of the horn bounces around the chamber. Vex\'s ray gun sparks and falls from his hand.')
s.say('narrator', 'He staggers back, kicks open a hidden trapdoor and flees down into the catacombs!')
s.walk('vex', 160, 150)
s.put('vex', 'deadend', 160, 146, FRONT)
s.hide('vex_t').show('trapdoor').setf('vex_fled')
s.cutoff()
s.end()
s.here(B)
s.say('pilot', 'TOOT! The sound echoes through the temple.')
G.on('horn', 'use', s, other='vex_t')
G.on('horn', 'use', s, other='starheart')
G.on('horn', 'use', s, other='vmach')
G.thing('edmund_t', 'heart', (0, 0, 1, 1), (100, 150), LEFT, 'talk', label='Uncle Edmund and Bix', actor='edmund',
        state=0)
G.thing('edmund_a', 'altar', (0, 0, 1, 1), (240, 160), RIGHT, 'talk', label='Uncle Edmund', actor='edmund', state=0)
simple('edmund_t', 'look', 'pilot', 'Uncle Edmund, muddy and out of breath, but smiling. Bix waves.')
s = G.script()
L = s.label()
s.iff('edmund_up', L)
s.say('edmund', 'A raven lock! Vex sealed the hollow. It takes two: one holds the lock, one turns the amulet.')
s.say('edmund', 'Come on, up we go!')
s.say('narrator', 'He climbs onto the altar.')
s.setf('edmund_up')
s.put('edmund', 'altar', 270, 160, LEFT)
s.hide('edmund_t').show('edmund_a')
s.end()
s.here(L)
s.say('edmund', 'Turn the amulet in the hollow, I\'ll hold the lock!')
G.on('edmund_t', 'talk', s)
s = G.script('heart_in')
A, B, I = s.label(), s.label(), s.label()
s.iff('intro_done', I)
s.setf('intro_done')
s.cuton()
s.say('narrator', 'Commander Vex steps out of the shadows, a ray gun in his hand. His soldiers drag a humming machine '
      'into the chamber and hook it up to the Star Heart.')
s.say('vex', 'Stand aside, little pilot. This world\'s power is MINE.')
s.cutoff()
s.here(I)
s.iff('seen_heart', A)
s.setf('seen_heart')
s.say('narrator', 'You are in the heart chamber. On a high altar floats the Star Heart, but it flickers weakly. '
      'Galleries lead east and west.')
s.here(A)
s.iff('vex_trapped', B)
s.end()
s.here(B)
C = s.label()
s.iff('edmund_came', C)
s.cuton()
s.setf('edmund_came').sound('door')
s.put('edmund', 'heart', 40, 150, RIGHT)
s.walk('edmund', 100, 150)
s.show('edmund_t')
s.say('narrator', 'Footsteps! Uncle Edmund rushes into the chamber, with Bix right behind him.')
s.say('edmund', 'I followed you in my old backup ship. Landed in a lake. Never mind! Where is Vex?')
s.cutoff()
s.here(C)
G.rooms['heart']['enter'] = s

# ---- the west gallery
hot('murals', 'westgal', (2, 14, 118, 110), (90, 140), LEFT, label='murals')
search('murals', 12, 'Old murals show Stronkies chasing away monsters with the sound of a horn. Behind a loose stone...',
       'Monsters with hands over their ears, fleeing from a horn.', verbs='look')
hot('horn_o', 'westgal', (216, 112, 260, 140), (220, 150), RIGHT, 'pickup', label='silver horn', image='horn', state=3,
    look='A curled silver horn. The murals show what it does.')
s = G.script()
s.hide('horn_o').imgoff('horn_o').pickup('horn')
G.on('horn_o', 'pickup', s)
door('wg_out', 'westgal', (120, 18, 200, 96), (160, 106), BACK, 'way back to the heart chamber', ('heart', 66, 132, RIGHT))
first_visit('westgal', 'You are in the west gallery. Old murals show Stronkies chasing away monsters with the sound of a horn.')

# ---- the east gallery
hot('plug', 'eastgal', (212, 56, 252, 92), (200, 130), RIGHT, 'pull', label='big plug',
    look='A huge plug in a stone socket. Vex\'s cables are attached to it.')
hot('cables', 'eastgal', (60, 90, 220, 167), None, label='cables', look='Vex\'s thick cables run along the floor to the plug.')
hot('esoldier', 'eastgal', (216, 88, 244, 130), (196, 140), RIGHT, 'talk', label='soldier', image='esoldier', state=3,
    look='A soldier in black guards the plug. He wears a big helmet.')
s = G.script()
s.say('soldier', 'Hands off!')
G.on('esoldier', 'talk', s)
s = G.script()
A, B = s.label(), s.label()
s.iff('soldier_gone', A)
s.say('soldier', 'Hands off!')
s.say('narrator', 'The soldier blocks your way.')
s.end()
s.here(A)
s.iff('unplugged', B)
s.cuton()
s.say('pilot', 'I yank the plug out of the wall.')
s.sound('zap').setf('unplugged')
s.say('narrator', 'With a dying whine Vex\'s machine stops. From the chamber comes a furious scream.')
s.say('vex', 'NOOOO!')
s.cutoff()
s.end()
s.here(B).say('pilot', 'Unplugged. Vex\'s machine is dead.')
on('plug', 'pull use', s)
s = G.script()
L = s.label()
s.iff('soldier_gone', L)
s.cuton()
s.say('pilot', 'TOOOOT!')
s.sound('zap')
s.say('narrator', 'A piercing note fills the gallery. The soldier clutches his helmet, screams and runs away!')
s.imgoff('esoldier').hide('esoldier').setf('soldier_gone')
s.cutoff()
s.end()
s.here(L)
s.say('pilot', 'TOOT!')
G.on('horn', 'use', s, other='esoldier')
G.on('horn', 'use', s, other='plug')
door('eg_out', 'eastgal', (120, 22, 200, 110), (160, 116), BACK, 'way back to the heart chamber', ('heart', 254, 132, LEFT))
first_visit('eastgal', 'You are in the east gallery. Vex\'s thick cables run along the floor to a big plug in the wall.')

# ---- the altar
hot('heartbig', 'altar', (122, 0, 196, 72), None, label='Star Heart', look='The Star Heart. It flickers weakly.')
hot('ravenlock', 'altar', (134, 100, 182, 144), (90, 160), RIGHT, 'open', label='raven lock',
    look='A round hollow, sealed by a heavy raven lock. It looks like a two-person job.')
line('ravenlock', 'open pull push', 'The lock is far too heavy to hold and turn at the same time.')
s = G.script()
s.say('edmund', 'Turn the amulet in the hollow, I\'ll hold the lock!')
G.on('edmund_a', 'talk', s)
door('al_down', 'altar', (0, 100, 30, 150), (20, 160), LEFT, 'steps down', ('heart', 160, 132, FRONT))
s = G.script('heal')
L = s.label()
s.iff('edmund_up', L)
s.say('pilot', 'The raven lock blocks the hollow. It needs two people to open.')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'Uncle Edmund holds the raven lock open while you press the amulet into the hollow. CLICK!')
s.sound('hyper')
s.say('narrator', 'The Star Heart blazes up like a new sun, and all over the planet the Stronkies cheer!')
s.sound('thunder')
s.say('narrator', 'Then a beam of red light shoots down from the sky. It rips Vex out of the catacombs... '
      'and Uncle Edmund with him!')
s.put('edmund', None, 0, 0)
s.say('narrator', 'High above, a huge black flagship slides away into orbit. Vex\'s voice echoes through the temple:')
s.say('vex', 'This isn\'t over, kid!')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
spoken_card(s, 'Chapter 10: Repairs', 'p12_card')
s.card('The Star Heart shines again, but Uncle Edmund is gone: Vex took him up to his flagship in orbit.', wait=True)
s.card('Bix has dragged the STARRAVEN to his workshop. "I can fix her," he says, "but her new engine needs a star crystal '
       'from the old mines. And nobody goes into the mines without a light."', wait=True)
s.music('p13')
s.room('site', 60, 156, RIGHT)
s.cutoff()
G.on('amulet', 'use', s, other='ravenlock')
G.on('amulet', 'use', s, other='heartbig')
first_visit('altar', 'You stand on the altar beside the Star Heart. There is a round hollow in its base, but a heavy lock '
            'shaped like a raven seals it.')

# ---- the catacombs
hot('clever', 'catacomb', (230, 80, 246, 112), (226, 146), RIGHT, 'pull', label='old lever',
    look='An old stone lever. A carving shows bars falling over an archway.')
hot('arch', 'catacomb', (248, 40, 284, 138), (240, 146), RIGHT, 'walk', label='archway', image='cbars', state=1)
s = G.script()
L = s.label()
s.iff('vex_trapped', L)
s.room('deadend', 30, 156, RIGHT)
s.end()
s.here(L).say('pilot', 'The crystal bars block the archway. Vex is not going anywhere.')
on('arch', 'walk open', s)
s = G.script()
A, B = s.label(), s.label()
s.iff('vex_trapped', A)
s.iff('vex_seen', B)
s.say('pilot', 'I pull the old lever...')
s.say('narrator', 'Nothing happens. A carving shows bars falling over an archway. Maybe later.')
s.end()
s.here(B)
s.cuton()
s.say('pilot', 'I pull the old lever.')
s.sound('thunder').imgon('arch').setf('vex_trapped')
s.say('narrator', 'With a crash, a gate of crystal bars drops in front of the dead end. Vex is trapped!')
s.say('vex', 'You don\'t even know who I am, kid!')
s.say('narrator', 'He rattles the bars.')
s.cutoff()
s.end()
s.here(A).say('pilot', 'The lever is down. Vex is trapped.')
on('clever', 'pull push use', s)
door('cc_up', 'catacomb', (118, 28, 202, 106), (160, 140), BACK, 'way up to the heart chamber', ('heart', 160, 156, FRONT))
first_visit('catacomb', 'You are in the catacombs under the temple. Glowing crystals light ancient tunnels. An old lever '
            'sticks out of the wall beside an archway to the east.')

# ---- the dead end
hot('chasm', 'deadend', (100, 120, 210, 167), None, label='chasm', look='A deep, dark chasm. No way across.')
careful('chasm', 'walk use', 'Jump into the chasm? Vex would watch me fall, and smile.')
hot('bars', 'deadend', (102, 0, 208, 44), None, label='crystal bars',
    look='A gate of crystal bars hangs above the archway. Something must let it drop.')
G.thing('vex_d', 'deadend', (0, 0, 1, 1), (110, 150), RIGHT, 'talk', label='Commander Vex', actor='vex')
s = G.script()
s.say('vex', 'Stay back, kid! You have no idea what you\'re messing with.')
s.say('narrator', 'Vex backs away to the edge of the chasm.')
G.on('vex_d', 'talk', s)
line('vex_d', 'push pull', 'Vex dodges and laughs. I will never catch him like this. Maybe I can trap him in here instead.')
door('de_out', 'deadend', (0, 40, 18, 167), (16, 156), LEFT, 'archway back to the catacombs', ('catacomb', 230, 146, LEFT))
s = G.script('dead_in')
L = s.label()
s.iff('vex_seen', L)
s.setf('vex_seen')
s.say('narrator', 'You are at a dead end on the edge of a deep chasm. Above the archway hangs a gate of crystal bars.')
s.say('narrator', 'Vex is here! He stands with his back to the chasm, looking for a way out. There is none... except past you.')
s.here(L)
G.rooms['deadend']['enter'] = s
s = G.script()
s.say('vex', 'Ask your dear uncle who I am, kid.')
s.say('narrator', 'Vex glares through the bars.')
G.on('arch', 'talk', s)

# =================================================================== CHAPTER 10: REPAIRS
# ---- Bix's workshop
hot('newengine', 'site', (108, 100, 228, 130), (160, 148), BACK, 'walk', label='STARRAVEN',
    look='The battered STARRAVEN fills half of the workshop. Bix has taken the engine apart. A round socket waits for a '
         'star crystal.')
hot('bix_s', 'site', (230, 98, 266, 166), (216, 156), RIGHT, 'talk', label='Bix',
    look='Bix has oil on his ears and a happy glint in his eye.')
hot('hammer_o', 'site', (44, 102, 84, 122), (64, 148), BACK, 'pickup', label='crystal hammer', image='hammer', state=3,
    look='A heavy hammer for breaking crystal.')
s = G.script()
s.hide('hammer_o').imgoff('hammer_o').pickup('hammer')
s.say('bix', 'Yes, take my hammer!')
G.on('hammer_o', 'pickup', s)
s = G.script()
L = s.label()
s.iff('engine_ok', L)
s.say('bix', 'A star crystal, that\'s what she needs. Take my hammer. And find a light before you go into the mines!')
s.end()
s.here(L).say('bix', 'She\'s ready! Go get your uncle!')
G.on('bix_s', 'talk', s)
s = G.script()
s.cuton()
s.drop('starcrystal').setf('engine_ok')
s.say('narrator', 'Bix fits the star crystal into the new engine. The STARRAVEN hums, then ROARS!')
nova(s, 'All systems green, pilot. I\'ve tracked Vex\'s flagship. It\'s called the IRON RAVEN.', 'p13_m17')
s.cutoff()
G.on('starcrystal', 'give', s, other='bix_s')
G.on('starcrystal', 'use', s, other='newengine')
s = G.script('takeoff')
L = s.label()
s.iff('engine_ok', L)
nova(s, 'No engine, no flight, pilot.', 'p13_m19')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'Pip waves his kite as the STARRAVEN climbs into the sky.')
nova(s, 'Hold on, Uncle Edmund. We\'re coming.', 'p13_m18')
s.sound('launch')
chapter_end(s, ['Up through the purple clouds, into orbit... towards the IRON RAVEN.'],
            ('Chapter 11: Vex\'s Flagship', 'p13_card'))
on('newengine', 'walk open', s)
door('si_east', 'site', (0, 150, 60, 167), (20, 160), LEFT, 'path east to the old crystal mines', ('mineentry', 40, 156, RIGHT))
first_visit('site', 'You are in Bix\'s workshop. The battered STARRAVEN fills half of it, surrounded by tools. A path leads '
            'east to the old crystal mines.')

# ---- the mine entrance
hot('kitetree', 'mineentry', (60, 0, 180, 140), (110, 150), BACK, 'use', label='tall tree',
    look='A tall purple tree. A kite is stuck high up in it.')
hot('kite_o', 'mineentry', (94, 10, 124, 40), (110, 150), BACK, 'pickup', label='kite', image='nokite', state=1,
    look='A little blue kite with a long tail, stuck high up in the branches.')
s = G.script()
s.cuton()
s.say('narrator', 'You climb the tree, wobble along a branch and free the kite. Not bad for a pilot!')
s.imgon('kite_o').hide('kite_o').pickup('kite').sound('score')
s.cutoff()
on('kite_o', 'pickup pull', s)
on('kitetree', 'use pull push', s)
hot('pip_m', 'mineentry', (124, 116, 156, 160), (110, 156), RIGHT, 'talk', label='little Stronkie', image='nopip', state=1,
    look='A little Stronkie called Pip. His ears glow like two lanterns.')
s = G.script()
s.say('pip', 'My kite is stuck in the tree. And I\'m too small to climb.')
s.say('narrator', 'Pip sniffs.')
G.on('pip_m', 'talk', s)
s = G.script()
s.cuton()
s.drop('kite')
s.say('narrator', 'Pip hugs his kite. His ears glow bright with joy!')
s.imgon('pip_m').hide('pip_m')
s.put('pip', 'mineentry', 140, 156, LEFT)
s.say('pip', 'Thank you! I know the old mines. My ears will light the way!')
s.say('narrator', 'From now on, Pip follows you everywhere.')
s.setf('pip_follows').sound('score')
s.cutoff()
G.on('kite', 'give', s, other='pip_m')
G.on('kite', 'use', s, other='pip_m')
s = G.script()
L = s.label()
s.iff('pip_follows', L)
s.say('pilot', 'Pitch black. I take two steps into the tunnel. I won\'t get far without a light.')
s.end()
s.here(L)
s.room('maze1', 160, 160, BACK)
hot('tunnel', 'mineentry', (218, 64, 286, 136), (250, 146), BACK, 'walk', label='dark tunnel',
    look='Pitch black. I would need a light in there.')
on('tunnel', 'walk open', s)
door('me_west', 'mineentry', (0, 100, 16, 167), (16, 156), LEFT, 'path back to the workshop', ('site', 200, 150, LEFT))
first_visit('mineentry', 'You stand at the entrance of the old crystal mines. A dark tunnel leads east. Under a tall tree sits '
            'a little Stronkie with glowing ears, crying. His kite is stuck high up in the branches.')

# ---- the maze of twisty little crystal passages
PIP_LINES = {'maze1': 'North! The crystal smell comes from the north. Straight ahead!',
             'maze2': 'East! Definitely east. That way, to the right!',
             'maze3': 'Down there! Down the hole!',
             'vein': 'A Stronkie saying: if someone says they\'ve seen asteroids with more brains than you, ask if '
                     'they\'ve been looking in a mirror!',
             'mineentry': 'Where to next?', 'site': 'Where to next?'}
MAZE = {'maze1': {'N': 'maze2', 'S': 'maze1', 'E': 'maze1', 'W': 'mineentry'},
        'maze2': {'N': 'maze1', 'S': 'maze1', 'E': 'maze3', 'W': 'maze2'},
        'maze3': {'N': 'maze2', 'S': 'maze3', 'E': 'maze1', 'W': 'maze2', 'D': 'vein'}}
ARRIVE = {'N': (160, 160, BACK), 'S': (160, 136, FRONT), 'E': (60, 150, RIGHT), 'W': (260, 150, LEFT)}
for rm, ex in MAZE.items():
    for d, (lab, box, wk, face) in {'N': ('passage ahead', (122, 22, 198, 92), (160, 136), BACK),
                                    'W': ('passage to the left', (72, 94, 100, 130), (100, 142), LEFT),
                                    'E': ('passage to the right', (220, 94, 250, 130), (220, 142), RIGHT),
                                    'S': ('passage behind me', (100, 160, 220, 167), (160, 160), FRONT)}.items():
        to = ex[d]
        x, y, f = (250, 146, FRONT) if to == 'mineentry' else ARRIVE[d]
        door(f'{rm}_{d}', rm, box, wk, face, lab, (to, x, y, f))
    first_visit(rm, 'You are in a maze of twisty little crystal passages, all alike. Pip\'s glowing ears light up the walls.',
                flag='seen_maze')
door('maze3_D', 'maze3', (134, 142, 186, 158), (160, 162), BACK, 'hole in the floor', ('vein', 160, 150, BACK))

# ---- the crystal vein
hot('vein_v', 'vein', (0, 36, 319, 70), (160, 140), BACK, 'pickup', label='vein of star crystal')
s = G.script()
L = s.label()
s.iff('crystal_cut', L)
s.say('pilot', 'A vein of star crystal, hard as diamond. I would need a hammer.')
s.end()
s.here(L).say('pilot', 'A wide vein of star crystal. I have my piece.')
G.on('vein_v', 'look', s)
line('vein_v', 'pickup pull push', 'It is part of the vein. My bare hands are no match for star crystal.')
s = G.script()
L = s.label()
s.iff('crystal_cut', L)
s.cuton()
s.say('pilot', 'I swing the crystal hammer. CRACK!')
s.sound('thunder').setf('crystal_cut').pickup('starcrystal')
s.say('narrator', 'A perfect star crystal breaks out of the vein.')
s.cutoff()
s.end()
s.here(L).say('pilot', 'One star crystal is all the STARRAVEN needs.')
G.on('hammer', 'use', s, other='vein_v')
hot('rubble', 'vein', (100, 116, 230, 160), (160, 146), BACK, label='rubble')
search('rubble', 13, 'Broken rock and crystal. In the rubble...', 'Broken rock and crystal.', verbs='look pickup')
hot('pickaxe', 'vein', (226, 110, 264, 152), None, label='old pickaxe', look='An old pickaxe, rusted to the rock.')
first_visit('vein', 'You are in a glittering cavern. A wide vein of star crystal runs through the rock. Rubble lies '
            'everywhere.')
door('vn_up', 'vein', (0, 70, 24, 140), (24, 146), LEFT, 'way up', ('maze3', 160, 150, FRONT))

# Pip follows the pilot: he is in every room after the mine entrance, and talks
for rm, (x, y) in {'mineentry': (120, 156), 'maze1': (200, 150), 'maze2': (200, 150), 'maze3': (210, 150),
                   'vein': (200, 146), 'site': (120, 156)}.items():
    G.thing(f'pip_{rm}', rm, (0, 0, 1, 1), (x - 24, y), RIGHT, 'talk', label='Pip', actor='pip', state=0)
    simple(f'pip_{rm}', 'look', 'pilot', 'Pip. His ears glow like two lanterns.')
    s = G.script()
    s.say('pip', PIP_LINES[rm])
    s.say('narrator', 'Pip smiles.') if rm in ('mineentry', 'site') else None
    G.on(f'pip_{rm}', 'talk', s)
    enter = G.rooms[rm]['enter'] or G.script(f'{rm}_enter')
    G.rooms[rm]['enter'] = enter
    L = enter.label()
    enter.ifnf('pip_follows', L)
    enter.put('pip', rm, x, y, LEFT)
    enter.show(f'pip_{rm}')
    enter.here(L)
s = G.rooms['vein']['enter']
L = s.label()
s.iff('pip_joke', L)
s.setf('pip_joke')
s.say('pip', 'My grandpa always said: if someone says they\'ve seen asteroids with more brains than you, ask if they\'ve '
      'been looking in a mirror!')
s.say('narrator', 'Pip giggles.')
s.here(L)

# =================================================================== the start
chapter_start([], ('Chapter 9: The Star Heart', 'p11_card'), 'heart', 160, 156, BACK, music='p12')
default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {'vex': ('heart', 240, 150, 1)}
VARIANTS = {
    'machine': ('heart', {'machine': False}, {'machine': True}),
    'horn': ('westgal', {}, {'horn': True}),
    'esoldier': ('eastgal', {}, {'soldier_': True}),
    'cbars': ('catacomb', {}, {'bars': True}),
    'hammer': ('workshop', {}, {'hammer': True}),
    'nokite': ('mineentry', {}, {'kite': False}),
    'nopip': ('mineentry', {}, {'pip': False}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('heart', 'Heart chamber', 160, 156), ('westgal', 'West gallery', 160, 150),
             ('eastgal', 'East gallery', 160, 150), ('altar', 'Altar', 40, 160), ('catacomb', 'Catacombs', 160, 156),
             ('deadend', 'Dead end', 30, 156), ('site', 'Workshop', 60, 156), ('mineentry', 'Mines', 40, 156),
             ('maze3', 'Maze', 160, 160), ('vein', 'Vein', 160, 150)]
DEV_ITEMS = ['amulet', 'horn', 'hammer', 'kite', 'starcrystal', 'spikes', 'shell', 'chicken', 'ration', 'paper']
