0.5::sw_a.
0.6::sw_e1.
0.7::sw_e2.
a :- sw_a.
e1 :- sw_e1.
e2 :- sw_e2.
b :- a, e1.
c :- a, e2.
q :- b.
q :- c.
query(q).
