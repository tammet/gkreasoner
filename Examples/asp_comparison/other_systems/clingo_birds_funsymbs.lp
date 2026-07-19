% Historical function-symbol variant for clingo.
% The positive recursive f(X) rules require infinitely many ground terms. The
% The clingo 5.4.0 run did not finish; clingo 5.6.2 was also still grounding
% when a local reproduction was interrupted after five seconds.

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

bird(f(X)) :- bird(X).
penguin(f(X)) :- penguin(X).

:- flies(b1).
