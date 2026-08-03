% E1: uncertain equality carrying opposed evidence.  The opposed
% literal -p(b) is not statable in ProbLog.  This best-effort
% simulation keeps it as the fresh atom np and adds hand-written
% substitution rules for both atoms; the output stays two disconnected
% numbers (p(a) 0.9, np(a) 0.56) with no combined verdict, so the E1
% ProbLog cell claims no faithful encoding.
0.9::p(a).
0.7::np(b).
0.8::eq(a,b).
eqs(X,Y) :- eq(X,Y).
eqs(Y,X) :- eq(X,Y).
p(Y) :- p(X), eqs(X,Y).
np(Y) :- np(X), eqs(X,Y).

query(p(a)).
query(np(a)).
