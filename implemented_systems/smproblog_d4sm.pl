0.8::quaker.
0.6::republican.

pacifist :- quaker, \+ nonpacifist.
nonpacifist :- republican, \+ pacifist.

query(pacifist).
query(nonpacifist).
