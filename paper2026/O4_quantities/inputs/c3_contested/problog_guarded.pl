0.5::sw_bird_pos.
0.5::sw_bird_neg.
0.9::sw_fly.
bird_pos(a) :- sw_bird_pos.
bird_neg(a) :- sw_bird_neg.
bird_usable(a) :- bird_pos(a), \+bird_neg(a).
flies(a) :- bird_usable(a), sw_fly.
query(flies(a)).
