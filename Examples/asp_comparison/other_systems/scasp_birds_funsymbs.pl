% Function-symbol variant for s(CASP). The recorded run on this program did
% not finish; the observation concerns this program, without a general claim
% about s(CASP) and function symbols.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

bird(f(X)) :- bird(X).
penguin(f(X)) :- penguin(X).

?- flies(b1).
