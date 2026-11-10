0.5::sw_p.
0.5::sw_b.
p(a) :- sw_p, \+b(a).
b(a) :- sw_b, \+p(a).
query(p(a)).
