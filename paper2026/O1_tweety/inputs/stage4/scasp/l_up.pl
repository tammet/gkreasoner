% The lineage with the rule towards the parent only.
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
