/*
(1) 0.3 : smokes(X)
(2) 0.1 : friends(X, Y )
(3) 0.9 : friends(X, Y ) ← friends(Y, X)
(4) 0.6 : susceptible(X)
(5) 0.2 : smokes(X) ← susceptible(X)
                      ∧ friends(X, Y ) ∧ smokes(Y )
(6)
friends(chris, sam)

problog fails to understand:

from

Negation Without Negation in Probabilistic Logic Programming
David Buchman and David Poole

0.3 : smokes(X).
0.1 : friends(X, Y ).
0.9 : friends(X, Y ) :- friends(Y, X).
0.6 : susceptible(X)
0.2 : smokes(X) :- susceptible(X), friends(X,Y), smokes(Y).
friends(chris, sam).
smokes(chris).
query(smokes(sam)).

*/
[
{"@confidence": 0.3, "@logic": ["smokes","?:X"]},
{"@confidence": 0.1, "@logic": ["friends","?:X","?:Y"]},
{"@confidence": 0.9, "@logic": [["friends","?:X","?:Y"],"=>",["friends","?:Y","?:X"]]},
{"@confidence": 0.6, "@logic": ["susceptible","?:X"]},
{"@confidence": 0.2, "@logic": [[["susceptible","?:X"],"&",["friends","?:X","?:Y"],"&",["smokes","?:Y"]],"=>",["smokes","?:X"]]},
{"@confidence": 100, "@logic": ["friends","chris","sam"]},
{"@confidence": 100, "@logic": ["smokes","chris"]},
{"@question": ["smokes","sam"]}
]