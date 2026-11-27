"""The story that goes from one chapter (disk) of World of Stronkie remake to the next
(like the original World of Stronkie): the story flags and the story items.
A chapter maps these names to its own flags and things with the same names; the
story file has room for 128 of each, numbered in the order below.
Never reorder these lists, only add to the end."""
FLAGS = [f'frag{n}' for n in range(1, 17)] + [   # the 16 star fragments of the true ending
    'edmund_freed',      # Prologue: freed Uncle Edmund
    'napkin_given',      # Chapter 3: gave the napkin to the janitor -> Chapter 12: Roger's keycard
    'kicked_chicken',    # Chapter 3: kicked the Astro Chicken machine -> Chapter 11: the guards' badge
    'untied_crewman',    # Chapter 4: untied Ricky -> Chapter 13: the plasma spanner
    'said_grandmother',  # Chapter 4: won LeChuckle's rematch -> Chapter 13: the pirates refuse Vex
    'monkey',            # Chapter 5: found the wooden monkey -> Chapter 11: the secret holodeck room
    'glasses',           # Chapter 6: wore the glasses -> Chapter 11: the disguise
]
ITEMS = ['amulet', 'suit', 'fragments', 'knife',
         'paper', 'ration', 'chicken', 'shell', 'spikes', 'horn']

# the item check list: every disk gives the player one keepsake that can never be
# lost; every later disk checks the keepsakes of ALL the disks before it.
KEEPSAKES = {1: 'paper', 2: 'ration', 3: 'chicken', 4: 'shell', 5: 'spikes', 6: 'horn'}
KEEP_FROM = {v: k for k, v in KEEPSAKES.items()}
