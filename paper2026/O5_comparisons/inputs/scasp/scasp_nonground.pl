n1_bird(a).
n1_bird(b).
n1_twobirds(X,Y) :- n1_bird(X), n1_bird(Y).

n2_stress(ann).
n2_stress(bob).
n2_influences(ann,bob).
n2_influences(bob,carl).
n2_smokes(X) :- n2_stress(X).
n2_smokes(X) :- n2_influences(Y,X), n2_smokes(Y).
