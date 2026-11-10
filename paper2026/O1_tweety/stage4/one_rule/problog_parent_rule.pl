% Stage 4, one lineage rule: a ProbLog analogue of gk_parent_rule.gkp with a positive gull switch.
bird(tweety).
bird(parent(X)) :- bird(X).
0.9::flies(X) :- bird(X), \+ penguin(X).
penguin(X) :- seabird(X), \+ gull(X).
0.8::seabird(parent(tweety)).
0.3::gull(parent(tweety)).
query(flies(parent(tweety))).
