bird(tweety).
0.9::sw_fly(tweety).
0.8::seabird(tweety).
0.7::sw_penguin(tweety).
penguin(X) :- seabird(X), sw_penguin(X).
flies(X) :- bird(X), sw_fly(X), not penguin(X).
nflies(X) :- penguin(X).
