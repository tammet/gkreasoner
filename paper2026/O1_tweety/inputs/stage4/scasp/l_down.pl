% The lineage with the rule towards the child only.
bird(parent(parent(tweety))).
bird(X) :- bird(parent(X)).
