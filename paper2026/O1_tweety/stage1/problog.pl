% Tweety, stage 1: the ProbLog encoding, an exact translation for this input only (Section 2.1).
bird(tweety).
0.9::flies(X) :- bird(X), \+ penguin(X).
0.8::seabird(tweety).
0.7::penguin(X) :- seabird(X).
query(flies(tweety)).
