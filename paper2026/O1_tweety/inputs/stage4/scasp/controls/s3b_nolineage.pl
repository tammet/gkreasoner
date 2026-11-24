% Control: stage4_s3b.pl with bird(tweety) as a fact in place of the register entry and the two lineage rules.
bird(tweety).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
-gull(tweety).
gull(X) :- seabird(X), yellow_bill(X).
yellow_bill(tweety).
