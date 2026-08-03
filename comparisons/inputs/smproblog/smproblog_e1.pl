% E1: uncertain equality carrying opposed evidence.  The syntax has no
% classical negation; the opposed literal is the fresh atom np, the
% incompatibility is the odd-loop idiom, and substitution rules cover
% both atoms.  Gate facts keep the probabilistic facts out of rule
% heads, which the system does not support.  The joint world has no
% stable model and its mass goes to the inconsistency column.
0.9::fpa.
0.7::fnpb.
0.8::feq.
p(a) :- fpa.
np(b) :- fnpb.
eq(a,b) :- feq.
eqs(X,Y) :- eq(X,Y).
eqs(Y,X) :- eq(X,Y).
p(Y) :- p(X), eqs(X,Y).
np(Y) :- np(X), eqs(X,Y).
inc :- p(a), np(a), \+ inc.
inc :- p(b), np(b), \+ inc.

query(p(a)).
