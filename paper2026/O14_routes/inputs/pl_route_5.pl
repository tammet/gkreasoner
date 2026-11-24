0.99::link(n0,n1).
0.99::link(n1,n2).
0.99::link(n2,n3).
0.99::link(n3,n4).
0.99::link(n4,n5).
0.99::reach(X,Y) :- link(X,Y).
0.99::reach(X,Z) :- link(X,Y), reach(Y,Z).
0.8::open(X) :- reach(n0,X), \+ closed(X).
0.5::closed(n5).
query(open(n5)).
