STORY = (['frag1', 'frag2', 'frag3', 'frag4', 'frag5', 'frag6', 'frag7', 'frag8', 'frag9', 'edmund_freed',
          'napkin_given', 'kicked_chicken', 'untied_crewman', 'said_grandmother', 'monkey', 'glasses'],
         ['fragments', 'paper', 'ration', 'chicken', 'shell'])
WALK = [
    ('expect', 'room:ledge'), ('pickup', 'snow'), ('expect', 'snowball'),
    ('walk', 'lg_cave'), ('look', 'junk'), ('expect', 'flag:frag10'), ('pickup', 'spikes_o'), ('expect', 'spikes'),
    ('walk', 'ic_out'), ('walk', 'lg_east'), ('walk', 'bridge'), ('expect', 'room:icebridge'), ('use', 'spikes'),
    ('walk', 'bridge'), ('expect', 'room:camp'), ('walk', 'cp_tent'), ('expect', 'room:camp'),
    ('use', 'snowball', 'soldiers_c'), ('expect', 'flag:distracted'), ('walk', 'cp_tent'), ('expect', 'room:tent'),
    ('pickup', 'amulet_o'), ('expect', 'amulet'), ('walk', 'tn_out'), ('walk', 'cp_steps'), ('expect', 'room:steps'),
    ('walk', 'stairs_t'), ('expect', 'room:tgate'), ('use', 'amulet', 'tgate_g'), ('walk', 'tgate_g'),
    ('expect', 'room:statues'), ('look', 'statues_l'), ('expect', 'flag:frag11'), ('pickup', 'mirror_o'),
    ('pickup', 'dust'), ('expect', 'stardust'), ('walk', 'st_east'), ('use', 'mirror', 'stand'), ('walk', 'eyedoor'),
    ('expect', 'room:starbridge'), ('use', 'stardust', 'void'), ('walk', 'void'), ('expect', 'room:heartdoor'),
    ('use', 'amulet', 'heartdoor_d'), ('expect', 'end'),
]
