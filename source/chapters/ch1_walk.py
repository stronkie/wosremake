WALK = [
    # Part 1: the grounds
    ('walk', 'gate'), ('expect', 'room:garden'),
    ('walk', 'shed_g'), ('pickup', 'tools'), ('expect', 'fragments'), ('expect', 'flag:frag1'),
    ('pickup', 'shovel_o'), ('expect', 'shovel'), ('walk', 'shed_out'),
    ('use', 'shovel', 'mound'), ('expect', 'flag:dug'), ('pickup', 'handle_o'), ('expect', 'crank'),
    ('walk', 'well_g'), ('use', 'crank', 'winch'), ('pickup', 'wkey'), ('expect', 'brasskey'),
    ('walk', 'well_out'), ('walk', 'porch_g'), ('pickup', 'mat'), ('expect', 'paper'),
    ('open', 'door'), ('expect', 'flag:door_open'), ('walk', 'door'), ('expect', 'room:hall'),
    # Part 2: the manor
    ('walk', 'east_door'), ('pickup', 'candle_o'), ('pickup', 'matches_o'), ('pickup', 'knife_o'),
    ('use', 'matches', 'candle'), ('expect', 'litcandle'),
    ('walk', 'steps_k'), ('expect', 'room:cellar'), ('pickup', 'barrels_l'), ('expect', 'flag:frag2'),
    ('pickup', 'skey_o'), ('expect', 'silverkey'), ('walk', 'cellar_up'), ('walk', 'kit_out'),
    ('use', 'silverkey', 'small_door'), ('walk', 'small_door'), ('expect', 'room:study'),
    ('look', 'diary'), ('walk', 'study_out'), ('walk', 'west_door'), ('pull', 'redbook'),
    ('walk', 'passage'), ('expect', 'room:secret'), ('use', 'knife', 'ropes'),
    ('expect', 'room:stairs'), ('expect', 'amulet'),
    # Part 3: the launch pad
    ('pickup', 'steps'), ('expect', 'flag:frag3'), ('walk', 'stairs_down'),
    ('walk', 'to_lockers'), ('open', 'pilot_locker'), ('expect', 'suit'), ('expect', 'keycard'),
    ('use', 'suit'), ('expect', 'flag:suit_worn'), ('walk', 'lockers_out'),
    ('use', 'keycard', 'cardslot'), ('walk', 'blast'), ('expect', 'room:hangar'),
    ('walk', 'to_control'), ('talk', 'edmund_c', ['What do I do']),
    ('use', 'amulet', 'slot_c'), ('pull', 'lever'), ('expect', 'flag:hatch_open'),
    ('walk', 'control_out'), ('walk', 'ship'), ('expect', 'room:shipin'),
    ('push', 'launch'), ('expect', 'end'),
]
