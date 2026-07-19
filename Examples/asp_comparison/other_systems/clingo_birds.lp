% Retained historical clingo query test.
% The final constraint rejects every model in which flies(b1) holds. Therefore
% UNSATISFIABLE is the successful result: no counterexample model exists.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

:- flies(b1).
