"""World of Stronkie remake - Chapter Three: Asteroid 42 (disk 3).

The original game's Chapter 3 (Asteroid 42: the space port) and Chapter 4
(Space Pirates: the SPACE MONKEY). Keepsake of this disk: the rubber chicken
with a pulley in the middle. Choices that matter later: the napkin for Roger,
the kick for Astro Chicken, untying Ricky and LeChuckle's rematch."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p06', 'p07']
for n, c in (('roger', 29), ('stan', 19), ('larry', 22), ('pirates', 25), ('band', 31), ('lechuckle', 31),
             ('ricky', 20), ('parrot', 31), ('barman', 26)):
    add_actor(n, c)
ACTORS.append(('pguard', 'pirate', 25, ('rms', 1.0)))
G.actors.append('pguard')
SPECIALS['pirate'] = []
LITE = ('pirate',)

# =================================================================== rooms
G.room('pad', 'pad', music='p06', walk=[[(10, 124), (310, 124), (319, 167), (0, 167)]])
G.room('plaza', 'plaza', music='p06', walk=[FLOOR(112)])
G.room('bar', 'bar', music='p06', walk=[FLOOR(136)])
G.room('stan', 'stan', music='p06', walk=[ROOM3D(104, 30)])
G.room('alley', 'alley', music='p06', walk=[[(40, 136), (280, 136), (300, 167), (20, 167)]])
G.room('backroom', 'backroom', music='p06', walk=[ROOM3D(140, 30)])
G.room('pcockpit', 'pcockpit', music='p07', walk=[[(30, 156), (290, 156), (290, 167), (30, 167)]])
G.room('pairlock', 'pairlock', music='p07', walk=[ROOM3D(116)])
G.room('deck', 'deck', music='p07', walk=[FLOOR(112)])
G.room('cabin', 'cabin', music='p07', walk=[[(0, 152), (60, 152), (60, 167), (0, 167)],
                                            [(256, 152), (319, 152), (319, 167), (256, 167)]])
G.room('pengine', 'pengine', music='p07', walk=[FLOOR(114)])
BLOCK = {'plaza': [[(106, 110), (206, 110), (206, 142), (106, 142)]],
         'stan': [[(58, 104), (120, 104), (120, 144), (58, 144)]],
         'pad': [[(94, 124), (150, 124), (150, 142), (94, 142)]],
         'pengine': [[(44, 114), (108, 114), (108, 146), (44, 146)], [(210, 114), (258, 114), (258, 146), (210, 146)]]}

# =================================================================== things you carry
for nm, lab, ic, txt in (
        ('burger', 'free sample burger', 'burger', 'A small grey burger. It is still twitching a little.'),
        ('coin', 'buckazoid coin', 'coin', 'One shiny buckazoid. Not enough for fuel, but it\'s a start.'),
        ('cash', 'fifty buckazoids', 'cash', 'Fifty shiny buckazoids. Enough for a fuel cell!'),
        ('napkin', 'greasy napkin', 'napkin', 'Scribbled on it: "LEFTY\'S BACK ROOM. PASSWORD: KEN SENT ME. '
                                              'DON\'T TELL ANYONE. - L."'),
        ('fuelcell', 'fuel cell', 'fuelcell', 'A glowing green fuel cell. Enough to get us to Stronkie.'),
        ('bigkey', 'big brass key', 'brasskey', 'A big brass key. A tag says: TRACTOR BEAM. DO NOT LOSE. AGAIN.')):
    G.thing(nm, None, label=lab, icon=ic)
    if nm != 'napkin':
        simple(nm, 'look', 'pilot', txt)
s = G.script()
s.say('pilot', 'Scribbled on it: "LEFTY\'S BACK ROOM. PASSWORD: KEN SENT ME. DON\'T TELL ANYONE. - L."')
s.setf('napkin_read')
G.on('napkin', 'look', s)
s = G.script()
s.say('pilot', 'I take one tiny bite. It tastes of space and regret. Maybe somebody hungrier would like it.')
G.on('burger', 'use', s)
s = G.script()
s.say('pilot', 'A rubber chicken with a pulley in the middle. The pulley would fit on a cable...')
G.on('chicken', 'look', s)

# =================================================================== CHAPTER 3: ASTEROID 42
# ---- landing pad 42
hot('ship42', 'pad', (86, 20, 154, 120), (160, 140), LEFT, 'walk', label='STARRAVEN',
    look='The fuel hatch is open. The gauge reads: EMPTY. Not even fumes.')
hot('roger', 'pad', (204, 104, 232, 158), (192, 152), RIGHT, 'talk', label='janitor',
    look='His name tag says: ROGER W., JANITOR, 2ND CLASS. He looks like a man who has saved the galaxy '
         'a few times and got a mop for it. His stomach rumbles.')
line('roger', 'pickup pull push', 'Roger hugs his mop. "Get your own!"')
hot('lamps_p', 'pad', (20, 50, 44, 110), None, label='lamp', look='A landing light. It blinks for nobody.')
door('pd_port', 'pad', (250, 50, 319, 118), (290, 130), RIGHT, 'space port', ('plaza', 160, 160, BACK))
s = G.script()
A, B, C, D, E = (s.label() for _ in range(5))
s.here(A)
s.iff('roger_fed', B)
s.say('roger', 'Name\'s Roger. Janitor. I\'ve saved the universe more times than I can count, and I still get '
      'stuck with the mop. And I\'m starving.')
s.end()
s.here(B)
s.iff('napkin_given', C)
s.say('roger', 'That burger was a bit messy. You wouldn\'t have a napkin, would you, pal?')
s.end()
s.here(C)
s.say('roger', 'Thanks for the burger, pal. Good luck out there!')
G.on('roger', 'talk', s)
s = G.script()
s.cuton()
s.say('pilot', 'Here, Roger. A free sample.')
s.drop('burger').setf('roger_fed').pickup('coin')
s.say('narrator', 'Roger wolfs down the burger in two bites.')
s.say('roger', 'Thanks, pal! I haven\'t eaten since the Sariens blew up my last ship. Here, I found this while mopping.')
s.say('narrator', 'He hands you a shiny buckazoid coin and wipes his chin on his sleeve.')
s.cutoff()
G.on('burger', 'give', s, other='roger')
G.on('burger', 'use', s, other='roger')
s = G.script()
L = s.label()
s.iff('roger_fed', L)
s.say('roger', 'A napkin? I\'d need something to eat first, pal.')
s.end()
s.here(L)
s.cuton()
s.drop('napkin').setf('napkin_given')
s.say('roger', 'A napkin! Nobody has ever been this nice to me.')
s.say('roger', '"Ken sent me"? Weird. If you ever need a favour, pal, Roger owes you one!')
s.cutoff()
G.on('napkin', 'give', s, other='roger')
G.on('napkin', 'use', s, other='roger')
s = G.script()
L = s.label()
s.iff('fuel_in', L)
s.cuton()
s.say('pilot', 'I plug the fuel cell into the STARRAVEN.')
s.drop('fuelcell').setf('fuel_in').sound('beep')
s.say('narrator', 'The gauge jumps to FULL.')
nova(s, 'Mmm, premium. Thank you, pilot. Ready when you are.', 'p06_m15')
s.cutoff()
s.here(L).end()
G.on('fuelcell', 'use', s, other='ship42')
s = G.script('board42')
A, B = s.label(), s.label()
s.iff('fuel_in', A)
nova(s, 'The tank is empty, pilot. We won\'t get off this rock without a fuel cell.', 'p06_m18')
s.end()
s.here(A)
s.has('chicken', B)
s.say('stan', 'HEY! Don\'t forget your free chicken!')
s.say('narrator', 'Stan\'s voice echoes across the pad.')
s.end()
s.here(B)
s.cuton()
s.say('narrator', 'You climb aboard.')
s.room('pcockpit', 0, 0)
s.put('pilot', None, 0, 0)
nova(s, 'Fuel: full. Chicken: on board. Course: the World of Stronkie.', 'p06_m16')
s.sound('launch')
s.say('narrator', 'The STARRAVEN lifts off from Asteroid 42. On the pad, Roger waves his mop goodbye...')
s.fade(0)
s.room('cards', 0, 0)
spoken_card(s, 'Chapter 4: Space Pirates', 'p06_card')
s.card('Halfway to Stronkie, a ship drops out of hyperspace right in front of you: an old sailing ship with solar '
       'sails and a black flag.', wait=True)
s.card('A green tractor beam grabs the STARRAVEN. A voice booms over the radio: "This is Captain LeChuckle of the '
       'SPACE MONKEY! Hand over yer star chart, or walk the space plank!"', wait=True)
s.music('p07')
s.room('pcockpit', 160, 162, BACK)
s.cutoff()
on('ship42', 'walk open use', s)
s = G.script()
nova(s, 'Find us a fuel cell, pilot. Try the shops on the plaza.', 'p06_m11')
G.on('ship42', 'talk', s)
first_visit('pad', 'You are on landing pad 42 of a dusty asteroid space port. The STARRAVEN stands here with its fuel '
            'hatch open. A janitor is mopping the pad. The port lies north.')

# ---- the plaza
hot('stand', 'plaza', (108, 96, 206, 140), (156, 148), BACK, 'pickup', label='Monolith Burger stand',
    look='MONOLITH BURGER - now with 2001 secret sauces! A sign says: FREE SAMPLES. TAKE ONE.')
s = G.script()
L = s.label()
s.has('burger', L)
s.iff('roger_fed', L)
s.say('pilot', 'One free sample, please.')
s.pickup('burger')
s.end()
s.here(L).say('pilot', 'One free sample is enough. They are still twitching.')
on('stand', 'pickup use', s)
door('pl_bar', 'plaza', (20, 40, 72, 110), (46, 120), BACK, 'SCUMM BAR', ('bar', 290, 150, LEFT))
door('pl_stan', 'plaza', (230, 40, 300, 112), (264, 120), BACK, 'Stan\'s Pre-Owned Starships', ('stan', 50, 150, RIGHT))
door('pl_alley', 'plaza', (138, 50, 174, 94), (126, 116), BACK, 'dark alley', ('alley', 160, 160, BACK))
door('pl_pad', 'plaza', (100, 156, 220, 167), (160, 160), FRONT, 'way back to the landing pad', ('pad', 280, 140, LEFT))
first_visit('plaza', 'You are on the plaza of Space Port 42. The SCUMM BAR is west, Stan\'s Pre-Owned Starships east, '
            'a dark alley north. A Monolith Burger stand hands out free samples.')

# ---- the SCUMM BAR
hot('arcade', 'bar', (56, 42, 84, 112), (70, 142), BACK, 'use', label='Astro Chicken arcade game')
s = G.script()
L = s.label()
s.iff('kicked_chicken', L)
s.say('pilot', 'ASTRO CHICKEN! The high score table: 1. STRONKIE 999999. 2. ROGER 000042. 3. LARRY 000001.')
s.end()
s.here(L).say('pilot', 'The high score table: 1. ME 1000000. 2. STRONKIE 999999. 3. ROGER 000042.')
G.on('arcade', 'look', s)
s = G.script()
s.say('narrator', 'You play Astro Chicken. Your chicken crashes after three seconds. GAME OVER.')
s.say('pilot', 'The high score still belongs to Stronkie: 999999. Nobody knows how he did it on a C64.')
s.say('pilot', 'The old machine rattles. It looks as if it could do with a good kick.')
on('arcade', 'use pull', s)
s = G.script()
L = s.label()
s.iff('kicked_chicken', L)
s.say('pilot', 'I give Astro Chicken a good kick!')
s.sound('zap').setf('kicked_chicken')
s.say('narrator', 'The screen flickers, the counter spins... NEW HIGH SCORE: 1000000! Stronkie will be furious.')
s.end()
s.here(L).say('narrator', 'The machine beeps. You already beat Stronkie. Once is enough.')
G.on('arcade', 'push', s)
hot('jukebox', 'bar', (238, 38, 268, 104), (252, 142), BACK, 'use', label='jukebox')
search('jukebox', 6, 'An old jukebox. Every button plays the same song. Behind the jukebox...',
       'An old jukebox. Every button plays the same song.', verbs='look')
line('jukebox', 'use push', 'I press a button. The Two Guys from Andromeda stop playing and glare at me.')
hot('band', 'bar', (128, 58, 200, 94), (164, 142), BACK, 'talk', label='The Two Guys from Andromeda',
    look='Two guys in Hawaiian shirts. A banner says: THE TWO GUYS FROM ANDROMEDA - TONIGHT ONLY. AND EVERY OTHER NIGHT.')
s = G.script()
s.say('band', 'We\'re the Two Guys from Andromeda! We also do weddings, funerals and space quests.')
G.on('band', 'talk', s)
hot('photo', 'bar', (108, 24, 132, 48), (120, 142), BACK, label='framed photo',
    look=['A signed photo: "TO THE SCUMM BAR - THANKS FOR ALL THE GROG! MARK STRONKS AKA STRONKIE."',
          'Under it a note: STRONKIE STILL OWES US 3 BUCKAZOIDS.'])
s = G.script()
s.say('barman', 'Hands off! Stronkie stays on the wall until he pays.')
on('photo', 'pickup pull', s)
hot('pirates', 'bar', (0, 60, 50, 132), (40, 142), LEFT, 'talk', label='pirates',
    look='Three important-looking pirates in the dark corner. They are too busy with their grog to pillage anything.')
s = G.script()
s.say('pirates', 'Going out into space? Watch out for Captain LeChuckle and his crew. They don\'t fight with swords, '
      'they fight with insults.')
s.say('pirates', 'If one says you fight like a dairy farmer, you say: how appropriate, you fight like a cow!')
s.setf('cow_tip')
G.on('pirates', 'talk', s)
hot('grog', 'bar', (150, 120, 192, 134), (172, 142), BACK, label='mugs of grog',
    look='Grog: kerosene, rum, battery acid and a dash of pepperoni. It is slowly eating through the mugs.')
careful('grog', 'use', 'One gulp of that and it melts through the mug, through my teeth, and then through the rest of me.')
line('grog', 'pickup', 'The mug is melting in my hand. I put it back, quickly.')
hot('napkin_o', 'bar', (194, 120, 216, 132), (206, 142), BACK, 'pickup', label='greasy napkin', image='napkin', state=3,
    look='A greasy napkin. Somebody scribbled on it.')
s = G.script()
s.hide('napkin_o').imgoff('napkin_o').pickup('napkin')
G.on('napkin_o', 'pickup', s)
door('br_out', 'bar', (300, 40, 319, 160), (300, 150), RIGHT, 'door to the plaza', ('plaza', 46, 124, FRONT))
first_visit('bar', 'You are in the SCUMM BAR. Pirates swap stories over mugs of bubbling grog. On stage the Two Guys '
            'from Andromeda play for nobody. There is a jukebox, an Astro Chicken arcade game and a framed photo.')

# ---- Stan's Pre-Owned Starships
hot('stanman', 'stan', (172, 40, 228, 146), (160, 150), RIGHT, 'talk', label='Stan',
    look='Stan never stops waving his arms. His jacket could blind a Sarien at fifty paces.')
hot('shelf', 'stan', (72, 30, 150, 56), (110, 150), BACK, 'pickup', label='fuel cells',
    look='Six glowing fuel cells. A price tag says: 50 BUCKAZOIDS EACH.')
s = G.script()
s.say('stan', 'WHOA THERE! That\'s 50 buckazoids. No money, no fuel. No exceptions!')
G.on('shelf', 'pickup', s)
hot('bin', 'stan', (58, 92, 120, 144), (130, 150), LEFT, label='bargain bin',
    look='A bin full of junk: broken droids, one left space boot and a rubber chicken with a pulley in the middle.')
hot('chicken_o', 'stan', (74, 80, 104, 94), (130, 150), LEFT, 'pickup', label='rubber chicken', image='chickenbin',
    state=3, look='A rubber chicken with a pulley in the middle. What could it possibly be for?')
s = G.script()
s.say('stan', 'That\'s not for sale! It\'s a free gift... with every purchase!')
G.on('chicken_o', 'pickup', s)
door('st_out', 'stan', (0, 30, 22, 160), (24, 150), LEFT, 'door to the plaza', ('plaza', 264, 124, FRONT))
s = G.script()
s.say('stan', 'Welcome to Stan\'s Pre-Owned Starships! Everything here was pre-owned by at least six pirates!')
s.say('stan', 'Fuel cells: 50 buckazoids. And every purchase comes with a FREE GIFT!')
G.on('stanman', 'talk', s)
s = G.script()
s.say('stan', 'One buckazoid? That buys you... a handshake.')
s.say('narrator', 'Stan shakes your hand and gives the coin back.')
G.on('coin', 'give', s, other='stanman')
G.on('coin', 'use', s, other='stanman')
s = G.script()
s.cuton()
s.drop('cash')
s.say('narrator', 'Stan counts the buckazoids twice.')
s.say('stan', 'A pleasure doing business! One fuel cell... and because I like your face, a FREE rubber chicken with a '
      'pulley in the middle! Who knows when you\'ll need one?')
s.pickup('fuelcell').hide('chicken_o').imgoff('chicken_o').pickup('chicken').setf('bought')
s.cutoff()
G.on('cash', 'give', s, other='stanman')
G.on('cash', 'use', s, other='stanman')
G.on('cash', 'give', s, other='shelf')
first_visit('stan', 'You are in Stan\'s Pre-Owned Starships. Stan, in a very loud jacket, waves his arms at you. '
            'Fuel cells glow on a shelf. A bargain bin says: SALE.')

# ---- the alley
hot('larry', 'alley', (178, 84, 208, 152), (164, 152), RIGHT, 'talk', label='man in a leisure suit',
    look='White polyester leisure suit, gold chain, hopeful smile. He smells of cheap aftershave.')
hot('trash', 'alley', (28, 116, 66, 152), None, label='trash can', look='Trash. Even the trash looks tired here.')
door('al_lefty', 'alley', (208, 30, 252, 132), (226, 142), BACK, 'door marked LEFTY\'S', ('backroom', 160, 160, BACK),
     locked=('larry_ok', lambda s: s.say('larry', 'Not so fast. What\'s the password?')))
door('al_out', 'alley', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the plaza', ('plaza', 156, 116, FRONT))
s = G.script()
A, B, OK, NO, X, DONE = (s.label() for _ in range(6))
s.iff('larry_ok', DONE)
s.say('larry', 'Name\'s Larry. Larry Laffer. I\'m not a bouncer, I\'m just... waiting for someone. '
      'Anyway. What\'s the password?')
s.here(A)
s.dialog([('Ken sent me.', OK, 'napkin_read'),
          ('Open sesame.', NO, None),
          ('Swordfish.', NO, None),
          ('Leisure suit.', NO, None),
          ('Never mind.', X, None)])
s.here(NO)
s.sound('error')
s.say('larry', 'Wrong password, pal. Nobody gets into Lefty\'s without the password.')
s.jmp(A)
s.here(OK)
s.say('larry', 'Ken sent you, eh? Any friend of Ken\'s is a friend of Larry\'s.')
s.say('narrator', 'He straightens his gold chain and opens the door.')
s.setf('larry_ok').sound('door')
s.end()
s.here(DONE)
s.say('larry', 'Good luck in there. That machine has eaten my last twelve buckazoids.')
s.here(X).end()
G.on('larry', 'talk', s)
s = G.script()
s.say('larry', 'No thanks, I\'m watching my figure.')
for it in ('burger', 'coin', 'napkin', 'chicken', 'ration', 'paper'):
    G.on(it, 'give', s, other='larry')
first_visit('alley', 'You are in a dark back alley. A man in a white polyester leisure suit leans against a door '
            'marked LEFTY\'S. He smells of cheap aftershave.')

# ---- Lefty's back room
hot('slots', 'backroom', (128, 12, 184, 136), (156, 146), BACK, 'use', label='SLOTS-O-DEATH',
    look='SLOTS-O-DEATH. Three reels full of skulls and one coin slot. A sticker says: KICKING THIS MACHINE IS '
         'STRICTLY FORBIDDEN.')
hot('sign_b', 'backroom', (212, 30, 250, 54), None, label='sign', look='It says: NO REFUNDS. NO SURVIVORS.')
s = G.script()
s.cuton()
s.say('pilot', 'I drop the buckazoid into SLOTS-O-DEATH and pull the arm.')
s.drop('coin').setf('coin_in').sound('click')
s.say('narrator', 'The reels spin... SKULL. SKULL. CHERRY. The machine burps and keeps your coin.')
s.say('narrator', 'From the alley you hear Larry snigger.')
s.cutoff()
G.on('coin', 'use', s, other='slots')
G.on('coin', 'give', s, other='slots')
s = G.script()
A, B = s.label(), s.label()
s.iff('jackpot', B)
s.iff('coin_in', A)
s.say('narrator', 'The machine growls at you. It only respects paying customers.')
s.end()
s.here(A)
s.cuton()
s.say('pilot', 'I give SLOTS-O-DEATH a good kick. CLANG!')
s.sound('zap')
s.say('narrator', 'The reels spin: STAR, STAR, STAR. JACKPOT! Fifty buckazoids rain into the tray.')
s.setf('jackpot').pickup('cash')
s.cutoff()
s.end()
s.here(B)
s.say('pilot', 'Kick it again? SLOTS-O-DEATH would kick back. Hard. I think twice and leave it.')
G.on('slots', 'push', s)
s = G.script()
L = s.label()
s.iff('jackpot', L)
s.say('pilot', 'I need a coin to play.')
s.end()
s.here(L).say('pilot', 'I\'ve pushed my luck enough. The skulls on the reels are watching me.')
on('slots', 'use pull', s)
door('bk_out', 'backroom', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the alley', ('alley', 226, 146, FRONT))
first_visit('backroom', 'You are in Lefty\'s back room. One bare bulb lights an old slot machine: SLOTS-O-DEATH.')

# =================================================================== CHAPTER 4: SPACE PIRATES
# ---- the cockpit, held by the tractor beam
hot('galleon', 'pcockpit', (40, 0, 280, 96), None, label='SPACE MONKEY',
    look='The SPACE MONKEY: a wooden sailing ship in space. Nobody knows how it works. Its green tractor beam holds us fast.')
hot('pthrottle', 'pcockpit', (120, 104, 200, 150), (160, 160), BACK, 'push', label='throttle')
s = G.script()
L = s.label()
s.iff('beam_off', L)
s.say('pilot', 'The throttle is at full power. The beam doesn\'t care.')
s.end()
s.here(L).say('pilot', 'The throttle. The beam is gone: time to fly!')
G.on('pthrottle', 'look', s)
hot('alarms', 'pcockpit', (20, 100, 60, 140), None, label='alarm light', look='ALARM! ALARM! As if I didn\'t know.')
hot('pnova', 'pcockpit', (266, 100, 306, 140), None, 'talk', label='NOVA', look='NOVA\'s alarm light. Even she is worried.')
s = G.script()
L = s.label()
s.iff('beam_off', L)
nova(s, 'The beam comes from their ship, pilot. Somebody has to switch it off from the inside. I wonder who.', 'p07_m14')
s.end()
s.here(L)
nova(s, 'The beam is gone! Fly, pilot, fly!', 'p07_m15')
G.on('pnova', 'talk', s)
G.on('galleon', 'talk', s)
door('pc_down', 'pcockpit', (0, 100, 28, 167), (34, 162), LEFT, 'ladder down to the airlock', ('pairlock', 50, 150, RIGHT))
s = G.script('flee')
L = s.label()
s.iff('beam_off', L)
s.say('narrator', 'The engines roar, but the tractor beam holds the STARRAVEN like a fly in syrup.')
s.end()
s.here(L)
s.cuton()
s.say('pilot', 'I slam the throttle!')
s.sound('hyper')
s.say('narrator', 'The STARRAVEN breaks free and shoots away! Behind you LeChuckle shakes his fist... and fires one '
      'parting shot.')
s.sound('thunder')
s.say('narrator', 'BOOM! Smoke fills the cockpit.')
nova(s, 'Main power crystal hit! We\'re going down, pilot. Straight onto the World of Stronkie!', 'p07_m12')
chapter_end(s, ['The STARRAVEN tumbles through the clouds of a strange and beautiful world...'],
            ('Chapter 5: Landfall', 'p07_card'))
on('pthrottle', 'push pull use', s)
first_visit('pcockpit', 'You are in the cockpit of the STARRAVEN. The pirate ship fills the window, and its green '
            'tractor beam holds you tight. Alarms blare. A ladder leads down to the airlock.')

# ---- the airlock
hot('pdoor', 'pairlock', (116, 12, 202, 108), (160, 126), BACK, 'open', label='outer door')
s = G.script()
L = s.label()
s.iff('pdoor_open', L)
s.say('pilot', 'The outer door of the airlock. My spacesuit helmet is on, so it\'s safe to open it here.')
s.say('pilot', 'Through its window I see a thick mooring cable: the pirates have tied their ship to ours!')
s.end()
s.here(L).say('pilot', 'The mooring cable stretches across the void to the pirate ship.')
G.on('pdoor', 'look', s)
s = G.script()
L = s.label()
s.iff('pdoor_open', L)
s.say('pilot', 'I check my helmet and open the outer door.')
s.sound('door').setf('pdoor_open')
s.say('narrator', 'Air hisses out. The mooring cable stretches across the void to the pirate ship.')
s.end()
s.here(L).say('pilot', 'It is open. Don\'t jump. Guybrush could hold his breath for ten minutes. I can not.')
G.on('pdoor', 'open', s)
s = G.script('zip_out')
A, B = s.label(), s.label()
s.iff('pdoor_open', A)
s.say('pilot', 'The outer door is closed.')
s.end()
s.here(A)
s.has('chicken', B)
s.say('pilot', 'The cable is too thick and slippery to hold on to. I\'d need something to slide along it with.')
s.end()
s.here(B)
s.cuton()
L = s.label()
s.iff('zipped', L)
s.say('narrator', 'You hook the pulley of the rubber chicken over the cable, hold on tight and... WHEEEE!')
s.say('narrator', 'You zip across the void to the pirate ship. Stan was right: everybody needs a rubber chicken with a '
      'pulley in the middle.')
s.setf('zipped')
s.here(L)
s.sound('hyper')
s.room('deck', 40, 150, RIGHT)
s.cutoff()
G.on('chicken', 'use', s, other='pdoor')
G.on('pdoor', 'walk', s)
hot('prack', 'pairlock', (250, 58, 292, 116), None, label='rack', look='An empty boot rack. My boots are on my feet.')
door('pa_up', 'pairlock', (0, 30, 24, 160), (30, 150), LEFT, 'ladder up to the cockpit', ('pcockpit', 60, 162, RIGHT))
first_visit('pairlock', 'You are in the airlock. Through the window of the outer door you see a thick mooring cable: '
            'the pirates have tied their ship to yours!')

# ---- the deck of the SPACE MONKEY
hot('cable_d', 'deck', (0, 84, 130, 108), (30, 150), LEFT, 'use', label='cable',
    look='The cable runs back to the STARRAVEN.')
s = G.script()
s.say('narrator', 'You hook the chicken over the cable and zip back to the STARRAVEN.')
s.sound('hyper')
s.room('pairlock', 200, 140, LEFT)
on('cable_d', 'use walk', s)
G.on('chicken', 'use', s, other='cable_d')
hot('parrot', 'deck', (48, 76, 66, 104), (70, 150), LEFT, 'talk', label='parrot',
    look='A green space parrot. It keeps muttering to itself.')
s = G.script()
s.say('parrot', 'SQUAWK! Family reunion! SQUAWK! Glad you attended your family reunion! SQUAWK! Polly wants a buckazoid!')
s.setf('parrot_heard')
G.on('parrot', 'talk', s)
line('parrot', 'pickup', 'It bites my glove. SQUAWK!')
hot('poster', 'deck', (208, 78, 242, 116), (224, 140), BACK, label='wanted poster',
    look=['WANTED: MARK STRONKS AKA STRONKIE. CRIME: WRITING ADVENTURE GAMES ON A COMMODORE 64 AND MAKING PIRATES '
          'READ ALL THIS TEXT.', 'REWARD: 3 BUCKAZOIDS.'])
hot('sails', 'deck', (40, 0, 280, 70), None, label='solar sails', look='Solar sails creak in the starlight.')
G.thing('pguard_t', 'deck', (164, 92, 196, 150), (140, 150), RIGHT, 'talk', label='pirate guard', actor='pguard')
simple('pguard_t', 'look', 'pilot', 'A space pirate with an eye patch and a laser cutlass. He looks very proud of his insults.')
line('pguard_t', 'push pull', 'I have no sword. And anyway, space pirates only fight with insults. Say something!')
door('dk_cabin', 'deck', (290, 30, 319, 140), (290, 150), RIGHT, 'door to the captain\'s cabin', ('cabin', 30, 160, RIGHT),
     locked=('guard_gone', lambda s: s.say('pguard', 'En garde, landlubber!')))
door('dk_hatch', 'deck', (244, 128, 288, 150), (240, 154), RIGHT, 'hatch to the engine room', ('pengine', 30, 150, RIGHT),
     locked=('guard_gone', lambda s: s.say('pguard', 'En garde, landlubber!')))
s = G.script('duel')
A, B, C, X, W1, W2 = (s.label() for _ in range(6))
s.iff('insult1', B)
s.say('pguard', 'You fight like a dairy farmer!')
s.here(A)
s.dialog([('How appropriate. You fight like a cow!', C, 'cow_tip'),
          ('Oh yeah?', W1, None),
          ('I am rubber, you are glue.', W1, None),
          ('Er... bye.', X, None)])
s.here(W1)
s.sound('error')
s.say('pguard', 'Ha! Is that all you\'ve got? I said: you fight like a dairy farmer!')
s.jmp(A)
s.here(C)
s.say('pguard', 'Arrr! Then try this one:')
s.setf('insult1').sound('zap')
s.here(B)
D = s.label()
s.say('pguard', 'I\'ve spoken with apes more polite than you!')
s.here(D)
C2 = s.label()
s.dialog([('I\'m glad to hear you attended your family reunion.', C2, 'parrot_heard'),
          ('So have I.', W2, None),
          ('Your mother was a hamster.', W2, None),
          ('Er... bye.', X, None)])
s.here(W2)
s.sound('error')
s.say('pguard', 'Pathetic! I\'ve spoken with apes more polite than you!')
s.jmp(D)
s.here(C2)
s.cuton()
s.say('narrator', 'The guard bursts into tears, drops his laser cutlass and runs below deck to tell his mother.')
s.walk('pguard', 312, 150)
s.put('pguard', None, 0, 0)
s.hide('pguard_t').setf('guard_gone')
s.cutoff()
s.here(X).end()
G.on('pguard_t', 'talk', s)
s = G.script('deck_in')
L = s.label()
s.iff('guard_met', L)
s.setf('guard_met')
s.say('narrator', 'You are on the deck of the SPACE MONKEY. Solar sails creak in the starlight and a wanted poster is '
      'nailed to the mast.')
s.say('pguard', 'En garde! You fight like a dairy farmer!')
s.here(L)
G.rooms['deck']['enter'] = s

# ---- the captain's cabin
hot('lechuckle', 'cabin', (138, 30, 182, 104), (64, 160), RIGHT, 'talk', label='Captain LeChuckle',
    look='A ghost pirate, green and see-through, except for his belt. On the belt hangs a big key.')
hot('buckazoids', 'cabin', (88, 92, 116, 106), (64, 160), RIGHT, label='buckazoids',
    look='Piles of stolen buckazoids. LeChuckle counts them again and again.')
s = G.script()
s.say('lechuckle', 'Touch my buckazoids and ye\'ll walk the plank!')
G.on('buckazoids', 'pickup', s)
hot('cake', 'cabin', (200, 78, 232, 100), (262, 160), LEFT, label='cake',
    look=['A birthday cake with a note: THE CAKE IS A LIE.', 'Under it, in smaller letters: ALSO, IT IS 300 YEARS OLD.'])
line('cake', 'pickup use', 'It\'s a lie. And rather stale.')
hot('desk_c', 'cabin', (62, 104, 254, 150), None, label='desk', look='A big desk. Mostly buckazoids.')
hot('porthole_c', 'cabin', (136, 8, 184, 30), None, label='porthole', look='Stars. And my poor STARRAVEN, on a leash.')
careful('lechuckle', 'push pull', 'My fist would go right through him: he\'s a ghost pirate. His fist, sadly, would not go '
        'right through me.')
door('cb_out', 'cabin', (0, 40, 20, 150), (20, 160), LEFT, 'door to the deck', ('deck', 280, 150, LEFT))
s = G.script()
s.say('lechuckle', 'Hands off, landlubber!')
s.say('narrator', 'LeChuckle slaps your hand away without looking up.')
G.on('lechuckle', 'pickup', s)
s = G.script('lechuckle_talk')
A, B, C, D, X, M, G1, G2, W = (s.label() for _ in range(9))
s.iff('beam_off', C)
s.iff('key_got', B)
s.say('lechuckle', 'Arrr! Ye got past my guard? No matter. Nothing in the galaxy can make Captain LeChuckle turn away '
      'from his buckazoids.')
s.say('lechuckle', 'Well... except maybe a three-headed monkey. I\'ve always wanted to see one.')
s.here(A)
s.dialog([('Look behind you, a three-headed monkey!', M, None),
          ('Nice beard.', W, None),
          ('Bye.', X, None)])
s.here(W)
s.say('lechuckle', 'Arrr. Boring.')
s.say('narrator', 'LeChuckle doesn\'t even look up from his buckazoids.')
s.jmp(A)
s.here(M)
s.cuton()
s.say('lechuckle', 'WHERE?!')
s.say('narrator', 'LeChuckle spins around. Quick as a flash you grab the big key from his belt.')
s.pickup('bigkey').setf('key_got')
s.cutoff()
s.end()
s.here(B)
s.say('lechuckle', 'Hey! Where\'s my key?')
s.say('narrator', 'LeChuckle starts counting his pockets.')
s.end()
s.here(C)
s.iff('said_grandmother', D)
s.say('lechuckle', 'Ye switched off my beam! En garde, landlubber: my grandmother flies better than you!')
s.here(G1)
W2 = s.label()
s.dialog([('Then she should be captain instead of you!', G2, 'ricky_tip'),
          ('So does mine.', W2, None),
          ('I\'m rubber, you\'re glue.', W2, None),
          ('I\'m leaving.', X, None)])
s.here(W2)
s.sound('error')
s.say('lechuckle', 'Ha! Call that an insult? My grandmother flies better than you!')
s.jmp(G1)
s.here(G2)
s.cuton()
s.say('narrator', 'LeChuckle\'s ghostly jaw drops.')
s.say('lechuckle', 'Arrr... nobody has ever out-insulted me. Ye have my respect, landlubber. My crew won\'t lift a '
      'finger for Vex ever again!')
s.setf('said_grandmother').sound('score')
s.cutoff()
s.end()
s.here(D)
s.say('lechuckle', 'Arrr. Respect, landlubber. Now get off my ship.')
s.here(X).end()
G.on('lechuckle', 'talk', s)
s = G.script('cabin_in')
L = s.label()
s.iff('seen_cabin', L)
s.setf('seen_cabin')
s.say('narrator', 'You are in the captain\'s cabin. Captain LeChuckle, a ghostly green space pirate with a beard full '
      'of space bugs, counts his buckazoids at a big desk. A big key hangs from his belt.')
s.here(L)
K = s.label()
s.iff('beam_off', K)
s.end()
s.here(K)
s.iff('rematch', L2 := s.label())
s.setf('rematch')
s.say('lechuckle', 'Ye switched off my beam! En garde, landlubber: my grandmother flies better than you!')
s.here(L2)
G.rooms['cabin']['enter'] = s

# ---- the engine room of the SPACE MONKEY
hot('beamgen', 'pengine', (120, 0, 200, 100), (160, 120), BACK, 'use', label='tractor beam generator')
s = G.script()
L = s.label()
s.iff('beam_off', L)
s.say('pilot', 'The tractor beam generator. It glows green and has a big keyhole.')
s.end()
s.here(L).say('pilot', 'The generator is dead. Good.')
G.on('beamgen', 'look', s)
s = G.script()
L, K = s.label(), s.label()
s.iff('beam_off', L)
s.has('bigkey', K)
s.say('pilot', 'The generator has a big keyhole. I\'ll need the key.')
s.end()
s.here(K)
s.cuton()
s.say('pilot', 'I turn the key.')
s.sound('zap').setf('beam_off')
s.say('narrator', 'The generator whines, splutters and dies. Outside, the green tractor beam flickers out!')
s.cutoff()
s.end()
s.here(L).say('pilot', 'It\'s off. Time to get back to the STARRAVEN.')
on('beamgen', 'use push pull', s)
G.on('bigkey', 'use', s, other='beamgen')
hot('pcrates', 'pengine', (44, 84, 108, 146), (120, 140), LEFT, label='crates of grog')
search('pcrates', 7, 'Crates of grog. Some of them are smoking. Between two crates...',
       'Crates of grog. Some of them are smoking.', verbs='look')
careful('pcrates', 'use open', 'Pirate grog. My insides would dissolve in a colourful way.')
hot('pcrates2', 'pengine', (210, 84, 258, 146), (200, 140), RIGHT, label='crates of grog',
    look='More crates of grog. They are smoking too.')
hot('ricky', 'pengine', (262, 100, 296, 166), (250, 156), RIGHT, 'talk', label='crewman in a red shirt',
    look='A young crewman in a red shirt, tied up. He looks nervous. He has every reason to be.')
G.objects['ricky']['image'] = 'rickygone'
s = G.script()
A, B, U, X = (s.label() for _ in range(4))
s.say('ricky', 'I\'m Ensign Ricky. They captured me on an away mission. I\'m wearing a red shirt, so... this '
      'probably won\'t end well. Could you untie me?')
s.say('ricky', 'Oh, and a tip: the captain always brags that his grandmother flies better than anyone. The perfect '
      'answer is: then she should be captain!')
s.setf('ricky_tip')
s.dialog([('I\'ll untie you.', U, None), ('Sorry, I\'m in a hurry.', X, None)])
s.here(U)
s.cuton()
s.say('narrator', 'You untie Ricky.')
s.say('ricky', 'Thank you! For once, a red shirt survives! I\'ll hide in an escape pod. If you ever need me, I\'ll be there!')
s.say('narrator', 'He sneaks off.')
s.imgon('ricky').hide('ricky').setf('untied_crewman').sound('score')
s.cutoff()
s.end()
s.here(X)
s.say('ricky', 'I\'ll... I\'ll just stay here. Red shirts never make it to the next chapter anyway.')
G.on('ricky', 'talk', s)
G.on('ricky', 'pull', s)
G.on('ricky', 'use', s)
door('pe_out', 'pengine', (0, 30, 18, 160), (20, 150), LEFT, 'ladder up to the deck', ('deck', 250, 156, LEFT))
first_visit('pengine', 'You are in the engine room of the SPACE MONKEY. The tractor beam generator hums and glows green. '
            'Crates of grog are stacked everywhere, and a crewman in a red shirt sits in the corner.')

# =================================================================== the start
chapter_start(['The STARRAVEN races away from KX-9... and then the engines cough.'],
              ('Chapter 3: Asteroid 42', 'p05_card'), 'pad', 60, 156, RIGHT, music='p06')
fv = G.rooms['pad']['enter']
once(fv, 'intro_said', lambda s: nova(s, 'That hyperjump drained our fuel cells, pilot. The nearest fuel is on Asteroid 42, the most wretched hive '
     'of scum and villainy this side of Andromeda. Don\'t panic. And hold on to your towel.'))
default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {'pguard': ('deck', 180, 150, LEFT)}
VARIANTS = {
    'napkin': ('bar', {}, {'napkin': True}),
    'chickenbin': ('stan', {}, {'chicken': True}),
    'rickygone': ('pengine', {}, {'ricky_gone': True}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('pad', 'Pad 42', 60, 156), ('plaza', 'Plaza', 160, 150), ('bar', 'Bar', 250, 150),
             ('stan', 'Stan', 50, 150), ('alley', 'Alley', 160, 150), ('backroom', 'Lefty', 160, 150),
             ('pcockpit', 'Cockpit', 160, 162), ('deck', 'Deck', 60, 150), ('cabin', 'Cabin', 30, 160),
             ('pengine', 'Pirate engine', 40, 150)]
DEV_ITEMS = ['burger', 'coin', 'cash', 'napkin', 'fuelcell', 'chicken', 'bigkey', 'ration', 'paper']
