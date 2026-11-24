0.5::sw_bird_evidence.
0.9::sw_fly.
bird_pos(a) :- sw_bird_evidence.
bird_neg(a) :- sw_bird_evidence.
bird_usable(a) :- bird_pos(a), \+bird_neg(a).
flies(a) :- bird_usable(a), sw_fly.
query(flies(a)).
