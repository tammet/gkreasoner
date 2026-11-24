% Stage 4 on the disjunction stage, crisp counterpart: the lineage in place of bird(tweety);
% the disjunction as two rules with negation as failure; the report against gull as a classical negative fact.
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
-gull(tweety).
