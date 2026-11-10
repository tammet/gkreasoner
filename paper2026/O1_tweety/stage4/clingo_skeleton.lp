% Tweety, stage 4: the certain skeleton of gk_stage2.gkp for a grounding test with clingo.
% Both lineage rules make the ground program infinite.
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
bird(parent(parent(tweety))).
flies(X) :- bird(X), not penguin(X).
gull(X) | penguin(X) :- seabird(X).
seabird(tweety).
