# none of the choices on the disks before, and not all fragments: the other way round, the normal ending
STORY = (['frag1', 'frag2', 'edmund_freed'], ['amulet', 'fragments', 'paper', 'ration', 'chicken', 'shell', 'spikes', 'horn'])
WALK = [
    ('expect', 'room:fhangar'), ('walk', 'mdoor'), ('expect', 'room:fhangar'),
    ('walk', 'fh_east'), ('walk', 'fc_break'), ('talk', 'bguards', []), ('push', 'barcade'), ('expect', 'badge'),
    ('look', 'bposter'), ('walk', 'bk_out'), ('walk', 'fc_laundry'), ('pickup', 'uniform_o'), ('talk', 'lrobot_t', []),
    ('walk', 'ld_out'), ('use', 'badge', 'cguard_t'), ('expect', 'room:fcorr'), ('use', 'uniform'),
    ('use', 'badge', 'cguard_t'), ('walk', 'fc_lift'), ('expect', 'room:lift'),
    ('talk', 'tron_t', ['Then you must have been looking in a mirror.',
                        'Maybe, but your jokes still load from a datasette.',
                        'At least I\'d be useful then, unlike you.']),
    ('walk', 'liftdoor'), ('expect', 'room:plift'), ('talk', 'roger_t', []), ('pickup', 'bucket_o'), ('expect', 'bucket'),
    ('walk', 'pl_guard'), ('use', 'bucket', 'gguard_t'), ('pickup', 'kc_o'), ('expect', 'keycard'),
    ('walk', 'gdoor'), ('pull', 'plever'), ('walk', 'pc_out'), ('walk', 'gr_out'),
    ('walk', 'pl_cells'), ('talk', 'edmund_t', []), ('walk', 'cb_out'), ('walk', 'pl_lift'), ('expect', 'room:fbridge'),
    ('walk', 'fb_cannon'), ('expect', 'room:fbridge'), ('walk', 'fb_radio'),
    ('talk', 'radio', ['LeChuckle! Look behind you, a three-headed monkey!']), ('expect', 'flag:pirates_gone'),
    ('walk', 'cm_out'), ('walk', 'fb_pods'), ('open', 'toolbox'), ('expect', 'spanner'), ('walk', 'pb_up'),
    ('walk', 'fb_cannon'), ('expect', 'room:cannon'), ('use', 'spanner', 'ccontrols'), ('walk', 'cn_out'),
    ('walk', 'fb_vex'), ('pickup', 'photo_o'), ('walk', 'vx_out'), ('use', 'photo', 'vex_b'), ('expect', 'room:egarden'),
    ('walk', 'eg_manor'), ('walk', 'eh_study'), ('use', 'fragments', 'globe'), ('expect', 'end'),
]
