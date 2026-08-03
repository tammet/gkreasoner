% F1 crisp counterpart: recursion over a function term. The grounder
% cannot finish on this program.
bird(a).
bird(f(X)) :- bird(X).
