"""The story that goes from one chapter (disk) of World of Stronkie remake to the next
(like the original World of Stronkie): the story flags and the story items.
A chapter maps these names to its own flags and things with the same names; the
story file has room for 128 of each, numbered in the order below.
Never reorder these lists, only add to the end."""
FLAGS = [f'frag{n}' for n in range(1, 17)] + [   # the 16 star fragments of the true ending
    'edmund_freed',      # Prologue: freed Uncle Edmund
    'fed_monkey',        # Chapter 3/4: the monkey bonus
    'helped_trader',     # choices that matter for the ending
    'spared_guard',
    'saved_nova',
]
ITEMS = ['amulet', 'suit', 'fragments', 'knife',
         'paper', 'ration', 'feather', 'shell', 'medal', 'compass']

# the item check list: every disk gives the player one keepsake that can never be
# lost; every later disk checks the keepsakes of ALL the disks before it.
KEEPSAKES = {1: 'paper', 2: 'ration', 3: 'feather', 4: 'shell', 5: 'medal', 6: 'compass'}
KEEP_FROM = {v: k for k, v in KEEPSAKES.items()}
