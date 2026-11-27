"""The story that goes from one chapter of World of Stronkie remake to the next
(like the original World of Stronkie): the story flags and the story items.
A chapter maps these names to its own flags and things with the same names; the
story file has room for 128 of each, numbered in the order below.
Never reorder these lists, only add to the end."""
FLAGS = [f'frag{n}' for n in range(1, 17)] + [   # the 16 star fragments of the true ending
    'edmund_freed',      # Prologue: freed Uncle Edmund
]
ITEMS = ['amulet', 'suit', 'fragments', 'knife']
