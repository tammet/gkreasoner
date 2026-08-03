% E1: uncertain equality carrying opposed evidence.  The equality is a
% probabilistic fact; substitution rules cover both polarities of the
% one predicate of the row.  The joint world derives p(b) and -p(b)
% and has no stable model; plingo renormalizes over the others.
p(a) :- &problog("0.9").
-p(b) :- &problog("0.7").
eq(a,b) :- &problog("0.8").
eq(b,a) :- eq(a,b).
p(Y) :- p(X), eq(X,Y).
-p(Y) :- -p(X), eq(X,Y).

&query(p(a)).
