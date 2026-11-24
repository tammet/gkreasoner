0.9::link(n0,n1).
0.9::link(n1,n2).
0.9::link(n2,n3).
0.9::link(n3,n4).
0.9::link(n4,n5).
0.9::link(n5,n6).
0.9::link(n6,n7).
0.9::link(n7,n8).
0.9::link(n8,n9).
0.9::link(n9,n10).
0.9::link(n10,n11).
0.9::link(n11,n12).
0.9::link(n12,n13).
0.9::link(n13,n14).
0.9::link(n14,n15).
0.9::link(n15,n16).
0.9::link(n16,n17).
0.9::link(n17,n18).
0.9::link(n18,n19).
0.9::link(n19,n20).
reach(X,Y) :- link(X,Y).
reach(X,Z) :- link(X,Y), reach(Y,Z).
0.8::open(X) :- reach(n0,X), \+ closed(X).
0.5::closed(n20).
query(open(n20)).
