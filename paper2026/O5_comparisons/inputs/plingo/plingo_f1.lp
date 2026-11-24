% F1: recursion over a function term. The grounder cannot finish on
% this program, so the rule weight never comes into play; it is left
% out rather than approximated.
bird(a) :- &problog("0.9").
bird(f(X)) :- bird(X).

&query(bird(f(f(a)))).
