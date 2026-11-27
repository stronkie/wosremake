"""World of Stronkie remake - Chapter Four: Landfall (disk 4).

The original game's Chapter 5 (Landfall: the crash, the jungle, the crystal
cave) and Chapter 6 (The Village of the Stronkies). Keepsake of this disk: the
singing shell. Choices that matter later: the wooden monkey and the glasses."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p08', 'p09']
for n, c in (('gateguard', 23), ('trader', 22), ('zooma', 17), ('bix', 19), ('stronkies', 24)):
    add_actor(n, c)

# =================================================================== rooms
G.room('wreck', 'wreck', music='p08', walk=[[(60, 156), (240, 156), (240, 167), (60, 167)]])
G.room('crash', 'crash', music='p08', walk=[FLOOR(142)])
G.room('jungle', 'jungle', music='p08', walk=[FLOOR(148)])
G.room('river', 'river', music='p08', walk=[FLOOR(148)])
G.room('ccave', 'ccave', music='p08', walk=[[(20, 144), (300, 144), (319, 167), (0, 167)]])
G.room('vgate', 'vgate', music='p08', walk=[FLOOR(142)])
G.room('vsquare', 'vsquare', music='p09', walk=[FLOOR(104)])
G.room('market', 'market', music='p09', walk=[FLOOR(140)])
G.room('elder', 'elder', music='p09', walk=[[(20, 146), (300, 146), (319, 167), (0, 167)]])
G.room('workshop', 'workshop', music='p09', walk=[[(0, 140), (222, 140), (222, 167), (0, 167)]])
G.room('tower', 'tower', music='p09', walk=[FLOOR(132)])
BLOCK = {'vsquare': [[(114, 104), (206, 104), (206, 134), (114, 134)]],
         'market': [[(138, 140), (182, 140), (182, 167), (138, 167)]]}

# =================================================================== things you carry
for nm, lab, ic, txt in (
        ('extinguisher', 'fire extinguisher', 'extinguisher', 'A heavy red fire extinguisher.'),
        ('fruit', 'blue fruit', 'fruit', 'A heavy blue fruit. It smells sweet.'),
        ('pcrystal', 'power crystal', 'powercrystal', 'It hums and glows. Just what the ship needs.'),
        ('monkey', 'wooden monkey', 'monkey', 'A small, hand-carved wooden monkey with a big grin. Carved under its '
                                             'feet: "MADE BY MARK STRONKS AKA STRONKIE. THIS IS NOT THE SECRET OF '
                                             'MONKEY ISLAND."'),
        ('starcoin', 'shiny coin', 'coin', 'A heavy coin with a star on it.'),
        ('vmap', 'map of the mountains', 'map', 'It shows the way to the Sky Temple. The bridge on the road is broken.'),
        ('banner', 'big banner', 'banner', 'A huge banner of strong cloth.'),
        ('glider', 'glider', 'glider', 'Light wooden wings with my banner as a sail.'),
        ('glasses', 'nose glasses', 'glasses', 'Plastic glasses with a big nose and a moustache. A label says: AS WORN '
                                               'BY ZAK MCKRACKEN.')):
    G.thing(nm, None, label=lab, icon=ic)
    simple(nm, 'look', 'pilot', txt)
line('fruit', 'use', 'I am not hungry. Maybe someone else would like it.')
line('monkey', 'talk', 'The wooden monkey just grins. For a moment I think it winked.')
s = G.script()
L = s.label()
s.iff('glasses', L)
s.say('pilot', 'I put on the nose glasses.')
s.setf('glasses').sound('score')
s.say('narrator', 'The Stronkies point at you and fall over laughing. Zak McKracken would be proud.')
s.say('pilot', 'I\'ll keep them in my pocket. You never know...')
s.end()
s.here(L).say('pilot', 'I put on the nose glasses again. Somewhere, Zak McKracken smiles.')
G.on('glasses', 'use', s)
s = G.script('listen')
L = s.label()
s.iff('understand', L)
s.cuton()
s.say('pilot', 'I hold the shell to my ear...')
s.setf('understand').sound('score')
s.say('narrator', 'The chirping all around you slowly turns into words! It works a bit like a Babel fish, but less slimy.')
s.cutoff()
s.end()
s.here(L).say('pilot', 'The shell hums softly. Thanks to it I understand the Stronkies.')
G.on('shell', 'use', s)
G.on('shell', 'talk', s)


def chirp(s, who, text, after=None):
    """a Stronkie talks: chirping, until the singing shell translates"""
    L = s.label()
    s.iff('understand', L)
    s.say(who, 'Chirp! Chirrup, chirp?')
    s.say('pilot', text)
    s.end()
    s.here(L)
    return s


# =================================================================== CHAPTER 5: LANDFALL
# ---- the wrecked cockpit
hot('wsky', 'wreck', (40, 0, 280, 86), None, label='window', look='Purple clouds. Two suns. We are not in Ravenmoor any more.')
hot('wlever', 'wreck', (226, 122, 244, 148), (220, 160), RIGHT, 'pull', label='red lever',
    look='EMERGENCY HATCH RELEASE. PULL IN CASE OF CRASH.')
hot('whatch', 'wreck', (248, 104, 296, 166), (232, 160), RIGHT, 'open', label='hatch')
hot('wslot', 'wreck', (186, 92, 226, 122), (200, 160), BACK, 'look', label='power crystal slot')
hot('wsparks', 'wreck', (66, 92, 112, 122), (88, 160), BACK, 'talk', label='console')
hot('ext_o', 'wreck', (22, 110, 46, 156), (66, 160), LEFT, 'pickup', label='fire extinguisher', image='extinguisher',
    state=3, look='A heavy red fire extinguisher.')
s = G.script()
s.hide('ext_o').imgoff('ext_o').pickup('extinguisher')
G.on('ext_o', 'pickup', s)
s = G.script()
L = s.label()
s.iff('ship_ok', L)
s.say('pilot', 'The empty power crystal slot is black and burnt.')
s.end()
s.here(L).say('pilot', 'The new power crystal hums in its slot.')
G.on('wslot', 'look', s)
line('wsparks', 'look', 'Sparks fly from the console.')
s = G.script()
L = s.label()
s.iff('ship_ok', L)
nova(s, 'I need a new power crystal, pilot. This planet seems to be full of them.', 'p08_m12')
s.end()
s.here(L)
nova(s, 'Repairs are under way. Go and make friends, pilot.', 'p08_m13')
G.on('wsparks', 'talk', s)
G.on('wslot', 'talk', s)
s = G.script()
L = s.label()
s.iff('hatch_open', L)
s.cuton()
s.say('pilot', 'I heave on the lever...')
s.sound('thunder').setf('hatch_open')
s.say('narrator', 'BANG! Explosive bolts blow the hatch open.')
s.cutoff()
s.end()
s.here(L).say('pilot', 'The hatch is already open.')
G.on('wlever', 'pull', s)
G.on('wlever', 'push', s)
G.on('wlever', 'use', s)
door('wreck_out', 'wreck', (248, 104, 296, 166), (232, 160), RIGHT, 'hatch', ('crash', 70, 150, RIGHT),
     locked=('hatch_open', 'It is jammed shut. Maybe the emergency lever will help.'))
G.objects['whatch']['state'] = 0           # (the exit is the hatch)
s = G.script()
s.cuton()
s.say('pilot', 'I slot the power crystal into the console.')
s.drop('pcrystal').setf('ship_ok').sound('beep')
s.say('narrator', 'The ship hums back to life!')
nova(s, 'Thank you, pilot. The repairs will take a while. I detect life signs to the east.', 'p08_m26')
s.cutoff()
G.on('pcrystal', 'use', s, other='wslot')
G.on('pcrystal', 'use', s, other='wsparks')
first_visit('wreck', 'You are in the wrecked cockpit of the STARRAVEN. Sparks fly from the console. The hatch is jammed '
            'shut. A red emergency lever hangs beside it.')

# ---- the crash site
hot('suns', 'crash', (200, 0, 319, 40), None, label='two suns',
    look='One sun is orange, the other blue. I am a long way from home.')
hot('wreckship', 'crash', (40, 82, 210, 144), (120, 150), BACK, 'walk', label='STARRAVEN',
    look='The smoking wreck of the STARRAVEN. Poor NOVA.')
s = G.script()
s.room('wreck', 150, 162, BACK)
on('wreckship', 'walk open', s)
hot('fire', 'crash', (216, 78, 278, 144), (200, 150), RIGHT, 'look', label='flames', image='fireout', state=1,
    look='The broken engine is burning fiercely. The flames block the path north.')
line('fire', 'walk pickup push pull', 'The flames are much too hot. I cannot get past.')
hot('jpath', 'crash', (216, 78, 278, 144), (246, 146), BACK, 'walk', label='path north', state=0,
    look='The path north into the jungle is clear.')
s = G.script()
s.room('jungle', 160, 160, BACK)
on('jpath', 'walk', s)
s = G.script()
s.cuton()
s.say('pilot', 'WHOOSH!')
s.sound('zap').imgon('fire').hide('fire').show('jpath').setf('fire_out')
s.say('narrator', 'A cloud of white foam smothers the flames. The path north into the jungle is clear.')
s.cutoff()
G.on('extinguisher', 'use', s, other='fire')
door('cr_east', 'crash', (300, 80, 319, 160), (300, 152), RIGHT, 'path east', ('vgate', 30, 152, RIGHT))
first_visit('crash', 'You stand beside the smoking wreck of the STARRAVEN in a field of purple grass under two suns. '
            'Flames from the engine block the path north. A path leads east.')

# ---- the jungle
hot('trees_j', 'jungle', (20, 0, 80, 116), None, label='giant trees',
    look='The trees are as tall as churches. Their leaves are purple. Strange birds sing.')
hot('fruit_o', 'jungle', (156, 56, 194, 80), (176, 152), BACK, 'pickup', label='blue fruit', image='nofruit', state=1,
    look='Heavy blue fruit hangs from a low branch.')
s = G.script()
L = s.label()
s.iff('got_fruit', L)
s.say('pilot', 'I reach up and pick a blue fruit.')
s.imgon('fruit_o').hide('fruit_o').setf('got_fruit').pickup('fruit')
s.end()
s.here(L)
G.on('fruit_o', 'pickup', s)
hot('bushes', 'jungle', (0, 116, 319, 146), (100, 152), BACK, 'look', label='bushes')
hot('monkey_o', 'jungle', (88, 116, 106, 140), (100, 152), BACK, 'pickup', label='wooden monkey', image='monkey', state=0,
    look='A small wooden monkey with a big grin. What is that doing on this planet?')
s = G.script()
L = s.label()
s.iff('bush_searched', L)
s.say('pilot', 'Thick purple bushes. Something seems to be hiding in there. I push the bushes apart...')
s.sound('beep').setf('bush_searched').show('monkey_o').imgon('monkey_o')
s.say('narrator', 'Peeking out between the roots is... a small wooden monkey! What is that doing on this planet?')
s.end()
s.here(L).say('pilot', 'Just leaves and roots now.')
on('bushes', 'look pickup pull push open', s)
s = G.script()
s.cuton()
s.hide('monkey_o').imgoff('monkey_o').pickup('monkey').setf('monkey')
s.say('narrator', 'From out of nowhere a jaunty Caribbean tune starts to play...')
s.sound('score')
s.say('pilot', 'Carved under its feet: "MADE BY MARK STRONKS AKA STRONKIE. THIS IS NOT THE SECRET OF MONKEY ISLAND."')
s.cutoff()
G.on('monkey_o', 'pickup', s)
door('ju_south', 'jungle', (100, 158, 220, 167), (160, 160), FRONT, 'path south to the crash site', ('crash', 246, 152, FRONT))
door('ju_east', 'jungle', (300, 40, 319, 150), (300, 156), RIGHT, 'path east to the river', ('river', 30, 156, RIGHT))
first_visit('jungle', 'You are in a jungle of giant purple trees. Strange birds sing. Thick bushes grow between the roots. '
            'Heavy blue fruit hangs from a low branch. The path leads east to a river.')

# ---- the river
hot('riverw', 'river', (0, 80, 319, 140), None, label='river',
    look='The water glows and rushes past much too fast to swim.')
careful('riverw', 'walk use open', 'Into the glowing river? The current would sweep me away in seconds.')
hot('cave_far', 'river', (200, 52, 262, 82), None, label='cave', look='On the far bank is a cave.')
hot('vine', 'river', (28, 0, 84, 140), (70, 152), LEFT, 'use', label='tree with a vine',
    look='A long, strong vine hangs from the tree, out over the water.')
s = G.script()
L = s.label()
s.iff('swung', L)
s.cuton()
s.say('narrator', 'You grab the vine, take a run... and swing across the glowing river!')
s.say('narrator', 'You land right in front of the cave.')
s.setf('swung')
s.room('ccave', 40, 156, RIGHT)
s.cutoff()
s.end()
s.here(L)
s.say('pilot', 'WHEEE!')
s.room('ccave', 40, 156, RIGHT)
on('vine', 'use pull walk', s)
door('rv_west', 'river', (0, 140, 22, 167), (20, 156), LEFT, 'path back to the jungle', ('jungle', 290, 156, LEFT))
first_visit('river', 'You stand by a wide, fast river of glowing water. A tall tree leans over it with a long vine. '
            'On the far bank is a cave.')

# ---- the crystal cave
hot('bigcrystal', 'ccave', (108, 46, 192, 142), (150, 150), BACK, 'pickup', label='big power crystal')
s = G.script()
L = s.label()
s.iff('crystal_got', L)
s.say('pilot', 'A big power crystal, stuck fast in the rock.')
s.end()
s.here(L).say('pilot', 'The big crystal still pulses with light. My piece of it is enough.')
G.on('bigcrystal', 'look', s)
s = G.script()
L = s.label()
s.iff('crystal_got', L)
s.say('pilot', 'It is stuck fast in the rock. My bare hands are no match for it. I need something heavy.')
s.end()
s.here(L).say('pilot', 'I already have a piece of it.')
on('bigcrystal', 'pickup pull push', s)
s = G.script()
L = s.label()
s.iff('crystal_got', L)
s.cuton()
s.say('pilot', 'I slam the heavy extinguisher against the rock.')
s.sound('thunder').setf('crystal_got').pickup('pcrystal')
s.say('narrator', 'CRACK! A power crystal comes loose.')
s.cutoff()
s.end()
s.here(L).say('pilot', 'I already have a piece of it.')
G.on('extinguisher', 'use', s, other='bigcrystal')
hot('rock', 'ccave', (200, 66, 304, 140), (250, 152), BACK, label='rock')
search('rock', 8, 'Small crystals grow everywhere in the rock. Between them...',
       'Small crystals grow everywhere in the rock.', verbs='look')
hot('diamonds', 'ccave', (224, 148, 270, 166), (210, 158), RIGHT, label='pile of diamonds',
    look='A pile of diamonds under a wobbly boulder. Scratched into the rock: ROCKFORD WAS HERE.')
line('diamonds', 'pickup pull push', 'The boulder above them wobbles. I have played Boulder Dash before, so I leave the '
     'diamonds alone.')
hot('vine_back', 'ccave', (0, 28, 44, 112), (20, 156), LEFT, 'use', label='vine')
s = G.script()
s.say('pilot', 'WHEEE!')
s.room('river', 80, 156, RIGHT)
on('vine_back', 'use walk pull', s)
first_visit('ccave', 'You are in a cave full of glowing crystals. In the middle one big crystal pulses with light. A vine '
            'hangs back across the river. In a corner, a pile of diamonds lies under a big boulder.')

# ---- the gate of the village
hot('vgate_g', 'vgate', (118, 40, 200, 114), (160, 146), BACK, 'walk', label='gate',
    look='Woven from living branches.')
hot('gguard', 'vgate', (218, 86, 266, 146), (200, 150), RIGHT, 'talk', label='small blue creature',
    look='A small blue Stronkie with long ears. He keeps looking hungrily at the jungle.')
careful('gguard', 'push pull', 'He is small, but his spear is sharp. Better make friends.')
s = G.script()
L = s.label()
s.iff('gate_open', L)
s.say('gateguard', 'Chirp! Chirrup!')
s.say('narrator', 'The guard chirps something and rubs his tummy.')
s.end()
s.here(L)
s.say('gateguard', 'Chirp chirp!')
s.say('narrator', 'He grins from ear to ear and waves you in.')
G.on('gguard', 'talk', s)
s = G.script()
s.cuton()
s.drop('fruit').setf('gate_open')
s.say('narrator', 'The guard sniffs the blue fruit, takes a huge bite and grins from ear to ear.')
s.say('narrator', 'He opens the gate and waves you in.')
s.sound('door')
s.cutoff()
G.on('fruit', 'give', s, other='gguard')
G.on('fruit', 'use', s, other='gguard')
s = G.script('to_village')
A, B = s.label(), s.label()
s.iff('gate_open', A)
s.say('narrator', 'The guard points his spear at you and chirps angrily.')
s.end()
s.here(A)
s.iff('ship_ok', B)
s.say('narrator', 'NOVA on your radio:')
nova(s, 'Pilot, first find a power crystal for the ship, please!', 'p08_m29')
s.end()
s.here(B)
s.cuton()
s.say('narrator', 'You follow the little guard through the gate, into the village of the Stronkies...')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
spoken_card(s, 'Chapter 6: The Village', 'p08_card')
s.card('The Stronkies live in round huts among the giant trees. Everywhere small blue faces peek at you and chirp '
       'excitedly. You cannot understand a word they say.', wait=True)
s.music('p09')
s.room('vsquare', 160, 156, BACK)
s.cutoff()
on('vgate_g', 'walk open', s)
door('vg_west', 'vgate', (0, 60, 18, 160), (20, 152), LEFT, 'path west to the crash site', ('crash', 290, 152, LEFT))
first_visit('vgate', 'You stand before a gate in a wall of woven branches. A small blue creature with long ears guards '
            'it with a spear.')

# =================================================================== CHAPTER 6: THE VILLAGE
# ---- the village square
hot('fountain', 'vsquare', (116, 84, 204, 132), (160, 142), BACK, 'look', label='fountain')
s = G.script()
L = s.label()
s.iff('coin_fished', L)
s.say('pilot', 'Clear water splashes into a stone bowl. Something shines at the bottom.')
s.end()
s.here(L).say('pilot', 'Clear water splashes into a stone bowl.')
G.on('fountain', 'look', s)
s = G.script()
L = s.label()
s.iff('coin_fished', L)
s.say('pilot', 'I fish a coin out of the fountain!')
s.setf('coin_fished').pickup('starcoin')
s.end()
s.here(L).say('pilot', 'There is nothing else in the fountain.')
on('fountain', 'pickup use open', s)
for nm, box, wk in (('sq_str1', (76, 104, 104, 144), (110, 150)), ('sq_str2', (224, 114, 250, 148), (214, 152))):
    hot(nm, 'vsquare', box, wk, BACK, 'talk', label='Stronkie',
        look='Small, blue and furry, with long ears and big friendly eyes.')
    s = G.script()
    chirp(s, 'stronkies', 'Chirp, chirp. I do not understand them.')
    s.say('stronkies', 'Welcome, stranger! The Elder and Bix have more to say.')
    G.on(nm, 'talk', s)
door('sq_work', 'vsquare', (8, 40, 74, 98), (40, 112), BACK, 'workshop', ('workshop', 60, 156, RIGHT))
door('sq_elder', 'vsquare', (128, 38, 184, 84), (110, 108), BACK, 'Elder\'s hut', ('elder', 160, 160, BACK))
door('sq_market', 'vsquare', (248, 40, 304, 98), (276, 112), BACK, 'market', ('market', 40, 152, RIGHT))
door('sq_tower', 'vsquare', (290, 0, 312, 100), (300, 112), BACK, 'lookout tower', ('tower', 160, 156, BACK))
door('sq_gate', 'vsquare', (100, 158, 220, 167), (160, 160), FRONT, 'way out to the gate', ('vgate', 160, 152, FRONT))
first_visit('vsquare', 'You are in the village square. A fountain splashes in the middle. The market is east, a workshop '
            'west and the Elder\'s hut north. A lookout tower rises to the south.')

# ---- the market
hot('stall1', 'market', (13, 62, 100, 134), (60, 150), BACK, label='stall', look='Stalls piled high with fruit.')
hot('stall2', 'market', (117, 62, 203, 108), (120, 150), BACK, label='stall of shells',
    look='Shells and shiny stones. One shell on the stall seems to be singing quietly.')
hot('stall3', 'market', (220, 62, 303, 134), (260, 150), BACK, label='stall', look='Shiny stones and odd junk.')
hot('glasses_o', 'market', (244, 64, 270, 86), (256, 150), BACK, 'pickup', label='nose glasses', image='glasses', state=3,
    look='Plastic glasses with a big nose and a moustache. A label says: AS WORN BY ZAK MCKRACKEN.')
s = G.script()
s.hide('glasses_o').imgoff('glasses_o').pickup('glasses')
s.say('trader', 'Chirp! Chirrup!')
s.say('narrator', 'The trader waves: take them, nobody else wants them.')
G.on('glasses_o', 'pickup', s)
hot('trader', 'market', (138, 108, 182, 167), (120, 156), RIGHT, 'talk', label='old trader',
    look='He points at his shells and rubs his fingers together.')
s = G.script()
L = s.label()
s.iff('understand', L)
s.say('trader', 'Chirp, chirp!')
s.say('narrator', 'He chirps, points at your empty hands, then at his shells.')
s.end()
s.here(L)
s.say('trader', 'A fine shell, no? The Elder wants to see you, stranger.')
G.on('trader', 'talk', s)
s = G.script()
L = s.label()
s.has('shell', L)
s.say('narrator', 'The trader shakes his head and rubs his fingers together. He wants to be paid.')
s.end()
s.here(L).say('pilot', 'I already have the singing shell.')
G.on('stall2', 'pickup', s)
s = G.script()
s.cuton()
s.drop('starcoin')
s.say('narrator', 'The trader bites the coin, grins and hands you a spiral shell.')
s.pickup('shell')
s.say('pilot', 'It hums softly. Maybe I should listen to it?')
s.cutoff()
G.on('starcoin', 'give', s, other='trader')
G.on('starcoin', 'use', s, other='trader')
door('mk_out', 'market', (0, 40, 12, 160), (16, 152), LEFT, 'way back to the square', ('vsquare', 270, 116, FRONT))
first_visit('market', 'You are at the market. Stalls are piled high with fruit, shells and shiny stones. An old trader '
            'with a long beard waves at you.')

# ---- the Elder's hut
hot('zooma', 'elder', (134, 68, 184, 144), (120, 154), RIGHT, 'talk', label='Elder',
    look='He is very old and very wise. His eyes twinkle.')
hot('scrolls', 'elder', (218, 136, 292, 166), (210, 154), RIGHT, label='scrolls',
    look=['Drawings of a temple on a mountain, and a shining crystal heart.',
          'One scroll holds Zooma\'s most powerful spell: LOAD"$",8 - nobody knows what it does, but it takes a very '
          'long time.'])
door('el_out', 'elder', (100, 160, 220, 167), (160, 162), FRONT, 'way out to the square', ('vsquare', 110, 112, FRONT))
s = G.script()
A, B = s.label(), s.label()
s.iff('understand', A)
s.say('zooma', 'Chirrrp... chirp.')
s.say('narrator', 'The Elder chirps slowly. You do not understand a word.')
s.end()
s.here(A)
s.iff('elder_met', B)
s.cuton()
s.say('zooma', 'Welcome, child of Earth. Your amulet is the key of the Sky Temple, where the Star Heart keeps our '
      'world alive.')
s.say('zooma', 'Commander Vex has come to steal its power. Take this map. Bix the inventor can help you reach the temple.')
s.setf('elder_met').pickup('vmap')
s.cutoff()
s.end()
s.here(B)
s.say('zooma', 'Hurry to the temple, before Vex finds another way in.')
G.on('zooma', 'talk', s)
first_visit('elder', 'You are inside the Elder\'s hut. An ancient Stronkie with white fur sits on a cushion, surrounded '
            'by scrolls.')

# ---- the workshop
hot('bixs', 'workshop', (230, 98, 266, 166), (216, 156), RIGHT, 'talk', label='young Stronkie with goggles',
    look='A young Stronkie with oil on his nose and huge goggles.')
hot('machines', 'workshop', (108, 102, 226, 128), (160, 150), BACK, label='half-built glider',
    look='Gears, springs and half-built flying machines. One of them is a glider without a sail.')
hot('gears', 'workshop', (80, 18, 230, 84), None, label='gears', look='Gears. Lots of gears. Bix likes gears.')
door('ws_out', 'workshop', (0, 150, 60, 167), (20, 160), LEFT, 'way back to the square', ('vsquare', 40, 112, FRONT))
s = G.script()
A, B, C = s.label(), s.label(), s.label()
s.iff('understand', A)
s.say('bix', 'Chirp! Chirp chirp chirp!')
s.say('narrator', 'The young Stronkie chirps excitedly and waves a spanner at you.')
s.end()
s.here(A)
s.iff('elder_met', B)
s.say('bix', 'Hello, Earthling! The Elder wants to see you first.')
s.end()
s.here(B)
s.iff('glider_ready', C)
s.say('bix', 'To the temple? The bridge is broken, but my glider can fly you there! It only needs a big, strong sail.')
s.setf('bix_sail')
s.end()
s.here(C)
s.say('bix', 'Jump from the lookout tower. Good luck!')
G.on('bixs', 'talk', s)
s = G.script()
A, B = s.label(), s.label()
s.iff('understand', A)
s.say('narrator', 'Bix chirps happily, but you cannot understand what he wants.')
s.end()
s.here(A)
s.iff('elder_met', B)
s.say('bix', 'Hello, Earthling! The Elder wants to see you first.')
s.end()
s.here(B)
s.cuton()
s.drop('banner').setf('glider_ready')
s.say('narrator', 'Bix stitches the banner onto his glider.')
s.say('bix', 'Perfect! Your glider is ready. Take it up the lookout tower and JUMP!')
s.pickup('glider')
s.cutoff()
G.on('banner', 'give', s, other='bixs')
G.on('banner', 'use', s, other='machines')
G.on('banner', 'give', s, other='machines')
first_visit('workshop', 'You are in a workshop full of gears, springs and half-built flying machines. A young Stronkie '
            'with goggles is tinkering.')

# ---- the lookout tower
hot('view', 'tower', (120, 0, 319, 90), None, label='Crystal Mountains',
    look='Far away on a snowy mountain shines a temple. Near it are black tents and a dark ship! That must be Vex\'s.')
hot('banner_o', 'tower', (54, 6, 112, 46), (70, 140), BACK, 'pickup', label='big banner', image='nobanner', state=1,
    look='A big banner flaps on a pole beside me. A huge banner of strong cloth.')
s = G.script()
s.say('pilot', 'I untie the big banner from its pole.')
s.imgon('banner_o').hide('banner_o').pickup('banner')
G.on('banner_o', 'pickup', s)
G.on('banner_o', 'pull', s)
hot('nest', 'tower', (44, 0, 64, 8), (70, 140), BACK, label='top of the pole')
search('nest', 9, 'An old bird\'s nest sits at the top of the pole. In the old nest...',
       'An old bird\'s nest sits at the top of the pole.', verbs='look pickup')
hot('edge', 'tower', (0, 90, 319, 128), None, label='edge of the tower')
careful('edge', 'walk use', 'Jump? Stronkie has very strong gravity. Not without wings.')
door('tw_down', 'tower', (100, 158, 220, 167), (160, 160), FRONT, 'ladder down to the square', ('vsquare', 296, 116, FRONT))
s = G.script()
s.say('pilot', 'I need to be up high. The lookout tower!')
G.on('glider', 'use', s)
s = G.script('fly')
s.cuton()
s.say('narrator', 'You strap into the glider, take a deep breath and JUMP.')
s.sound('hyper')
s.say('narrator', 'The wind catches the sail and you soar away towards the Crystal Mountains...')
chapter_end(s, ['High above the purple jungle you glide towards the snowy peaks, the temple... and Vex.'],
            ('Chapter 7: The Crystal Mountains', 'p09_card'))
G.on('glider', 'use', s, other='edge')
G.on('glider', 'use', s, other='view')
first_visit('tower', 'You are on top of the lookout tower. Far away on a snowy mountain shines a temple. Near it are '
            'black tents and a dark ship! A big banner flaps on a pole beside you.')
s = G.rooms['tower']['enter']
L = s.label()
s.has('glider', L)
s.end()
s.here(L)
s.say('pilot', 'Here goes nothing. Time to use the glider and jump.')

# =================================================================== the start
chapter_start(['LeChuckle\'s parting shot has done its work. The STARRAVEN dives through purple clouds.',
               'Alarms scream, the engines cough... and with a terrible CRASH you land on the World of Stronkie.'],
              ('Chapter 5: Landfall', 'p07_card'), 'wreck', 150, 162, BACK, music='p08')
fv = G.rooms['wreck']['enter']
once(fv, 'intro_said', lambda s: nova(s, 'Main power crystal shattered. Pilot, I need a new power crystal to repair the ship.'))
default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {}
VARIANTS = {
    'extinguisher': ('wreck', {}, {'extinguisher': True}),
    'fireout': ('crash', {}, {'fire_out': True}),
    'nofruit': ('jungle', {}, {'fruit': False}),
    'monkey': ('jungle', {}, {'monkey': True}),
    'glasses': ('market', {}, {'glasses': True}),
    'nobanner': ('tower', {}, {'banner': False}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('wreck', 'Wreck', 150, 162), ('crash', 'Crash site', 70, 150), ('jungle', 'Jungle', 160, 156),
             ('river', 'River', 80, 156), ('ccave', 'Crystal cave', 40, 156), ('vgate', 'Gate', 60, 152),
             ('vsquare', 'Square', 160, 156), ('market', 'Market', 40, 152), ('workshop', 'Workshop', 60, 156),
             ('tower', 'Tower', 160, 156)]
DEV_ITEMS = ['extinguisher', 'fruit', 'pcrystal', 'starcoin', 'shell', 'vmap', 'banner', 'glider', 'glasses',
             'chicken', 'ration', 'paper']
