% Stage 4, one lineage rule: a ProbLog analogue of gk_child_rule.gkp with a positive gull switch.
bird(X) :- bird(parent(X)).
bird(parent(parent(tweety))).
0.9::flies(X) :- bird(X), \+ penguin(X).
penguin(X) :- seabird(X), \+ gull(X).
0.8::seabird(tweety).
0.3::gull(tweety).
query(flies(tweety)).
