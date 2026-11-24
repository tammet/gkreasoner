{link(n0,n1)}.
{link(n1,n2)}.
{link(n2,n3)}.
{link(n3,n4)}.
{link(n4,n5)}.
reach(X,Y) :- link(X,Y).
reach(X,Z) :- link(X,Y), reach(Y,Z).
open(X) :- reach(n0,X), not closed(X).
{closed(n5)}.
