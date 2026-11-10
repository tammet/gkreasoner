% Tweety, stage 4: a ProbLog analogue with the positive switch 0.3::gull(tweety). It tests
% grounding with both lineage rules; it is no matched numerical comparison.
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
bird(parent(parent(tweety))).
0.9::flies(X) :- bird(X), \+ penguin(X).
penguin(X) :- seabird(X), \+ gull(X).
0.8::seabird(tweety).
0.3::gull(tweety).
query(flies(tweety)).
