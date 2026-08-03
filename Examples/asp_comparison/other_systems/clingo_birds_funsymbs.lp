% Function-symbol variant for clingo.
% The positive recursive f(X) rules require infinitely many ground terms,
% so grounding does not finish.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

bird(f(X)) :- bird(X).
penguin(f(X)) :- penguin(X).

:- flies(b1).
