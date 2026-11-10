0.5::sw_bird_pos.
0.5::sw_bird_neg.
0.9::sw_fly.
bird_pos(a) :- sw_bird_pos.
bird_neg(a) :- sw_bird_neg.
flies(a) :- bird_pos(a), sw_fly.
query(flies(a)).
