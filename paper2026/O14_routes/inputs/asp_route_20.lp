{link(n0,n1)}.
{link(n1,n2)}.
{link(n2,n3)}.
{link(n3,n4)}.
{link(n4,n5)}.
{link(n5,n6)}.
{link(n6,n7)}.
{link(n7,n8)}.
{link(n8,n9)}.
{link(n9,n10)}.
{link(n10,n11)}.
{link(n11,n12)}.
{link(n12,n13)}.
{link(n13,n14)}.
{link(n14,n15)}.
{link(n15,n16)}.
{link(n16,n17)}.
{link(n17,n18)}.
{link(n18,n19)}.
{link(n19,n20)}.
reach(X,Y) :- link(X,Y).
reach(X,Z) :- link(X,Y), reach(Y,Z).
open(X) :- reach(n0,X), not closed(X).
{closed(n20)}.
