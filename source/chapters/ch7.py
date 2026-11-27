"""World of Stronkie remake - Chapter Seven: Vex's Flagship (disk 7, the last).

The original game's Chapter 11 (Vex's Flagship), Chapter 12 (The Prison Deck),
Chapter 13 (The Bridge) and the Epilogue (Home Again). Every choice that mattered
on the disks before comes back here: the napkin (Roger), the Astro Chicken kick
(the badge), Ricky (the plasma spanner), LeChuckle's rematch (the pirates), the
wooden monkey (the secret holodeck), the glasses (the checkpoint) and the 16
star fragments (the true ending)."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p14', 'p15', 'p16', 'p17']
for nm, cost, col in (('edmund', 'edmund', 19), ('vex', 'vex', 25), ('roger', 'roger', 29)):
    ACTORS.append((nm, cost, col, ('rms', 1.0)))
    G.actors.append(nm)
    SPECIALS[cost] = []
LITE = ('edmund', 'vex', 'roger')
for n, c in (('cguard', 18), ('guards', 18), ('lrobot', 22), ('tron', 22), ('gguard', 18), ('lechuckle', 31),
             ('ricky', 20), ('pip', 24), ('pirates', 25)):
    add_actor(n, c)

# =================================================================== rooms
G.room('fhangar', 'fhangar', music='p14', walk=[FLOOR(130)])
G.room('fcorr', 'fcorr', music='p14', walk=[[(130, 100), (190, 100), (300, 167), (20, 167)]])
G.room('breakroom', 'breakroom', music='p14', walk=[FLOOR(142)])
G.room('laundry', 'laundry', music='p14', walk=[[(60, 136), (240, 136), (250, 167), (60, 167)]])
G.room('holodeck', 'holodeck', music='p14', walk=[FLOOR(142)])
G.room('lift', 'lift', music='p14', walk=[FLOOR(134)])
G.room('plift', 'stcorr', music='p15', walk=[[(128, 104), (192, 104), (300, 167), (20, 167)]])
G.room('cellblock', 'cellblock', music='p15', walk=[[(76, 124), (244, 124), (300, 167), (20, 167)]])
G.room('guardroom', 'guardroom', music='p15', walk=[FLOOR(140)])
G.room('records', 'quarters', music='p15', walk=[ROOM3D(104)])
G.room('pcontrol', 'control', music='p15', walk=[FLOOR(154)])
G.room('fbridge', 'fbridge', music='p16', walk=[FLOOR(140)])
G.room('comms', 'maproom', music='p16', walk=[[(206, 112), (296, 112), (319, 167), (186, 167)]])
G.room('cannon', 'cannon', music='p16', walk=[FLOOR(112)])
G.room('vexroom', 'vexroom', music='p16', walk=[FLOOR(132)])
G.room('podbay', 'airlock', music='p16', walk=[ROOM3D(116)])
G.room('egarden', 'egarden', music='p17', walk=[[(0, 112), (176, 112), (176, 167), (0, 167)]])
G.room('ehall', 'hall', music='p17',
       walk=[[(30, 118), (96, 106), (224, 106), (290, 118), (319, 140), (319, 167), (0, 167), (0, 140)]])
G.room('estudy', 'study', music='p17', walk=[FLOOR(110)])
BLOCK = {'fhangar': [[(58, 128), (152, 128), (152, 160), (58, 160)]],
         'estudy': [[(82, 104), (238, 104), (238, 154), (82, 154)]]}

# =================================================================== things you carry
G.thing('amulet', None, label='amulet', icon='amulet')
simple('amulet', 'look', 'pilot', 'My amulet. It glows softly, like the Star Heart.')
for nm, lab, ic, txt in (
        ('glasses', 'nose glasses', 'glasses', 'My trusty Groucho nose glasses.'),
        ('monkey', 'wooden monkey', 'monkey', 'My wooden monkey. It grins, as if it knows something.'),
        ('badge', 'guard\'s badge', 'badge', 'A badge with a raven on it. The photo could be anybody.'),
        ('uniform', 'black uniform', 'uniform', 'A black uniform of Vex\'s army. Three sizes too big.'),
        ('tshirt', 'T-shirt', 'tshirt', 'It says: I FOUND THE SECRET ROOM AND ALL I GOT WAS THIS LOUSY T-SHIRT.'),
        ('bucket', 'bucket of soapy water', 'mopbucket', 'Roger\'s bucket, full of very slippery soapy water.'),
        ('keycard', 'keycard', 'keycard', 'A black keycard with a silver raven.'),
        ('spanner', 'plasma spanner', 'spanner', 'A plasma spanner. It can jam anything.'),
        ('photo', 'old photo', 'photo', 'Two boys in front of Ravenmoor Manor, arm in arm. On the back: EDMUND AND '
                                         'VICTOR, BROTHERS FOREVER.')):
    G.thing(nm, None, label=lab, icon=ic)
    simple(nm, 'look', 'pilot', txt)
s = G.script()
L = s.label()
s.iff('uniform_on', L)
s.say('pilot', 'I pull the uniform on over my clothes. It is three sizes too big. I look like a tent. A black, '
      'military tent.')
s.setf('uniform_on').sound('click')
s.end()
s.here(L).say('pilot', 'I am already wearing it. Unfortunately.')
G.on('uniform', 'use', s)
line('glasses', 'use', 'I put on the nose glasses. Somewhere, Zak McKracken smiles.')

# =================================================================== CHAPTER 11: VEX'S FLAGSHIP
# ---- the hangar
hot('shuttles', 'fhangar', (30, 80, 104, 116), None, label='black shuttles',
    look='Rows of black shuttles with a raven on every tail.')
hot('shuttles2', 'fhangar', (222, 80, 292, 116), None, label='black shuttles',
    look='Rows of black shuttles with a raven on every tail.')
hot('fcrate', 'fhangar', (58, 112, 152, 160), None, label='cargo crate', look='The STARRAVEN hides behind this cargo crate.')
hot('raven7', 'fhangar', (104, 92, 130, 126), (160, 140), LEFT, 'talk', label='STARRAVEN',
    look='My STARRAVEN, hiding behind a cargo crate.')
s = G.script()
nova(s, 'We\'re in, pilot. Uncle Edmund must be on the prison deck. The only way down is the lift... and there are '
     'guards everywhere.')
G.on('raven7', 'talk', s)
hot('mdoor', 'fhangar', (136, 40, 180, 98), (158, 136), BACK, 'open', label='door with a monkey-shaped hollow',
    look='A steel door. In the middle is a hollow shaped like a small monkey.')
s = G.script('monkeydoor')
A, B = s.label(), s.label()
s.has('monkey', A)
s.say('pilot', 'The door with the monkey-shaped hollow will not open. What could fit in there?')
s.end()
s.here(A)
s.iff('holo_open', B)
s.cuton()
s.say('narrator', 'Your wooden monkey wriggles in your pocket... and fits perfectly into the hollow. The door slides open!')
s.sound('door').setf('holo_open')
s.cutoff()
s.here(B)
s.room('holodeck', 160, 160, BACK)
on('mdoor', 'open walk', s)
G.on('monkey', 'use', s, other='mdoor')
door('fh_east', 'fhangar', (300, 40, 319, 160), (300, 150), RIGHT, 'corridor', ('fcorr', 160, 160, BACK))
s = first_visit('fhangar', 'You are in the hangar of the IRON RAVEN. Black shuttles stand in rows. The STARRAVEN hides behind '
                'a cargo crate. In the north wall is a door with a strange monkey-shaped hollow. A corridor leads east.')
A, B = s.label(), s.label()
s.ifnf('glasses', A)
s.has('glasses', A)
s.pickup('glasses')
s.here(A)
s.ifnf('monkey', B)
s.has('monkey', B)
s.pickup('monkey')
s.here(B)

# ---- the secret holodeck
hot('sand', 'holodeck', (10, 140, 112, 166), (120, 152), LEFT, 'pickup', label='sand',
    look='Warm, soft sand. Something seems to be buried here.')
s = G.script()
L = s.label()
s.iff('tshirt_found', L)
s.cuton()
s.say('narrator', 'You dig in the warm sand and find a treasure chest! Inside: a T-shirt.')
s.pickup('tshirt').setf('tshirt_found')
s.say('narrator', 'It says: I FOUND THE SECRET ROOM AND ALL I GOT WAS THIS LOUSY T-SHIRT. Somewhere a jaunty tune starts '
      'to play...')
s.sound('score')
s.cutoff()
s.end()
s.here(L).say('pilot', 'Just sand now.')
on('sand', 'pickup use open', s)
hot('grogstand', 'holodeck', (112, 84, 192, 142), (150, 150), BACK, 'use', label='grog stand',
    look='A grog stand. The grog is holographic.')
line('grogstand', 'use pickup', 'It\'s holo-grog. It tastes of nothing at all. Much safer.')
hot('hsign', 'holodeck', (208, 116, 272, 140), (230, 150), BACK, label='sign',
    look='WELCOME TO MONKEY ISLAND. Somebody has crossed that out and written: STRONKIE BEACH.')
door('hd_out', 'holodeck', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the hangar', ('fhangar', 158, 136, FRONT))
first_visit('holodeck', 'A secret holodeck! Warm sand, palm trees and a grog stand.')

# ---- the corridor and the checkpoint
hot('cguard_t', 'fcorr', (180, 52, 216, 116), (176, 120), RIGHT, 'talk', label='guard at the checkpoint',
    look='A big guard with a big gun.')
careful('cguard_t', 'push pull', 'The guard is faster. Much faster.')
door('fc_lift', 'fcorr', (138, 40, 180, 92), (160, 104), BACK, 'checkpoint', ('lift', 40, 150, RIGHT),
     locked=('passed', lambda s: s.say('cguard', 'HALT! Uniform and badge, or you don\'t get past.')))
s = G.script()
L = s.label()
s.iff('passed', L)
s.say('cguard', 'Uniform and badge, or you don\'t get past.')
s.end()
s.here(L).say('cguard', 'Move along.')
G.on('cguard_t', 'talk', s)
s = G.script()
s.cuton()
s.say('pilot', 'I put on the nose glasses.')
s.say('cguard', 'Oh! Doctor Nose from Accounting! Go right in, sir!')
s.say('narrator', 'The guard salutes. The Groucho glasses work again.')
s.setf('passed').sound('score')
s.cutoff()
G.on('glasses', 'use', s, other='cguard_t')
G.on('glasses', 'give', s, other='cguard_t')
s = G.script()
L = s.label()
s.iff('uniform_on', L)
s.say('cguard', 'Nice badge. And where is your uniform, recruit?')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'The guard looks at your badge and your uniform, which is three sizes too big.')
s.say('cguard', 'Huh. New recruit? Go on through.')
s.setf('passed').sound('score')
s.cutoff()
G.on('badge', 'use', s, other='cguard_t')
G.on('badge', 'give', s, other='cguard_t')
door('fc_break', 'fcorr', (0, 20, 44, 150), (40, 150), LEFT, 'door to the break room', ('breakroom', 160, 160, BACK))
door('fc_laundry', 'fcorr', (276, 20, 319, 150), (280, 150), RIGHT, 'door to the laundry', ('laundry', 200, 156, LEFT))
door('fc_hangar', 'fcorr', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the hangar', ('fhangar', 290, 150, LEFT))
first_visit('fcorr', 'You are in a long black corridor. A guard stands at a checkpoint in front of the lift. Doors lead '
            'north and south.')

# ---- the break room
hot('bposter', 'breakroom', (188, 26, 238, 84), (210, 146), BACK, label='poster')
s = G.script()
s.say('pilot', 'INSULT OF THE WEEK: if a robot brags about its fast circuits, tell it: but your jokes still load from '
      'a datasette!')
s.setf('datasette_tip')
G.on('bposter', 'look', s)
hot('barcade', 'breakroom', (76, 26, 124, 98), (100, 146), BACK, 'use', label='Astro Chicken machine',
    look='An Astro Chicken machine. The high score table still shows Stronkie at the top.')
hot('bguards', 'breakroom', (70, 96, 158, 140), (110, 150), BACK, 'talk', label='guards',
    look='Two guards, glued to their Astro Chicken game. One of them has left his badge on the table.')
hot('badge_o', 'breakroom', (160, 122, 186, 136), (172, 150), BACK, 'pickup', label='badge', image='nobadge', state=1,
    look='A badge with a raven on it. The photo could be anybody.')
s = G.script()
s.say('guards', 'Hands off.')
s.say('narrator', 'A guard slaps your hand without looking up from the game.')
G.on('badge_o', 'pickup', s)
s = G.script()
A, B = s.label(), s.label()
s.iff('badge_got', B)
s.iff('kicked_chicken', A)
s.say('guards', 'Go away, we\'re trying to beat Stronkie\'s high score!')
s.say('narrator', 'The guards don\'t even look up.')
s.end()
s.here(A)
s.cuton()
s.say('guards', 'Wait... are you the one who beat Stronkie\'s high score on Astro Chicken?')
s.say('narrator', 'The guards go wild and run off to find a pen for an autograph. You pocket the badge.')
s.imgon('badge_o').hide('badge_o').pickup('badge').setf('badge_got')
s.cutoff()
s.end()
s.here(B).say('narrator', 'The guards are still looking for a pen.')
G.on('bguards', 'talk', s)
s = G.script()
L = s.label()
s.iff('badge_got', L)
s.cuton()
s.say('pilot', 'I give their Astro Chicken machine a good kick.')
s.sound('error')
s.say('narrator', 'It goes haywire: the chicken squawks at full volume! While the guards try to shut it up, you pocket '
      'the badge.')
s.imgon('badge_o').hide('badge_o').pickup('badge').setf('badge_got')
s.cutoff()
s.end()
s.here(L).say('pilot', 'Once is enough.')
G.on('barcade', 'push', s)
line('barcade', 'use', 'WAIT YOUR TURN! the guards snap.')
door('bk_out', 'breakroom', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the corridor', ('fcorr', 50, 150, RIGHT))
first_visit('breakroom', 'You are in the guards\' break room. Two guards are playing Astro Chicken. A badge lies on the '
            'table. A poster hangs on the wall.')

# ---- the laundry
hot('lrobot_t', 'laundry', (18, 86, 56, 162), (70, 150), LEFT, 'talk', label='laundry robot',
    look='A laundry robot. It folds uniforms and grumbles about the Insult-O-Tron.')
s = G.script()
s.say('lrobot', 'That Insult-O-Tron by the lift, always threatening to recycle everybody. I always say: at least I\'d be '
      'useful then, unlike you!')
s.setf('useful_tip')
G.on('lrobot_t', 'talk', s)
hot('lockers_l', 'laundry', (66, 14, 262, 100), None, label='lockers', look='Lockers full of black uniforms.')
hot('uniform_o', 'laundry', (142, 112, 180, 128), (160, 140), BACK, 'pickup', label='black uniform', image='luniform',
    state=3, look='A black uniform of Vex\'s army. Three sizes too big.')
s = G.script()
s.hide('uniform_o').imgoff('uniform_o').pickup('uniform')
s.say('narrator', 'The laundry robot doesn\'t even notice. Taken.')
G.on('uniform_o', 'pickup', s)
hot('lpile', 'laundry', (246, 126, 319, 166), (236, 156), RIGHT, label='pile of dirty laundry')
search('lpile', 14, 'Dirty uniforms and smelly socks. Under a smelly sock...', 'Dirty uniforms and smelly socks.',
       verbs='look pickup')
door('ld_out', 'laundry', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the corridor', ('fcorr', 270, 150, LEFT))
first_visit('laundry', 'You are in the laundry. A robot folds uniforms and mutters to itself. A big pile of dirty laundry '
            'fills the corner.')

# ---- the lift and the Insult-O-Tron 3000
hot('liftdoor', 'lift', (100, 8, 212, 126), (156, 140), BACK, 'walk', label='lift to the prison deck',
    image='tronoff', state=1)
hot('tron_t', 'lift', (126, 78, 188, 152), (100, 150), RIGHT, 'talk', label='Insult-O-Tron 3000', image='tron', state=3,
    look='A battle robot with a loudspeaker instead of a gun. It guards the lift.')
line('tron_t', 'push pull', 'I have no sword. The Insult-O-Tron only fights with words. Answer it!')
door('lf_west', 'lift', (0, 40, 18, 160), (18, 150), LEFT, 'way back to the checkpoint', ('fcorr', 160, 110, FRONT))
s = G.script('insults')
R1, R2, R3, W1, W2, W3, X, C1, C2, C3 = (s.label() for _ in range(10))
s.iff('tron2', R2)
s.iff('tron1', R1)
s.say('tron', 'I have seen asteroids with more brains than you!')
s.dialog([('Then you must have been looking in a mirror.', C1, None),
          ('So have I.', W1, None),
          ('Beep boop to you too.', W1, None),
          ('Er... bye.', X, None)])
s.here(W1)
s.sound('error')
s.say('tron', 'HA! PATHETIC!')
s.say('narrator', 'The Insult-O-Tron zaps your toes. That was not the right answer.')
s.end()
s.here(C1)
s.say('narrator', 'The robot\'s lights flicker.')
s.say('tron', 'ERROR... RECALCULATING.')
s.setf('tron1').sound('zap')
s.here(R1)
s.say('tron', 'My circuits are faster than your feet!')
s.dialog([('Maybe, but your jokes still load from a datasette.', C2, 'datasette_tip'),
          ('My feet are very fast.', W2, None),
          ('Your mother was a toaster.', W2, None),
          ('Er... bye.', X, None)])
s.here(W2)
s.sound('error')
s.say('tron', 'HA! PATHETIC!')
s.end()
s.here(C2)
s.say('narrator', 'The Insult-O-Tron smokes a little.')
s.setf('tron2').sound('zap')
s.here(R2)
s.say('tron', 'When I am done with you, you will be recycled!')
s.dialog([('At least I\'d be useful then, unlike you.', C3, 'useful_tip'),
          ('Recycling is good for the planet.', W3, None),
          ('I\'m not scared of you.', W3, None),
          ('Er... bye.', X, None)])
s.here(W3)
s.sound('error')
s.say('tron', 'HA! PATHETIC!')
s.end()
s.here(C3)
s.cuton()
s.say('narrator', 'The Insult-O-Tron 3000 shudders, sparks and shuts down with a sad little beep.')
s.sound('thunder').imgoff('tron_t').hide('tron_t').imgon('liftdoor').setf('tron_off')
s.say('narrator', 'The lift to the prison deck is free!')
s.cutoff()
s.here(X).end()
G.on('tron_t', 'talk', s)
s = G.script()
L = s.label()
s.iff('tron_off', L)
s.say('pilot', 'The Insult-O-Tron blocks the lift.')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'The lift drops down and down, deep into the IRON RAVEN...')
s.sound('hyper')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
spoken_card(s, 'Chapter 12: The Prison Deck', 'p14_card')
s.card('The lift drops into the prison deck. Red lights, cold steel... and somewhere, a prisoner is singing.', wait=True)
s.card('It sounds like Uncle Edmund. It also sounds terrible.', wait=True)
s.music('p15')
s.room('plift', 160, 156, BACK)
s.cutoff()
on('liftdoor', 'walk open', s)
s = first_visit('lift', 'You stand before the lift to the prison deck.')
s.sound('beep')
L = s.label()
s.iff('tron_met', L)
s.setf('tron_met')
s.say('narrator', 'A robot rolls in front of the lift.')
s.say('tron', 'I am the INSULT-O-TRON 3000! En garde, human: I have seen asteroids with more brains than you!')
s.here(L)

# =================================================================== CHAPTER 12: THE PRISON DECK
# ---- the lift lobby
G.thing('roger_t', 'plift', None, (190, 150), RIGHT, 'talk', label='janitor', actor='roger')
simple('roger_t', 'look', 'pilot', 'Roger the janitor, from Asteroid 42! He is mopping the prison deck now.')
hot('bucket_o', 'plift', (220, 140, 244, 162), (210, 156), RIGHT, 'pickup', label='bucket', state=0,
    look='Roger\'s bucket, full of very slippery soapy water.')
s = G.script()
s.hide('bucket_o').pickup('bucket')
G.on('bucket_o', 'pickup', s)
s = G.script()
A, B, C = s.label(), s.label(), s.label()
s.iff('roger_done', C)
s.iff('napkin_given', A)
s.say('roger', 'Do I know you? Nobody ever gives me a napkin, you know. Anyway, I\'m on my break.')
s.say('narrator', 'He wanders off and leaves his bucket behind.')
s.walk('roger', 312, 150)
s.put('roger', None, 0, 0)
s.hide('roger_t').show('bucket_o').setf('roger_done')
s.end()
s.here(A)
s.cuton()
s.say('roger', 'Hey, it\'s the napkin kid! I work here now. Better pay. You need the guard\'s keycard? Leave it to me.')
s.say('narrator', 'He mops the guardroom floor until it shines... CRASH! The guard slips and knocks himself out.')
s.say('roger', 'Here\'s the keycard. Now we\'re even, pal.')
s.pickup('keycard').setf('guard_out').setf('roger_done').setf('roger_mopped').setf('keycard_got')
s.cutoff()
s.end()
s.here(C)
s.say('roger', 'Good luck, pal!')
G.on('roger_t', 'talk', s)
door('pl_cells', 'plift', (128, 30, 192, 100), (160, 108), BACK, 'cellblock', ('cellblock', 160, 156, BACK))
door('pl_guard', 'plift', (290, 10, 319, 150), (276, 150), RIGHT, 'guardroom', ('guardroom', 40, 156, RIGHT))
door('pl_records', 'plift', (0, 10, 60, 150), (50, 150), LEFT, 'records room', ('records', 160, 160, BACK),
     locked=('keycard_got', 'The records room is locked. A card reader blinks red.'))
s = G.script('lift_up')
L = s.label()
s.iff('edmund_joined', L)
s.say('pilot', 'I won\'t leave without Uncle Edmund.')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'You and Uncle Edmund step into the lift.')
s.say('edmund', 'Bridge.')
s.say('narrator', 'The doors slide shut...')
s.sound('hyper')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
s.put('edmund', None, 0, 0)
spoken_card(s, 'Chapter 13: The Bridge', 'p15_card')
s.card('The lift doors open on the bridge of the IRON RAVEN. Vex stands at the great window, where the World of Stronkie '
       'glows below.', wait=True)
s.card('He turns. "Hello, brother," he says to Uncle Edmund. "And hello, kid. My star cannon is charged. One shot, and the '
       'Star Heart is mine."', wait=True)
s.music('p16')
s.room('fbridge', 100, 156, RIGHT)
s.cutoff()
hot('pl_lift', 'plift', (100, 158, 220, 167), (160, 162), FRONT, 'walk', label='lift up')
on('pl_lift', 'walk open', s)
first_visit('plift', 'You are in the lift lobby of the prison deck. Red lights blink. A janitor is mopping the floor. The '
            'cells are north, the guardroom east, the records room west.')

# ---- the cellblock
hot('fields', 'cellblock', (0, 10, 72, 156), (80, 150), LEFT, label='force fields',
    look='Humming force fields. Don\'t touch them!')
hot('fields2', 'cellblock', (78, 30, 120, 102), None, label='prisoners',
    look='Stronkies from the village, a few pirates, and in the last cell: Uncle Edmund!')
hot('fields3', 'cellblock', (200, 30, 242, 102), None, label='prisoners',
    look='Stronkies from the village, a few pirates, and in the last cell: Uncle Edmund!')
careful('fields', 'pickup push pull use', 'ZZZAP! The force field would throw me across the cellblock.')
hot('ecell', 'cellblock', (248, 10, 302, 156), (240, 150), RIGHT, 'talk', label='Uncle Edmund',
    look='Uncle Edmund, a bit thin but cheerful. He waves at me.')
s = G.script()
s.say('edmund', 'You\'re here! Find the control room and switch off these force fields!')
s.say('narrator', 'Uncle Edmund stops singing.')
G.on('ecell', 'talk', s)
G.thing('edmund_t', 'cellblock', None, (200, 150), RIGHT, 'talk', label='Uncle Edmund', actor='edmund', state=0)
simple('edmund_t', 'look', 'pilot', 'Uncle Edmund, a bit thin but cheerful.')
s = G.script()
L = s.label()
s.iff('edmund_joined', L)
s.say('narrator', 'Uncle Edmund hugs you.')
s.say('edmund', 'You came for me! So... you know now. Victor is my little brother. He was always jealous of the STARRAVEN.')
s.say('edmund', 'Let\'s stop him, together. The bridge is up the lift!')
s.setf('edmund_joined')
s.end()
s.here(L)
s.say('edmund', 'To the bridge! Up the lift!')
G.on('edmund_t', 'talk', s)
door('cb_out', 'cellblock', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the lobby', ('plift', 160, 110, FRONT))
s = first_visit('cellblock', 'You are in the cellblock. Behind humming force fields sit Stronkies, a few pirates... and '
                'Uncle Edmund, singing badly.')
L = s.label()
s.ifnf('fields_off', L)
s.iff('freed7', L)
s.setf('freed7').sound('score')
s.say('narrator', 'The prisoners stream out of their cells. The Stronkies cheer, and Uncle Edmund steps out, grinning.')
s.hide('ecell').hide('fields').put('edmund', 'cellblock', 250, 152, LEFT).show('edmund_t')
s.walk('edmund', 210, 150)
s.here(L)

# ---- the guardroom
hot('gdoor', 'guardroom', (138, 16, 182, 98), (160, 140), BACK, 'walk', label='door to the control room')
s = G.script()
L = s.label()
s.iff('guard_out', L)
s.say('gguard', 'Nobody gets into the control room!')
s.say('narrator', 'The guard jumps up.')
s.end()
s.here(L)
s.room('pcontrol', 60, 162, RIGHT)
on('gdoor', 'walk open', s)
hot('gout_t', 'guardroom', (174, 132, 228, 150), None, label='guard', image='gout', state=0,
    look='He is out cold, snoring.')
hot('gguard_t', 'guardroom', (184, 100, 210, 142), (170, 150), RIGHT, 'talk', label='guard at his desk', image='ggard',
    state=3, look='A guard with a keycard on his belt. He watches the north door.')
careful('gguard_t', 'push pull', 'The guard is much bigger than me. Much, much bigger.')
s = G.script()
s.say('gguard', 'Move along, janitor.')
G.on('gguard_t', 'talk', s)
hot('kc_o', 'guardroom', (220, 144, 236, 152), (230, 156), RIGHT, 'pickup', label='keycard', state=0,
    look='A black keycard with a silver raven.')
s = G.script()
s.hide('kc_o').pickup('keycard').setf('keycard_got')
G.on('kc_o', 'pickup', s)
line('gguard_t', 'pickup', 'The guard growls: "Hands off my keycard."')
s = G.script()
s.cuton()
s.say('pilot', 'I pour the soapy water all over the guardroom floor.')
s.drop('bucket')
s.say('narrator', 'The guard jumps up, slips... CRASH! He knocks himself out. His keycard skids across the floor.')
s.sound('thunder').imgoff('gguard_t').hide('gguard_t').imgon('gout_t').show('gout_t').show('kc_o').setf('guard_out')
s.cutoff()
G.on('bucket', 'use', s, other='gguard_t')
G.on('bucket', 'use', s, other='gdoor')
door('gr_out', 'guardroom', (0, 40, 20, 160), (20, 156), LEFT, 'way back to the lobby', ('plift', 270, 150, LEFT))
s = first_visit('guardroom', 'You are in the guardroom. A door leads north to the control room.')
L = s.label()
s.ifnf('roger_mopped', L)
s.iff('gr_fixed', L)
s.setf('gr_fixed').imgoff('gguard_t').hide('gguard_t').imgon('gout_t').show('gout_t')
s.here(L)

# ---- the records room
hot('cabinets', 'records', (58, 32, 154, 98), (106, 112), BACK, label='filing cabinets')
search('cabinets', 15, 'Drawers full of files on every prisoner... and one drawer marked: PRIVATE. In it...',
       'Drawers full of files on every prisoner.', verbs='look open pickup')
hot('vfile', 'records', (194, 44, 256, 94), (226, 112), BACK, 'open', label='file on the desk',
    look='A file with a red stamp: TOP SECRET. COMMANDER VEX.')
s = G.script()
s.cuton()
s.say('narrator', 'The file reads: COMMANDER VEX. REAL NAME: VICTOR RAVENMOOR. YOUNGER BROTHER OF EDMUND RAVENMOOR.')
s.say('narrator', 'THROWN OUT OF THE FAMILY FOR STEALING THE PLANS OF THE STARRAVEN. WANTED ON SEVEN WORLDS...')
s.sound('thunder')
s.say('pilot', 'Vex is my other uncle!')
s.setf('vex_known')
s.cutoff()
on('vfile', 'open pickup use', s)
door('rc_out', 'records', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the lobby', ('plift', 60, 150, RIGHT))
first_visit('records', 'You are in the records room. Filing cabinets line the walls. One file lies open on the desk.')

# ---- the prison control room
hot('pscreens', 'pcontrol', (64, 18, 254, 60), None, label='screens', look='Screens show every cell. Uncle Edmund is '
    'still singing.')
hot('plever', 'pcontrol', (278, 48, 314, 106), (290, 162), BACK, 'pull', label='big lever',
    look='A big lever with a card reader: FORCE FIELDS ON / OFF.')
s = G.script()
A, B = s.label(), s.label()
s.iff('fields_off', B)
s.has('keycard', A)
s.say('pilot', 'The card reader blinks red. I need a keycard.')
s.end()
s.here(A)
s.cuton()
s.say('pilot', 'I swipe the keycard and pull the big lever.')
s.sound('zap').setf('fields_off')
s.say('narrator', 'All over the prison deck the force fields flicker and die. The prisoners cheer!')
s.cutoff()
s.end()
s.here(B).say('pilot', 'The force fields are off.')
on('plever', 'pull push', s)
G.on('keycard', 'use', s, other='plever')
door('pc_out', 'pcontrol', (0, 100, 26, 167), (12, 162), LEFT, 'way back to the guardroom', ('guardroom', 160, 146, FRONT))
first_visit('pcontrol', 'You are in the prison control room. Screens show every cell. A big lever controls the force fields.')

# =================================================================== CHAPTER 13: THE BRIDGE
hot('fwindow', 'fbridge', (190, 10, 300, 100), None, label='great window',
    look='The World of Stronkie, blue and green and beautiful. And right in the cannon\'s sights.')
hot('vex_b', 'fbridge', (138, 30, 184, 138), (120, 150), RIGHT, 'talk', label='Vex',
    look='My other uncle, Victor Ravenmoor. He has Edmund\'s eyes, but not his smile.')
careful('vex_b', 'push pull', 'Vex would sidestep and his guards would do the rest.')
hot('edmund_b', 'fbridge', (14, 62, 60, 158), (70, 156), LEFT, 'talk', label='Uncle Edmund',
    look='Uncle Edmund looks at his brother with sad eyes.')
s = G.script()
s.say('edmund', 'When we were boys, Victor kept a photo of us two everywhere he went. I wonder if he still does.')
s.say('narrator', 'Uncle Edmund whispers.')
G.on('edmund_b', 'talk', s)
s = G.script()
L = s.label()
s.iff('cannon_off', L)
s.say('vex', 'You have no idea, kid. Edmund got everything: the manor, the STARRAVEN, the glory. Now it\'s my turn.')
s.end()
s.here(L)
s.say('vex', 'So what now, kid? What could you possibly say to me?')
s.say('narrator', 'Vex stares at his dead cannon.')
G.on('vex_b', 'talk', s)
door('fb_radio', 'fbridge', (0, 20, 14, 160), (16, 156), LEFT, 'radio room', ('comms', 250, 150, LEFT))
hot('pirates_b', 'fbridge', (236, 120, 288, 158), (220, 156), RIGHT, 'talk', label='three space pirates', image='bpirates',
    state=1, look='LeChuckle\'s pirates, blocking the way to the cannon room.')
G.objects['pirates_b']['state'] = 0
s = G.script()
s.say('pirates', 'ARRR! Nobody passes!')
G.on('pirates_b', 'talk', s)
careful('pirates_b', 'push pull', 'Three against one? Not a good idea.')
door('fb_cannon', 'fbridge', (300, 20, 319, 92), (300, 150), RIGHT, 'cannon room', ('cannon', 30, 150, RIGHT))
door('fb_vex', 'fbridge', (100, 158, 220, 167), (160, 162), FRONT, 'way to Vex\'s quarters', ('vexroom', 160, 156, BACK))
door('fb_pods', 'fbridge', (280, 94, 304, 158), (276, 156), RIGHT, 'ladder down to the pod bay', ('podbay', 40, 150, RIGHT))
s = G.script('fb_in')
A, B, C = s.label(), s.label(), s.label()
s.iff('radio_done', A)
s.setf('radio_done')
s.say('narrator', 'You are on the bridge of the IRON RAVEN. Vex stands at the great window. Uncle Edmund stays close '
      'behind you.')
s.say('vex', 'LeChuckle! Get over here and deal with these pests!')
s.say('narrator', 'Vex grabs his radio.')
s.iff('said_grandmother', B)
s.say('lechuckle', 'Arrr, Vex, we\'re coming!')
s.sound('door')
s.say('narrator', 'The SPACE MONKEY docks and three pirates burst onto the bridge. They block the way to the cannon room!')
s.setf('pirates_here').show('pirates_b').imgon('pirates_b')
s.end()
s.here(B)
s.say('lechuckle', 'Sorry, Vex. That kid out-insulted me fair and square. We\'re staying out of this. ARRR!')
s.say('narrator', 'Vex throws his radio across the bridge.')
s.here(A)
G.rooms['fbridge']['enter'] = s
s = G.script()
L = s.label()
s.ifnf('pirates_here', L)
s.say('narrator', 'Three pirates block the way to the cannon room, waving their cutlasses.')
s.end()
s.here(L)
s.room('cannon', 30, 150, RIGHT)
G.objects['fb_cannon']['handlers'] = []
on('fb_cannon', 'walk open', s)

# the photo: the end of Chapter 13
s = G.script('photo_end')
L = s.label()
s.iff('cannon_off', L)
s.say('vex', 'Sentimental nonsense! My cannon is still ready to fire!')
s.say('narrator', 'Vex snarls.')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'You hold up the old photo. Vex stares at it for a long time. His hand shakes.')
s.say('vex', 'Brothers forever... I... I had forgotten.')
s.say('narrator', 'He drops his weapon. Uncle Edmund puts an arm around him.')
s.say('edmund', 'Come home, Victor.')
s.sound('score')
s.say('narrator', 'The crew of the IRON RAVEN throws down their weapons. It is over.')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
spoken_card(s, 'Epilogue: Home Again', 'p16_card')
s.card('Weeks later, the STARRAVEN lands in the garden of Ravenmoor Manor. The storm is long gone.', wait=True)
s.card('Uncle Edmund and Victor - not Vex any more - climb out, arguing about who gets the bigger room. Pip waves from '
       'the hatch: he wanted to see Earth.', wait=True)
s.music('p17')
s.put('edmund', 'ehall', 100, 124, RIGHT)
s.put('vex', 'ehall', 220, 124, LEFT)
s.room('egarden', 80, 150, RIGHT)
s.cutoff()
G.on('photo', 'use', s, other='vex_b')
G.on('photo', 'give', s, other='vex_b')

# ---- the radio room
hot('radio', 'comms', (56, 30, 206, 140), (210, 140), LEFT, 'talk', label='big radio',
    look='A big radio. A label says: CHANNEL 1 - THE SPACE MONKEY.')
s = G.script()
A, B, M, X = (s.label() for _ in range(4))
s.iff('pirates_gone', B)
s.ifnf('pirates_here', B)
s.say('pilot', 'The radio is set to the SPACE MONKEY. What would make LeChuckle look the other way?')
s.dialog([('LeChuckle! Look behind you, a three-headed monkey!', M, None),
          ('LeChuckle, please go home.', A, None),
          ('Never mind.', X, None)])
s.here(A)
s.say('lechuckle', 'ARRR! Never!')
s.end()
s.here(M)
s.cuton()
s.say('lechuckle', 'WHERE?!')
s.say('narrator', 'Out of the window you see the SPACE MONKEY spin around... and around... and tumble off into space.')
s.say('narrator', 'The pirates run back to their ship.')
s.imgoff('pirates_b').hide('pirates_b').setf('pirates_gone')
s.clrf('pirates_here')
s.cutoff()
s.end()
s.here(B)
s.say('pilot', 'Static. Nobody to talk to.')
s.here(X).end()
on('radio', 'talk use', s)
door('cm_out', 'comms', (296, 30, 319, 160), (290, 150), RIGHT, 'way back to the bridge', ('fbridge', 30, 156, RIGHT))
first_visit('comms', 'You are in the radio room. A big radio crackles on the table.')

# ---- the cannon room
hot('bigcannon', 'cannon', (40, 26, 300, 98), None, label='star cannon',
    look='The star cannon hums, aimed at the World of Stronkie.')
hot('ccontrols', 'cannon', (60, 126, 262, 154), (160, 140), BACK, 'look', label='cannon controls')
s = G.script()
L = s.label()
s.iff('cannon_off', L)
s.say('pilot', 'The star cannon\'s controls glow red. One good jam in the right place...')
s.end()
s.here(L).say('pilot', 'Dead and dark. Good.')
G.on('ccontrols', 'look', s)
line('ccontrols', 'push pull use', 'The controls are locked. I need to jam them with something.')
s = G.script()
s.cuton()
s.say('pilot', 'I jam the plasma spanner into the cannon\'s controls.')
s.drop('spanner').sound('zap').setf('cannon_off')
s.say('narrator', 'Sparks fly! The star cannon powers down with a sad whine.')
s.cutoff()
G.on('spanner', 'use', s, other='ccontrols')
G.on('spanner', 'use', s, other='bigcannon')
door('cn_out', 'cannon', (0, 40, 18, 160), (18, 150), LEFT, 'way back to the bridge', ('fbridge', 290, 150, LEFT))
first_visit('cannon', 'You are in the cannon room. The star cannon hums, aimed at the World of Stronkie. Its controls glow red.')

# ---- Vex's quarters
hot('vbed', 'vexroom', (8, 102, 122, 128), (130, 140), LEFT, label='bed')
search('vbed', 16, 'A hard, narrow bed. Very neat. Under the pillow...', 'A hard, narrow bed. Very neat.',
       verbs='look pickup pull')
hot('photo_o', 'vexroom', (222, 96, 254, 132), (226, 140), BACK, 'pickup', label='old photo', image='nophoto', state=1,
    look='An old photo in a silver frame.')
s = G.script()
s.imgon('photo_o').hide('photo_o').pickup('photo')
G.on('photo_o', 'pickup', s)
hot('vframe', 'vexroom', (160, 24, 232, 82), None, label='frame', look='An empty frame. Vex is not a man of art.')
door('vx_out', 'vexroom', (100, 158, 220, 167), (160, 162), FRONT, 'way back to the bridge', ('fbridge', 160, 156, BACK))
first_visit('vexroom', 'You are in Vex\'s quarters. A hard bed, a black desk... and on the desk, an old photo in a silver frame.')

# ---- the pod bay
hot('pods', 'podbay', (116, 12, 202, 108), (160, 126), BACK, 'walk', label='escape pods',
    look='Round escape pods with a big red launch button inside.')
careful('pods', 'walk open use', 'Into a pod, alone, with no way to steer? Bye!')
hot('toolbox', 'podbay', (250, 58, 292, 118), (270, 130), BACK, 'open', label='rusty toolbox',
    look='A rusty toolbox. It isn\'t locked.')
s = G.script()
L = s.label()
s.iff('spanner_got', L)
s.say('pilot', 'I open the toolbox. Among the rusty tools lies a plasma spanner.')
s.pickup('spanner').setf('spanner_got')
s.end()
s.here(L).say('pilot', 'Just rusty tools now.')
on('toolbox', 'open pickup', s)
door('pb_up', 'podbay', (0, 30, 24, 160), (30, 150), LEFT, 'ladder up to the bridge', ('fbridge', 270, 156, LEFT))
s = first_visit('podbay', 'You are in the pod bay. Round escape pods line the wall. A rusty toolbox stands in the corner.')
L = s.label()
s.ifnf('untied_crewman', L)
s.iff('ricky_came', L)
s.setf('ricky_came')
s.sound('door')
s.say('narrator', 'An escape pod docks with a CLANG. Out climbs... Ensign Ricky, still in his red shirt!')
s.say('ricky', 'Told you I\'d be there! Here, a plasma spanner. It can jam anything.')
s.pickup('spanner').setf('spanner_got')
s.here(L)

# =================================================================== EPILOGUE: HOME AGAIN
hot('eship', 'egarden', (176, 18, 264, 166), (170, 150), RIGHT, 'talk', label='STARRAVEN', look='Home, safe and sound.')
s = G.script()
nova(s, 'Welcome home, pilot.')
G.on('eship', 'talk', s)
hot('epip', 'egarden', (136, 124, 164, 162), (120, 156), RIGHT, 'talk', label='Pip',
    look='Pip is very excited about butterflies.')
s = G.script()
s.say('pip', 'Earth has only ONE sun! How do you even see anything?')
G.on('epip', 'talk', s)
door('eg_manor', 'egarden', (116, 34, 206, 84), (150, 116), BACK, 'Ravenmoor Manor', ('ehall', 160, 160, BACK))
first_visit('egarden', 'You are in the garden of Ravenmoor. The STARRAVEN stands on the lawn, and Pip chases butterflies. '
            'The manor lies north.')
G.thing('edmund_h', 'ehall', None, (100, 124), RIGHT, 'talk', label='Uncle Edmund', actor='edmund')
G.thing('victor_h', 'ehall', None, (220, 124), LEFT, 'talk', label='Victor', actor='vex')
simple('edmund_h', 'look', 'pilot', 'Two brothers and a crooked portrait. It\'s good to see them together.')
simple('victor_h', 'look', 'pilot', 'Victor Ravenmoor, no longer Commander Vex. He looks rather sheepish.')
s = G.script()
s.say('edmund', 'Go and have a look at my star globe in the study. Bring your star fragments.')
G.on('edmund_h', 'talk', s)
s = G.script()
s.say('vex', 'I\'m sorry, kid. For everything.')
s.say('edmund', 'He\'s doing the dishes for the next hundred years.')
G.on('victor_h', 'talk', s)
hot('eportrait', 'ehall', (98, 32, 118, 58), (108, 112), BACK, label='family portrait',
    look='An old family portrait, back on the wall. Two boys, arm in arm.')
door('eh_study', 'ehall', (118, 30, 202, 104), (160, 112), BACK, 'stairs up to the study', ('estudy', 160, 160, BACK))
door('eh_out', 'ehall', (110, 160, 210, 167), (160, 165), FRONT, 'front door', ('egarden', 150, 120, FRONT))
first_visit('ehall', 'You are in the grand hall. Uncle Edmund and Victor are hanging an old family portrait back on the wall. '
            'The study is north.')
hot('globe', 'estudy', (84, 96, 238, 154), (160, 162), BACK, 'use', label='desk with the star globe',
    look='Uncle Edmund\'s desk. The brass star globe beside it has sixteen empty little hollows in it, like stars.')
hot('ewindow', 'estudy', (126, 14, 194, 88), None, label='window', look='Moonlight. And somewhere up there: Stronkie.')
door('es_out', 'estudy', (0, 100, 24, 167), (12, 156), LEFT, 'door to the hall', ('ehall', 160, 116, FRONT))
first_visit('estudy', 'You are in Uncle Edmund\'s study. Moonlight falls on the big oak desk. A brass star globe stands '
            'beside it.')
s = G.script('the_end')
PART, NONE, HAS = s.label(), s.label(), s.label()
s.has('fragments', HAS)
s.cuton()
s.jmp(NONE)
s.here(HAS)
for n in range(1, 17):
    s.ifnf(f'frag{n}', PART)
s.cuton()
s.say('narrator', 'You lay all sixteen star fragments on the desk. One by one they rise into the air and form a glowing '
      'star map...')
s.sound('hyper')
s.say('narrator', 'It shows a world nobody has ever seen.')
s.say('edmund', 'The other Stronkie world. The one from the old legends!')
nova(s, 'Course plotted, pilot. Whenever you\'re ready.', 'p17_m04')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
s.music('title')
s.card('THE TRUE ENDING!', wait=True)
s.card('*Congratulations!', wait=True)
s.card('The World of Stronkie will return...', wait=True)
s.card('World of Stronkie remake. Created By Mark Stronks, Stronkie Soft.', wait=True)
s.endgame()
s.here(PART)
s.cuton()
s.say('narrator', 'You lay your star fragments on the desk. They flicker... but nothing happens. Some pieces are still missing.')
s.here(NONE)
s.say('edmund', 'Home at last. Thank you, kid.')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
s.music('title')
s.card('THE END. (Find all 16 star fragments for the true ending!)', wait=True)
s.card('*Congratulations!', wait=True)
s.card('World of Stronkie remake. Created By Mark Stronks, Stronkie Soft.', wait=True)
s.endgame()
G.on('fragments', 'use', s, other='globe')
G.on('globe', 'use', s)
G.on('globe', 'push', s)

# =================================================================== the start
chapter_start(['The STARRAVEN slips into the hangar of Vex\'s flagship, the IRON RAVEN, right behind a cargo shuttle.'],
              ('Chapter 11: Vex\'s Flagship', 'p13_card'), 'fhangar', 180, 150, LEFT, music='p14')
default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {'roger': ('plift', 220, 150, 1)}
VARIANTS = {
    'nobadge': ('breakroom', {}, {'badge': False}),
    'luniform': ('laundry', {}, {'uniform': True}),
    'tron': ('lift', {}, {'tron': True}),
    'tronoff': ('lift', {}, {'tron_off': True}),
    'ggard': ('guardroom', {}, {'guard': True}),
    'gout': ('guardroom', {}, {'out': True}),
    'bpirates': ('fbridge', {}, {'pirates': True}),
    'nophoto': ('vexroom', {}, {'photo': False}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('fhangar', 'Hangar', 180, 150), ('fcorr', 'Corridor', 160, 156), ('breakroom', 'Break room', 160, 156),
             ('laundry', 'Laundry', 200, 156), ('lift', 'Lift', 40, 150), ('plift', 'Prison deck', 160, 156),
             ('guardroom', 'Guardroom', 40, 156), ('fbridge', 'Bridge', 100, 156), ('podbay', 'Pod bay', 40, 150),
             ('estudy', 'Epilogue', 160, 160)]
DEV_ITEMS = ['badge', 'uniform', 'glasses', 'monkey', 'keycard', 'bucket', 'spanner', 'photo', 'fragments', 'amulet',
             'horn', 'spikes', 'shell', 'chicken', 'ration', 'paper']
