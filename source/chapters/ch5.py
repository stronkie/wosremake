"""World of Stronkie remake - Chapter Five: The Crystal Mountains (disk 5).

The original game's Chapter 7 (The Crystal Mountains: the ledge, the ice cave,
Vex's camp) and Chapter 8 (The Sky Temple). Keepsake of this disk: the spiked
boots."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p10', 'p11']
for n, c in (('soldiers', 18), ('vex', 25), ('beast', 17)):
    add_actor(n, c)

# =================================================================== rooms
G.room('ledge', 'ledge', music='p10', walk=[[(80, 114), (319, 114), (319, 167), (60, 167)]])
G.room('icecave', 'icecave', music='p10', walk=[[(0, 152), (112, 152), (112, 167), (0, 167)]])
G.room('icebridge', 'icebridge', music='p10', walk=[[(0, 102), (94, 102), (98, 167), (0, 167)]])
G.room('camp', 'camp', music='p10', walk=[[(110, 138), (300, 138), (319, 167), (100, 167)]])
G.room('tent', 'tent', music='p10', walk=[FLOOR(138)])
G.room('steps', 'steps', music='p10', walk=[FLOOR(150)])
G.room('tgate', 'tgate', music='p11', walk=[[(20, 156), (300, 156), (300, 167), (20, 167)]])
G.room('statues', 'statues', music='p11', walk=[[(70, 124), (250, 124), (300, 167), (20, 167)]])
G.room('mirrors', 'mirrors', music='p11', walk=[FLOOR(140)])
G.room('starbridge', 'starbridge', music='p11', walk=[[(0, 142), (100, 142), (110, 167), (0, 167)]])
G.room('heartdoor', 'heartdoor', music='p11', walk=[ROOM3D(116)])
BLOCK = {'tent': [[(56, 132), (166, 132), (166, 152), (56, 152)]],
         'mirrors': [[(140, 140), (180, 140), (180, 152), (140, 152)]]}

# =================================================================== things you carry
G.thing('amulet', None, label='amulet', icon='amulet')
for nm, lab, ic, txt in (
        ('snowball', 'snowball', 'snowball', 'Hard and cold.'),
        ('mirror', 'silver mirror', 'mirror', 'A round mirror of polished silver.'),
        ('stardust', 'handful of star dust', 'stardust', 'It glitters and sticks to everything.')):
    G.thing(nm, None, label=lab, icon=ic)
    simple(nm, 'look', 'pilot', txt)
simple('amulet', 'look', 'pilot', 'My amulet! It glows brighter and brighter the closer I get to the temple.')
s = G.script()
s.say('pilot', 'I throw the snowball. SPLAT. Very satisfying, but not very useful here.')
s.drop('snowball')
G.on('snowball', 'use', s)
s = G.script()
L = s.label()
s.iff('spikes_on', L)
s.say('pilot', 'I pull on the spiked boots. CRUNCH! They bite into the ice.')
s.setf('spikes_on').sound('click')
s.end()
s.here(L).say('pilot', 'I am already wearing them. They grip the ice well.')
G.on('spikes', 'use', s)


def radio(s):
    s.say('narrator', 'NOVA on the radio:')
    nova(s, 'Get the amulet back, pilot. The temple needs it.', 'p10_m19')
    return s


# =================================================================== CHAPTER 7: THE CRYSTAL MOUNTAINS
# ---- the snowy ledge
hot('glider_w', 'ledge', (166, 96, 264, 150), (150, 140), RIGHT, label='wreck of the glider',
    look='It will never fly again.')
hot('snow', 'ledge', (80, 150, 319, 167), (200, 158), BACK, 'pickup', label='snow',
    look='Deep, fresh snow. Good for snowballs.')
s = G.script()
L = s.label()
s.has('snowball', L)
s.say('pilot', 'I pack a handful of snow into a hard snowball.')
s.pickup('snowball')
s.end()
s.here(L).say('pilot', 'One snowball is enough. My fingers are freezing.')
on('snow', 'pickup use', s)
door('lg_cave', 'ledge', (24, 38, 68, 98), (90, 120), LEFT, 'dark cave', ('icecave', 30, 160, RIGHT))
door('lg_east', 'ledge', (300, 70, 319, 160), (300, 140), RIGHT, 'path east', ('icebridge', 40, 150, RIGHT))
hot('peaks', 'ledge', (90, 0, 319, 90), None, label='Crystal Mountains', look='Snowy peaks and glittering crystal.')
s = G.script()
radio(s)
G.on('peaks', 'talk', s)
first_visit('ledge', 'You are on a narrow, snowy ledge high in the Crystal Mountains. The wreck of your glider lies in '
            'the snow. A path leads east, a dark cave north.')

# ---- the ice cave
hot('beast', 'icecave', (96, 98, 248, 150), (100, 160), RIGHT, 'look', label='sleeping beast',
    look='White fur, six legs and teeth like icicles. It is fast asleep, snoring loudly. Better be quiet!')
careful('beast', 'talk push pull pickup', 'Wake it up? It would open one huge eye... then its mouth.')
hot('junk', 'icecave', (124, 144, 240, 162), (110, 160), RIGHT, 'look', label='pile of junk')
search('junk', 10, 'Old ropes, broken sledges... and something that glitters. Rooting through the junk as quietly as I can...',
       'Old ropes and broken sledges.', verbs='look')
hot('spikes_o', 'icecave', (62, 136, 92, 160), (100, 160), LEFT, 'pickup', label='spiked boots', image='spikeboots',
    state=3, look='Boots with iron spikes under the soles. Perfect for ice.')
s = G.script()
s.hide('spikes_o').imgoff('spikes_o').pickup('spikes')
s.say('pilot', 'Spiked boots. Quietly now...')
G.on('spikes_o', 'pickup', s)
door('ic_out', 'icecave', (0, 96, 18, 167), (14, 160), LEFT, 'way out to the ledge', ('ledge', 90, 124, RIGHT))
first_visit('icecave', 'You are in an ice cave. A huge white beast sleeps on a pile of old junk, snoring loudly. '
            'Better be quiet!')

# ---- the ice bridge
hot('bridge', 'icebridge', (94, 78, 212, 100), (80, 106), RIGHT, 'walk', label='ice bridge',
    look='A bridge of pure ice over a bottomless gorge. One slip and I am gone.')
hot('gorge', 'icebridge', (100, 102, 200, 167), None, label='gorge', look='A bottomless gorge. Don\'t look down!')
careful('gorge', 'walk use', 'Into a bottomless gorge? Really?')
hot('tents_far', 'icebridge', (210, 56, 280, 84), None, label='black tents', look='On the other side are black tents.')
s = G.script()
A, B = s.label(), s.label()
s.iff('spikes_on', A)
s.say('narrator', 'You step onto the ice and slide straight back. You need something to grip the ice.')
s.end()
s.here(A)
s.iff('crossed', B)
s.cuton()
s.say('narrator', 'Step by step the spikes carry you across the gorge. Don\'t look down!')
s.setf('crossed')
s.room('camp', 120, 156, RIGHT)
s.cutoff()
s.end()
s.here(B)
s.room('camp', 120, 156, RIGHT)
on('bridge', 'walk', s)
door('ib_west', 'icebridge', (0, 104, 16, 167), (14, 150), LEFT, 'path west to the ledge', ('ledge', 290, 140, LEFT))
first_visit('icebridge', 'You stand at an ice bridge over a bottomless gorge. The ice is as smooth as glass. On the other '
            'side are black tents.')

# ---- Vex's camp
hot('tents', 'camp', (74, 76, 130, 110), None, label='black tents',
    look='Black tents with the sign of a raven in a circle.')
door('cp_tent', 'camp', (156, 68, 264, 126), (210, 140), BACK, 'Vex\'s tent', ('tent', 260, 156, LEFT),
     locked=('distracted', 'The soldiers would see me at once. I need to distract them.'))
door('cp_steps', 'camp', (128, 64, 156, 100), (140, 140), BACK, 'path north to the temple steps', ('steps', 160, 160, BACK),
     locked=('got_amulet', 'Without the amulet the temple will never open. Vex has it in his tent.'))
hot('soldiers_c', 'camp', (176, 94, 248, 130), (170, 150), RIGHT, 'look', label='soldiers', image='soldiers', state=3,
    look='Two soldiers in black, guarding the big tent.')
careful('soldiers_c', 'push pull talk', 'Two against one, and they have ray guns. No.')
door('cp_back', 'camp', (0, 88, 40, 167), (110, 156), LEFT, 'rock (back to the ice bridge)', ('icebridge', 80, 106, LEFT))
s = G.script()
L = s.label()
s.iff('distracted', L)
s.cuton()
s.say('pilot', 'I throw the snowball far over the tents...')
s.drop('snowball').sound('click')
s.say('narrator', 'THUMP! The soldiers spin around.')
s.say('soldiers', 'WHO GOES THERE?')
s.say('narrator', 'They run off to search the rocks.')
s.imgoff('soldiers_c').hide('soldiers_c').setf('distracted')
s.cutoff()
s.end()
s.here(L)
G.on('snowball', 'use', s, other='soldiers_c')
G.on('snowball', 'use', s, other='tents')
G.on('snowball', 'use', s, other='cp_tent')
first_visit('camp', 'You hide behind a rock at the edge of Vex\'s camp. The biggest tent is to the east. A path leads north '
            'to the temple steps.')

# ---- Vex's tent
hot('vtable', 'tent', (58, 98, 164, 132), (176, 150), LEFT, label='maps',
    look='Vex\'s plans: drain the Star Heart, sell its power, rule the galaxy. Charming.')
hot('vmachine', 'tent', (178, 80, 242, 100), (210, 146), BACK, label='strange machine',
    look='Strange machines with blinking lights. Vex likes his gadgets.')
hot('amulet_o', 'tent', (126, 104, 146, 120), (176, 150), LEFT, 'pickup', label='amulet', image='tamulet', state=3,
    look='My amulet! It glows warmly, as if it knows me.')
s = G.script()
s.hide('amulet_o').imgoff('amulet_o').pickup('amulet').setf('got_amulet').sound('score')
s.say('narrator', 'You grab the amulet. It glows warmly in your hand, as if it knows you.')
G.on('amulet_o', 'pickup', s)
door('tn_out', 'tent', (290, 40, 319, 160), (296, 150), RIGHT, 'way out of the tent', ('camp', 210, 140, FRONT))
first_visit('tent', 'You are inside Commander Vex\'s tent. Maps and strange machines cover a table.')

# ---- the temple steps
hot('stairs_t', 'steps', (60, 0, 260, 148), (160, 156), BACK, 'walk', label='crystal stairs',
    look='Crystal stairs, glittering all the way to the temple.')
door('sp_back', 'steps', (0, 152, 60, 167), (30, 160), LEFT, 'path back to the camp', ('camp', 140, 140, FRONT))
s = G.script('climb')
s.cuton()
s.say('narrator', 'You climb the endless crystal stairs.')
s.say('narrator', 'Far below, an angry shout echoes from the camp: Vex has found his tent empty!')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
spoken_card(s, 'Chapter 8: The Sky Temple', 'p10_card')
s.card('At the top of the stairs stands the Sky Temple, carved from one giant crystal. The wind howls.', wait=True)
s.card('Somewhere far below, boots are marching up the steps.', wait=True)
s.music('p11')
s.room('tgate', 160, 162, BACK)
s.cutoff()
on('stairs_t', 'walk', s)
s = G.script('steps_in')
L = s.label()
s.iff('seen_steps', L)
s.setf('seen_steps')
s.say('narrator', 'You stand at the foot of the temple steps. Thousands of crystal stairs climb up to the shining Sky Temple.')
s.say('narrator', 'A figure in black sneaks across the steps, rolls... and vanishes. Just the Last Ninja, on his way to '
      'some other game.')
s.here(L)
G.rooms['steps']['enter'] = s

# =================================================================== CHAPTER 8: THE SKY TEMPLE
# ---- the gate
hot('tgate_g', 'tgate', (90, 8, 226, 150), (160, 160), BACK, 'open', label='crystal gate',
    look='A gate of solid crystal with a round hollow in the middle, exactly the size of my amulet.')
s = G.script()
L = s.label()
s.iff('gate_t', L)
s.say('pilot', 'It has no handle. Only a round hollow.')
s.end()
s.here(L)
s.room('statues', 160, 156, BACK)
on('tgate_g', 'open walk', s)
s = G.script()
L = s.label()
s.iff('gate_t', L)
s.cuton()
s.say('pilot', 'I press the amulet into the hollow.')
s.sound('beep').setf('gate_t')
s.say('narrator', 'The gate glows and slides open without a sound. You take the amulet back.')
s.cutoff()
s.end()
s.here(L).say('pilot', 'The gate is already open.')
G.on('amulet', 'use', s, other='tgate_g')
line('amulet', 'give', 'I hold on to it. I will need it.')
first_visit('tgate', 'You stand before the gate of the Sky Temple. In the middle of the gate is a round hollow, exactly '
            'the size of your amulet.')

# ---- the hall of statues
hot('statues_l', 'statues', (6, 46, 122, 160), (80, 150), LEFT, label='statues')
search('statues_l', 11, 'Ancient Stronkie heroes. Their crystal eyes seem to follow me. Behind the feet of a stone hero...',
       'Ancient Stronkie heroes. Their crystal eyes seem to follow me.', verbs='look')
hot('statue_r', 'statues', (200, 46, 300, 160), (210, 150), RIGHT, label='statue',
    look='A stone hero. It holds a round silver mirror.')
hot('mirror_o', 'statues', (226, 76, 250, 110), (210, 150), RIGHT, 'pickup', label='silver mirror', image='nomirror',
    state=1, look='A round mirror of polished silver.')
s = G.script()
s.say('pilot', 'I gently take the mirror from the statue\'s hands.')
s.imgon('mirror_o').hide('mirror_o').pickup('mirror')
G.on('mirror_o', 'pickup', s)
hot('dust', 'statues', (90, 136, 230, 167), (160, 156), BACK, 'pickup', label='star dust',
    look=['Fine star dust. It clings to everything it touches.', 'Somebody has drawn a big X in it. X never, ever marks '
          'the spot.'])
s = G.script()
L = s.label()
s.has('stardust', L)
s.say('pilot', 'I scoop up a handful of glittering dust.')
s.pickup('stardust')
s.end()
s.here(L).say('pilot', 'One handful is enough. It sticks to everything.')
G.on('dust', 'pickup', s)
line('dust', 'use open push', 'I dig at the X. Nothing. As every archaeologist knows: X never, ever marks the spot.')
door('st_south', 'statues', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the gate', ('tgate', 160, 162, BACK))
door('st_east', 'statues', (130, 20, 196, 110), (160, 126), BACK, 'passage', ('mirrors', 30, 156, RIGHT))
first_visit('statues', 'You are in the Hall of Statues. Stone Stronkies with crystal eyes line the walls. One of them holds '
            'a mirror. Glittering dust covers the floor. Somebody has drawn a big X in it.')

# ---- the round room
hot('eyedoor', 'mirrors', (120, 4, 182, 112), (160, 146), BACK, 'open', label='door with a crystal eye')
s = G.script()
L = s.label()
s.iff('eye_open', L)
s.say('pilot', 'A door with a big crystal eye. It looks at the stand.')
s.end()
s.here(L).say('pilot', 'The door stands open.')
G.on('eyedoor', 'look', s)
s = G.script()
L = s.label()
s.iff('eye_open', L)
s.say('pilot', 'The door with the crystal eye is closed.')
s.end()
s.here(L)
s.room('starbridge', 40, 156, RIGHT)
on('eyedoor', 'open walk', s)
hot('stand', 'mirrors', (140, 112, 180, 152), (190, 150), LEFT, label='stand in the sunbeam', image='mstand', state=1,
    look='A stand with a round frame, right in the sunbeam. It looks empty.')
s = G.script()
s.cuton()
s.say('pilot', 'I place the mirror on the stand.')
s.drop('mirror').imgon('stand').setf('eye_open').sound('beep')
s.say('narrator', 'The sunbeam bounces straight into the crystal eye... and the door swings open!')
s.cutoff()
G.on('mirror', 'use', s, other='stand')
G.on('mirror', 'use', s, other='eyedoor')
door('mr_west', 'mirrors', (0, 40, 16, 167), (16, 156), LEFT, 'passage back to the statues', ('statues', 160, 130, FRONT))
first_visit('mirrors', 'You are in a round room. A beam of sunlight falls through the roof onto an empty stand. In the north '
            'wall is a door with a crystal eye.')

# ---- the starbridge
hot('void', 'starbridge', (112, 0, 319, 167), (100, 150), RIGHT, 'look', label='void', image='bridge', state=1)
s = G.script()
L = s.label()
s.iff('bridge_on', L)
s.say('pilot', 'Nothing but stars and darkness. Or is there something I cannot see?')
s.end()
s.here(L).say('pilot', 'A glittering bridge of star dust, all the way to the golden door.')
G.on('void', 'look', s)
s = G.script()
L = s.label()
s.iff('bridge_on', L)
s.say('pilot', 'I step into the void... and quickly pull my foot back. There is nothing there!')
s.end()
s.here(L)
s.say('narrator', 'You walk across the glittering bridge...')
s.room('heartdoor', 160, 160, BACK)
on('void', 'walk use', s)
hot('gdoor_far', 'starbridge', (238, 40, 272, 94), None, label='golden door', look='Far across the void glows a golden door.')
s = G.script()
s.cuton()
s.say('pilot', 'I throw the star dust into the void.')
s.drop('stardust').sound('hyper')
s.say('narrator', 'It settles on something invisible... a glittering bridge appears!')
s.imgon('void').setf('bridge_on')
s.cutoff()
G.on('stardust', 'use', s, other='void')
G.on('stardust', 'use', s, other='gdoor_far')
door('sb_back', 'starbridge', (0, 142, 16, 167), (10, 160), LEFT, 'door back to the round room', ('mirrors', 160, 146, FRONT))
first_visit('starbridge', 'You stand at the edge of an endless drop. Stars float in the air, but there is no bridge. Far '
            'across the void glows a golden door.')

# ---- the golden door
hot('heartdoor_d', 'heartdoor', (100, 0, 220, 112), (160, 124), BACK, 'open', label='golden door',
    look=['A golden door covered in symbols. Behind it I hear a deep, slow heartbeat.',
          'The symbols look like the ones on my amulet.'])
door('hd_back', 'heartdoor', (100, 158, 220, 167), (160, 160), FRONT, 'bridge back', ('starbridge', 90, 150, RIGHT))
s = G.script('heart_open')
s.cuton()
s.say('narrator', 'The symbols light up one by one as you hold up the amulet. The golden door opens.')
s.sound('beep')
s.say('narrator', 'Then a cold voice behind you says:')
s.say('vex', 'Thank you for opening the way.')
s.say('pilot', 'Commander Vex!')
chapter_end(s, ['To be continued... the Star Heart is in danger!'], ('Chapter 9: The Star Heart', 'p11_card'))
on('heartdoor_d', 'open walk', s)
G.on('amulet', 'use', s, other='heartdoor_d')
first_visit('heartdoor', 'You stand before a golden door covered in symbols. Behind it you hear a deep, slow heartbeat.')

# =================================================================== the start
chapter_start(['The glider carries you high over forests and rivers, until a storm throws you down on a snowy ledge.'],
              ('Chapter 7: The Crystal Mountains', 'p09_card'), 'ledge', 200, 140, LEFT, music='p10')
fv = G.rooms['ledge']['enter']
fv.say('narrator', 'NOVA on your radio:')
nova(fv, 'Pilot! Someone broke into the STARRAVEN and took the amulet. The tracks lead to the black tents!')
default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {}
VARIANTS = {
    'spikeboots': ('icecave', {}, {'boots': True}),
    'soldiers': ('camp', {}, {'soldiers': True}),
    'tamulet': ('tent', {}, {'amulet': True}),
    'nomirror': ('statues', {}, {'mirror': False}),
    'mstand': ('mirrors', {}, {'mirror': True}),
    'bridge': ('starbridge', {}, {'bridge': True}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('ledge', 'Ledge', 200, 140), ('icecave', 'Ice cave', 30, 160), ('icebridge', 'Ice bridge', 40, 150),
             ('camp', 'Camp', 120, 156), ('tent', 'Tent', 260, 156), ('steps', 'Steps', 160, 160),
             ('tgate', 'Temple gate', 160, 162), ('statues', 'Statues', 160, 156), ('mirrors', 'Round room', 30, 156),
             ('starbridge', 'Starbridge', 40, 156)]
DEV_ITEMS = ['snowball', 'spikes', 'amulet', 'mirror', 'stardust', 'shell', 'chicken', 'ration', 'paper']
