% F1 crisp counterpart: recursion over a function term. Top-down
% execution needs no grounding.
bird(a).
bird(f(X)) :- bird(X).
