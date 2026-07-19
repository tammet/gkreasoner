% Historical function-symbol variant for s(CASP) 0.21.10.09. The recorded run did
% not finish. This is an observation about this program and version, not a
% general claim that s(CASP) cannot use function symbols.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

bird(f(X)) :- bird(X).
penguin(f(X)) :- penguin(X).

?- flies(b1).
