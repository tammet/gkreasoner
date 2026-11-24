% Control: stage4_s2.pl with bird(tweety) as a fact in place of the register entry and the two lineage rules.
bird(tweety).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
-gull(tweety).
