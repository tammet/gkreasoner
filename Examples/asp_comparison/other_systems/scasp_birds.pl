% Historical basic-birds input for s(CASP) 0.21.10.09. The query is last.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

?- flies(b1).
