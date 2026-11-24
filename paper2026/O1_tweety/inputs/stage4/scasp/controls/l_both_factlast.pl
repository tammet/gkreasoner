% Control: l_both.pl with the register entry written after the two lineage rules.
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
bird(parent(parent(tweety))).
