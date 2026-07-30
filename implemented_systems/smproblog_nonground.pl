0.5::n1_bird(a).
0.6::n1_bird(b).
n1_twobirds(X,Y) :- n1_bird(X), n1_bird(Y).

0.8::n2_stress(ann).
0.4::n2_stress(bob).
0.6::n2_influences(ann,bob).
0.2::n2_influences(bob,carl).
n2_smokes(X) :- n2_stress(X).
n2_smokes(X) :- n2_influences(Y,X), n2_smokes(Y).

query(n1_twobirds(X,Y)).
query(n2_smokes(X)).
