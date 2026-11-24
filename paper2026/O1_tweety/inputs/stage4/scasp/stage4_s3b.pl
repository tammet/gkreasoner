% Stage 4 on stage 3b, crisp counterpart: as stage4_s2.pl, with the certain gull rule and the yellow bill.
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
-gull(tweety).
gull(X) :- seabird(X), yellow_bill(X).
yellow_bill(tweety).
