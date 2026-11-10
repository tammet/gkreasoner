bird(tweety).
0.9::sw_fly(tweety).
0.8::seabird(tweety).
0.7::ngull_ev(tweety).
gull(X) :- seabird(X), \+penguin(X).
penguin(X) :- seabird(X), \+gull(X).
inconsistent(X) :- gull(X), ngull_ev(X), \+inconsistent(X).
flies(X) :- bird(X), sw_fly(X), \+penguin(X).
nflies(X) :- penguin(X).
query(flies(tweety)).
query(nflies(tweety)).
