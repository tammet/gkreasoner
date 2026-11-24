bird(t).
0.7::sw_injury.
0.9::sw_fly.
injured(t) :- sw_injury.
flies(t) :- bird(t), sw_fly, \+injured(t).
query(flies(t)).
