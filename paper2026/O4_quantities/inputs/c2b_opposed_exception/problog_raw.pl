bird(t).
0.7::sw_injury_pos.
0.3::sw_injury_neg.
0.9::sw_fly.
injured_pos(t) :- sw_injury_pos.
injured_neg(t) :- sw_injury_neg.
flies(t) :- bird(t), sw_fly, \+injured_pos(t).
query(flies(t)).
