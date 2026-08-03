% F1: probabilistic recursion over a function term. The rule weight
% would need a per-instance probabilistic gate over an infinite
% Herbrand universe; the grounder cannot finish on this program.
0.9::bird(a).
bird(f(X)) :- bird(X).
