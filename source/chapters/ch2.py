"""World of Stronkie remake - Chapter Two: Into Space (disk 2).

The original game's Chapter 1 (Into Space: the STARRAVEN) and Chapter 2 (The
Derelict Station: KX-9), with the same story, rooms, pictures, puzzles, music
and speech, played with the mouse. Keepsake of this disk: the space ration."""
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters', 'common.py')).read(), 'common.py', 'exec'))
SONGS = ['title', 'p04', 'p05']
add_actor('robot', 22)

# =================================================================== rooms
G.room('cockpit', 'cockpit', music='p04', walk=[[(30, 156), (290, 156), (290, 167), (30, 167)]])
G.room('shipcorr', 'shipcorr', music='p04', walk=[[(110, 124), (210, 124), (300, 167), (20, 167)]])
G.room('galley', 'galley', music='p04', walk=[ROOM3D(112)])
G.room('engine', 'engine', music='p04', walk=[ROOM3D(104)])
G.room('cargo', 'cargo', music='p04', walk=[[(10, 112), (104, 112), (104, 167), (0, 167)]])
G.room('airlock', 'airlock', music='p04', walk=[ROOM3D(116)])
G.room('dock', 'dock', music='p05', walk=[[(124, 120), (300, 120), (319, 167), (128, 167)]])
G.room('stcorr', 'stcorr', music='p05', walk=[[(128, 104), (192, 104), (300, 167), (20, 167)]])
G.room('quarters', 'quarters', music='p05', walk=[ROOM3D(104)])
G.room('power', 'power', music='p05', walk=[ROOM3D(106)])
G.room('maproom', 'maproom', music='p05', walk=[[(206, 112), (296, 112), (319, 167), (186, 167)]])
BLOCK = {'galley': [[(88, 112), (182, 112), (182, 132), (88, 132)]]}

# =================================================================== things you carry
G.thing('crowbar', None, label='crowbar', icon='crowbar')
G.thing('crystal', None, label='navigation crystal', icon='crystal')
G.thing('boots', None, label='magnetic boots', icon='boots')
G.thing('chart', None, label='star chart disc', icon='disc')
simple('crowbar', 'look', 'pilot', 'A heavy red crowbar.')
simple('crystal', 'look', 'pilot', 'A blue crystal that hums quietly.')
simple('chart', 'look', 'pilot', 'A shiny disc. It holds the route to the World of Stronkie.')
s = G.script()
L = s.label()
s.iff('boots_on', L)
s.say('pilot', 'Heavy boots with magnets in the soles. For walking without gravity.')
s.end()
s.here(L).say('pilot', 'My magnetic boots. They clank on the floor with every step.')
G.on('boots', 'look', s)
s = G.script()
L = s.label()
s.iff('boots_on', L)
s.say('pilot', 'I pull on the magnetic boots. CLANK! They stick to the floor.')
s.setf('boots_on').sound('click')
s.end()
s.here(L).say('pilot', 'I am already wearing them.')
G.on('boots', 'use', s)
G.on('boots', 'pull', s)
s = G.script()
s.say('pilot', 'It tastes like cardboard, I bet. I\'ll keep it: my lucky space ration.')
G.on('ration', 'use', s)

# =================================================================== CHAPTER 1: INTO SPACE
# ---- the cockpit
hot('window', 'cockpit', (40, 0, 280, 96), None, label='window',
    look='The Earth, already far away. Somewhere down there is Ravenmoor.')
hot('navscreen', 'cockpit', (120, 118, 200, 152), (160, 160), BACK, label='navigation screen')
s = G.script()
L = s.label()
s.iff('nav_ok', L)
s.say('pilot', 'It reads: NAVIGATION CRYSTAL CRACKED. INSERT SPARE CRYSTAL.')
s.end()
s.here(L).say('pilot', 'COURSE FOUND: STATION KX-9. The screen glows a happy green.')
G.on('navscreen', 'look', s)
hot('c_amulet', 'cockpit', (150, 100, 170, 116), (160, 160), BACK, label='amulet',
    look='The amulet sits in the console, glowing softly. It powers the whole ship.')
line('c_amulet', 'pickup pull', 'If I take it out, the whole ship goes dark. It stays where it is.')
hot('throttle', 'cockpit', (198, 114, 222, 154), (200, 160), BACK, 'push', label='hyperdrive throttle',
    look='The hyperdrive throttle. Only use it when navigation works.')
hot('novascreen', 'cockpit', (30, 118, 96, 152), (64, 160), BACK, 'talk', label='NOVA',
    look='NOVA has no body, just a calm voice that is everywhere on the ship.')
hot('rightscreen', 'cockpit', (226, 118, 292, 152), (256, 160), BACK, label='engine screen',
    look='The engine screen. Everything is green, except my nerves.')
door('c_out', 'cockpit', (0, 100, 28, 167), (34, 162), LEFT, 'way back to the corridor', ('shipcorr', 160, 130, FRONT))

# NOVA
s = G.script('nova_talk')
A, B, C, D, E = (s.label() for _ in range(5))
s.here(A)
s.dialog([('NOVA, what do we do now?', B, None),
          ('Make it so!', C, None),
          ('Where are we going?', D, None),
          ('Nothing. Carry on.', E, None)])
s.here(B)
L = s.label()
s.iff('nav_ok', L)
nova(s, 'The navigation crystal cracked during the launch. There should be a spare in the cargo hold.', 'p04_m03')
s.jmp(A)
s.here(L)
nova(s, 'All systems ready. Engage the hyperdrive in the cockpit.', 'p04_m04')
s.jmp(A)
s.here(C)
s.say('pilot', 'Make it so!')
nova(s, 'Engaging... nothing, pilot. I am not that kind of starship.', 'p04_m01')
s.say('narrator', 'You shall be missed, Sir Patrick Stewart - our Captain Jean-Luc Picard of Star Trek. 1940-2026.')
s.jmp(A)
s.here(D)
nova(s, 'The amulet has woken me. Together we must find the lost World of Stronkie.')
s.jmp(A)
s.here(E).end()
G.on('novascreen', 'talk', s)
G.on('c_amulet', 'talk', s)

# the throttle: the end of Chapter 1
s = G.script('hyper')
L = s.label()
s.iff('nav_ok', L)
nova(s, 'Without navigation we could end up inside a sun, pilot.', 'p04_m16')
s.sound('error')
s.end()
s.here(L)
s.cuton()
s.say('pilot', 'Hold on to something, NOVA.')
s.sound('hyper')
s.say('narrator', 'You push the throttle forward. The stars stretch into long white lines...')
s.fade(0)
s.room('cards', 0, 0)
s.put('pilot', None, 0, 0)
s.card('The STARRAVEN leaps into hyperspace!', wait=True)
spoken_card(s, 'Chapter 2: The Derelict Station', 'p04_card')
s.card('The STARRAVEN drops out of hyperspace next to a huge, silent space station: KX-9. NOVA docks the ship.',
       wait=True)
s.music('p05')
s.room('dock', 200, 150, RIGHT)
nova(s, 'The star chart should be in the map room. Be careful, pilot. Nobody has lived here for a hundred years.')
s.cutoff()
on('throttle', 'push pull use', s)

# the crystal into the console
s = G.script()
s.cuton()
s.say('pilot', 'I slot the crystal into the console.')
s.drop('crystal').setf('nav_ok').sound('score')
s.say('narrator', 'The navigation screen lights up!')
nova(s, 'Course found. The star chart to Stronkie is kept on the old station KX-9. Ready for hyperdrive, pilot.',
     'p04_m13')
s.cutoff()
for o in ('navscreen', 'c_amulet', 'throttle', 'rightscreen'):
    G.on('crystal', 'use', s, other=o)

# ---- the corridor of the ship
hot('sc_lights', 'shipcorr', (110, 20, 210, 40), None, label='lights', look='Little green lights. Everything works. Mostly.')
door('sc_cockpit', 'shipcorr', (136, 40, 184, 120), (160, 126), BACK, 'door to the cockpit', ('cockpit', 60, 162, RIGHT))
door('sc_galley', 'shipcorr', (0, 10, 56, 150), (40, 150), LEFT, 'galley', ('galley', 280, 150, LEFT))
door('sc_engine', 'shipcorr', (264, 10, 319, 150), (280, 150), RIGHT, 'engine room', ('engine', 40, 150, RIGHT))
door('sc_airlock', 'shipcorr', (122, 152, 198, 167), (160, 158), FRONT, 'ladder down to the airlock',
     ('airlock', 50, 150, RIGHT))
G.thing('sc_cargo', 'shipcorr', (56, 112, 108, 140), (100, 134), LEFT, 'walk', label='cargo hold')
s = G.script()
L = s.label()
s.iff('boots_on', L)
s.cuton()
s.say('narrator', 'The gravity is off in the cargo hold. You float helplessly back into the corridor.')
s.say('pilot', 'I need something to keep my feet on the floor.')
s.cutoff()
s.end()
s.here(L)
s.say('pilot', 'CLANK. CLANK. CLANK.')
s.room('cargo', 40, 150, RIGHT)
on('sc_cargo', 'walk open', s)
first_visit('shipcorr', 'You are in the ship\'s main corridor. The cockpit is north, the galley west, the engine room '
            'east and the cargo hold south. A ladder leads down to the airlock.')

# ---- the galley
hot('porthole', 'galley', (140, 30, 180, 72), (160, 118), BACK, label='porthole',
    look='Outside, a purple moon drifts slowly past.')
hot('dispenser', 'galley', (196, 30, 236, 96), (216, 118), BACK, 'push', label='food dispenser',
    look='A food dispenser with one button. The label says: PRESS FOR FOOD.')
hot('ration_o', 'galley', (204, 70, 228, 84), (216, 118), BACK, 'pickup', label='space ration', image='ration', state=0,
    look='A grey bar wrapped in foil. It smells like nothing at all.')
s = G.script()
L = s.label()
s.iff('rationed', L)
s.sound('beep')
s.say('narrator', 'The machine beeps and drops a space ration into the tray.')
s.setf('rationed').show('ration_o').imgon('ration_o')
s.end()
s.here(L).say('narrator', 'The machine says: ONE RATION PER PILOT.')
on('dispenser', 'push use', s)
s = G.script()
s.hide('ration_o').imgoff('ration_o').pickup('ration')
s.say('pilot', 'A space ration. I\'ll keep it for later. Or forever.')
G.on('ration_o', 'pickup', s)
hot('table', 'galley', (88, 98, 182, 124), (134, 140), BACK, label='table')
search('table', 4, 'A white table bolted to the floor. I look under it... stuck to the floor, there!',
       'A white table bolted to the floor.', verbs='look')
door('ga_out', 'galley', (296, 30, 319, 160), (290, 150), RIGHT, 'corridor', ('shipcorr', 60, 150, RIGHT))
first_visit('galley', 'You are in the galley. A food dispenser hums in the corner. Stars drift past a round porthole.')

# ---- the engine room
hot('reactor', 'engine', (128, 10, 182, 104), (156, 110), BACK, label='reactor',
    look='The reactor core burns like a little sun. Better not touch the glass.')
line('reactor', 'push pull use pickup open', 'Ouch! The glass is hot. I pull my hand back.')
hot('rack', 'engine', (216, 40, 252, 96), (236, 110), BACK, label='tool rack', look='A rack of tools. Most are bolted down.')
hot('crowbar_o', 'engine', (220, 44, 240, 92), (236, 110), BACK, 'pickup', label='crowbar', image='crowbar', state=3,
    look='A heavy red crowbar. That one is not bolted down.')
s = G.script()
s.hide('crowbar_o').imgoff('crowbar_o').pickup('crowbar')
G.on('crowbar_o', 'pickup', s)
hot('pipes', 'engine', (76, 30, 110, 112), None, label='pipes', look='Pipes. They gurgle.')
door('en_out', 'engine', (0, 30, 24, 160), (30, 150), LEFT, 'corridor', ('shipcorr', 260, 150, LEFT))
first_visit('engine', 'You are in the engine room. The reactor glows behind thick glass. A tool rack hangs on the wall.')

# ---- the cargo hold
hot('crates_f', 'cargo', (56, 20, 260, 92), None, label='floating crates',
    look='Crates float around me. My magnetic boots keep me on the floor.')
hot('crate', 'cargo', (106, 94, 214, 167), (100, 150), RIGHT, 'open', label='big crate')
hot('crystal_o', 'cargo', (150, 90, 170, 108), (100, 150), RIGHT, 'pickup', label='navigation crystal',
    image='crystal', state=0, look='A blue crystal that hums quietly.')
s = G.script()
L = s.label()
s.iff('crate_open', L)
s.say('pilot', 'A big crate marked SPARE PARTS. Its lid is sealed shut.')
s.end()
s.here(L).say('pilot', 'The crate is open. Spare parts, spare parts, more spare parts.')
G.on('crate', 'look', s)
s = G.script('open_crate')
L, K = s.label(), s.label()
s.iff('crate_open', L)
s.has('crowbar', K)
s.say('pilot', 'The lid is sealed shut. I need something to pry it open.')
s.end()
s.here(K)
s.say('pilot', 'I wedge the crowbar under the lid and heave...')
s.sound('click').setf('crate_open').imgon('crate').show('crystal_o').imgon('crystal_o')
s.say('narrator', 'The crate pops open. Among the spare parts lies a blue navigation crystal!')
s.end()
s.here(L).say('pilot', 'It is already open.')
on('crate', 'open pull push', s)
G.on('crowbar', 'use', s, other='crate')
G.objects['crate']['image'] = 'crateopen'
G.objects['crate']['state'] = 1
s = G.script()
s.hide('crystal_o').imgoff('crystal_o').pickup('crystal')
G.on('crystal_o', 'pickup', s)
door('ca_out', 'cargo', (0, 30, 20, 160), (20, 150), LEFT, 'corridor', ('shipcorr', 90, 140, RIGHT))
first_visit('cargo', 'You are in the cargo hold. Your magnetic boots keep you on the floor while crates float around '
            'you. One big crate is marked PARTS.')

# ---- the airlock
hot('outer', 'airlock', (120, 20, 230, 140), (176, 140), BACK, 'look', label='outer door',
    look='The outer door. A sign says: DANGER! NEVER OPEN WITHOUT A SPACESUIT.')
careful('outer', 'open pull push use', 'If I open that, the air rushes out into space... and me with it.')
hot('redlight', 'airlock', (148, 0, 172, 20), None, label='red light', look='It blinks. Red means: no.')
hot('bootrack', 'airlock', (250, 58, 292, 120), (270, 130), BACK, label='rack', look='A rack for boots.')
hot('boots_o', 'airlock', (254, 88, 290, 112), (270, 130), BACK, 'pickup', label='magnetic boots', image='boots',
    state=3, look='Heavy boots with magnets in the soles. For walking without gravity.')
s = G.script()
s.hide('boots_o').imgoff('boots_o').pickup('boots')
G.on('boots_o', 'pickup', s)
door('al_out', 'airlock', (0, 30, 24, 160), (30, 150), LEFT, 'ladder up to the corridor', ('shipcorr', 160, 150, BACK))
first_visit('airlock', 'You are in the airlock. A round outer door leads into space and a red light blinks above it. '
            'There is a rack on the wall.')

# =================================================================== CHAPTER 2: THE DERELICT STATION
# ---- the docking bay
hot('ship', 'dock', (0, 94, 120, 160), (130, 150), LEFT, 'walk', label='STARRAVEN',
    look='My ship, waiting for me. NOVA\'s lights blink in the cockpit.')
hot('planet_d', 'dock', (150, 10, 200, 50), None, label='moon', look='A grey moon. It has seen better centuries.')
door('dk_out', 'dock', (282, 40, 319, 118), (290, 130), RIGHT, 'dark corridor', ('stcorr', 160, 160, BACK))
s = G.script('dock_ship')
L = s.label()
s.has('chart', L)
nova(s, 'Not without the star chart, pilot!', 'p05_m18')
s.end()
s.here(L)
s.cuton()
s.say('narrator', 'You climb aboard and slot the star chart into the console.')
s.room('cockpit', 0, 0)
s.put('pilot', None, 0, 0)
nova(s, 'Course plotted for the World of Stronkie. Hold on, pilot!', 'p05_m17')
s.sound('hyper')
R = s.label()
s.has('ration', R)
s.say('narrator', 'On your way through the galley you grab a space ration. Your lucky ration.')
s.pickup('ration')
s.here(R)
s.say('narrator', 'The STARRAVEN blasts away from KX-9, towards a distant ringed planet...')
s.say('narrator', '...but first, a few detours.')
chapter_end(s, ['KX-9 grows small behind you. The star chart is yours!'],
            ('Chapter 3: Asteroid 42', 'p05_card'))
on('ship', 'walk open use', s)
s = G.script()
A, B, C, D = (s.label() for _ in range(4))
s.here(A)
s.dialog([('NOVA, can you hear me?', B, None), ('Make it so!', C, None), ('Bye, NOVA.', D, None)])
s.here(B)
L = s.label()
s.iff('power_on', L)
s.say('narrator', 'NOVA\'s voice in your helmet:')
nova(s, 'The station has no power. Find the generator.', 'p05_m19')
s.jmp(A)
s.here(L)
s.say('narrator', 'NOVA\'s voice in your helmet:')
nova(s, 'Get the star chart and come back.', 'p05_m20')
s.jmp(A)
s.here(C)
s.say('pilot', 'Make it so!')
nova(s, 'Engaging... nothing, pilot. I am not that kind of starship.', 'p05_m01')
s.jmp(A)
s.here(D).end()
G.on('ship', 'talk', s)
first_visit('dock', 'You are in the docking bay of station KX-9. The STARRAVEN rests behind you. '
            'A dark corridor leads east.')

# ---- the station corridor
hot('wires', 'stcorr', (96, 0, 224, 26), None, label='sparking wires',
    look='Torn power cables, still sparking. Don\'t touch them!')
careful('wires', 'pickup pull push use', 'ZZZAP! A hundred-year-old power cable still has plenty of power left.')
door('st_dock', 'stcorr', (110, 158, 210, 167), (160, 160), FRONT, 'way back to the docking bay', ('dock', 270, 140, LEFT))
door('st_quarters', 'stcorr', (0, 10, 64, 150), (50, 150), LEFT, 'crew quarters', ('quarters', 160, 160, BACK))
door('st_map', 'stcorr', (128, 30, 192, 100), (160, 108), BACK, 'map room door', ('maproom', 250, 150, LEFT),
     locked=('power_on', 'The map room door is dead. There is no power.'))
door('st_power', 'stcorr', (290, 10, 319, 150), (270, 150), RIGHT, 'door to the power room',
     ('power', 160, 160, BACK),
     locked=('robot_off', 'The robot blocks the way. "ACCESS CODE REQUIRED."'))
hot('robot', 'stcorr', (216, 70, 258, 140), (200, 150), RIGHT, 'talk', label='security robot', image='robot', state=3,
    look='A tall robot with a red eye blocks the south door. The number 001 is painted on its chest.')
hot('robot2', 'stcorr', (262, 56, 300, 124), None, label='switched-off robot', image='robotoff', state=0,
    look='It stands quietly in the corner, its eye dark.')
line('robot', 'push pull use', 'My fist clangs off its armour. The robot gives me a warning zap. Ouch!')
line('robot', 'pickup', 'It weighs more than a car.')
s = G.script()
A, B, C, D, OK, NO = (s.label() for _ in range(6))
s.say('robot', 'ACCESS CODE REQUIRED.')
s.here(A)
s.dialog([('The code is 1985.', OK, 'code_seen'),
          ('The code is 1234.', NO, None),
          ('The code is 0000.', NO, None),
          ('Open sesame!', NO, None),
          ('Never mind.', D, None)])
s.here(NO)
s.sound('error')
s.say('robot', 'ACCESS DENIED.')
s.jmp(A)
s.here(OK)
s.cuton()
s.say('robot', 'ACCESS GRANTED.')
s.sound('beep')
s.say('narrator', 'The robot\'s eye turns green. It rolls aside and switches itself off.')
s.imgoff('robot').hide('robot').show('robot2').imgon('robot2').setf('robot_off')
s.cutoff()
s.end()
s.here(D).end()
G.on('robot', 'talk', s)
s = G.script('stcorr_in')
L = s.label()
s.iff('robot_met', L)
s.setf('robot_met')
s.cuton()
s.sound('beep')
s.say('narrator', 'Something clanks in the dark. A red eye turns towards you and a metallic voice booms:')
s.say('robot', 'ANOTHER VISITOR. STAY A WHILE... STAY FOREVER!')
s.say('narrator', 'You are in a long station corridor. Torn wires spark from the ceiling. Doors lead north, south and east.')
s.cutoff()
s.here(L)
G.rooms['stcorr']['enter'] = s

# ---- the crew quarters
hot('bunks', 'quarters', (60, 34, 152, 96), (106, 112), BACK, label='bunks')
search('bunks', 5, 'The bunks are empty and covered in dust. Under a dusty mattress...',
       'The bunks are empty and covered in dust.', verbs='look pickup push pull open')
hot('terminal', 'quarters', (196, 46, 254, 92), (226, 112), BACK, label='terminal')
s = G.script()
s.say('pilot', 'The last log entry reads: "SECURITY CODE CHANGED TO 1985. DO NOT FORGET IT AGAIN, ZORG!"')
s.setf('code_seen')
on('terminal', 'look use push', s)
door('qu_out', 'quarters', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the corridor', ('stcorr', 60, 150, RIGHT))
first_visit('quarters', 'You are in the old crew quarters. Empty bunks line the wall. A computer terminal still '
            'flickers in the corner.')

# ---- the power room
hot('generator', 'power', (98, 14, 168, 106), (134, 112), BACK, label='generator')
s = G.script()
L = s.label()
s.iff('power_on', L)
s.say('pilot', 'A huge generator. It is switched off.')
s.end()
s.here(L).say('pilot', 'The generator roars. The lights are on all over the station.')
G.on('generator', 'look', s)
hot('switch', 'power', (222, 42, 258, 98), (240, 112), BACK, 'pull', label='big switch',
    look='A big switch with two positions: ON and OFF.')
s = G.script()
L = s.label()
s.iff('power_on', L)
s.cuton()
s.say('pilot', 'I throw the switch.')
s.sound('zap')
s.say('narrator', 'The generator coughs, then roars into life. All over the station the lights flicker on!')
s.setf('power_on')
s.cutoff()
s.end()
s.here(L).say('pilot', 'The generator is already running.')
on('switch', 'pull push use', s)
G.on('generator', 'use', s)
door('pw_out', 'power', (100, 158, 220, 167), (160, 160), FRONT, 'way back to the corridor', ('stcorr', 250, 150, LEFT))
first_visit('power', 'You are in the power room. A huge generator stands silent. A big switch on the wall is set to OFF.')

# ---- the map room
hot('holo', 'maproom', (66, 30, 196, 100), (210, 140), LEFT, label='hologram',
    look='A ringed planet slowly turns in the air: the World of Stronkie! Under it the table shows a star chart disc.')
hot('maptable', 'maproom', (56, 104, 206, 140), (210, 140), LEFT, label='round table', look='A round table. It hums.')
hot('chart_o', 'maproom', (120, 110, 144, 122), (210, 140), LEFT, 'pickup', label='star chart disc', image='chart', state=3,
    look='A shiny disc. It holds the route to the World of Stronkie.')
s = G.script()
s.hide('chart_o').imgoff('chart_o').pickup('chart')
s.say('narrator', 'You pull the star chart disc out of the table. The hologram flickers.')
G.on('chart_o', 'pickup', s)
door('mp_out', 'maproom', (296, 30, 319, 160), (290, 150), RIGHT, 'way back to the corridor', ('stcorr', 160, 110, FRONT))
first_visit('maproom', 'You are in the map room. Above a round table floats a hologram of a planet with rings: '
            'the World of Stronkie!')


# =================================================================== the start
chapter_start(['The STARRAVEN breaks free of the Earth. A calm voice fills the cabin...'],
              ('Chapter 1: Into Space', 'say_c1'), 'cockpit', 160, 162, BACK, music='p04')
fv = first_visit('cockpit', 'You are in the cockpit of the STARRAVEN. Through the window the Earth glows blue. '
                 'The navigation screen flashes an error.')
once(fv, 'intro_said', lambda s: nova(s, 'Hello, pilot. I am NOVA, the ship\'s computer. The amulet has woken me. '
     'Together we must find the lost World of Stronkie.'))

default_answers()
VOICES = {a[0]: a[3] for a in ACTORS}

START_ACTORS = {}
VARIANTS = {
    'ration': ('galley', {}, {'ration': True}),
    'crowbar': ('engine', {}, {'crowbar': True}),
    'crateopen': ('cargo', {}, {'open_': True}),
    'crystal': ('cargo', {}, {'open_': True, 'crystal': True}),
    'boots': ('airlock', {}, {'boots': True}),
    'robot': ('stcorr', {}, {'robot_on': True}),
    'robotoff': ('stcorr', {}, {'robot_off': True}),
    'chart': ('maproom', {}, {'chart': True}),
}
STORY_DEFAULT = ((), ())
DEV_SPOTS = [('cockpit', 'Cockpit', 160, 162), ('shipcorr', 'Corridor', 160, 150), ('galley', 'Galley', 250, 150),
             ('cargo', 'Cargo', 40, 150), ('airlock', 'Airlock', 60, 150), ('dock', 'Dock', 200, 150),
             ('stcorr', 'Station', 160, 150), ('quarters', 'Quarters', 160, 150), ('power', 'Power', 160, 150),
             ('maproom', 'Map room', 250, 150)]
DEV_ITEMS = ['crowbar', 'crystal', 'boots', 'chart', 'ration', 'paper']
