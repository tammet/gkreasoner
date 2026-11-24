% Control: clingo_skeleton_scasp.pl with the register entry written before the two lineage rules (the order of l_both.pl).
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
