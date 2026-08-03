% E1: uncertain equality carrying opposed evidence.  The equality is a
% probabilistic fact; substitution rules cover both polarities of the
% one predicate of the row.  The joint world derives p(b) and -p(b)
% and has no answer set.
0.9::fpa.
0.7::fnpb.
0.8::feq.
p(a) :- fpa.
-p(b) :- fnpb.
eq(a,b) :- feq.
eq(b,a) :- eq(a,b).
p(Y) :- p(X), eq(X,Y).
-p(Y) :- -p(X), eq(X,Y).
