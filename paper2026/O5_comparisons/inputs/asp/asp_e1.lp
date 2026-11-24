% E1 crisp counterpart: equality carrying opposed evidence, with
% substitution rules for both polarities of the one predicate.
p(a).
-p(b).
eq(a,b).
eq(b,a) :- eq(a,b).
p(Y) :- p(X), eq(X,Y).
-p(Y) :- -p(X), eq(X,Y).
