% Probabilistic ASP specification; render constraints per solver.
p_pos.
p_neg.
0.6::sw_r.
r :- sw_r.
:- p_pos, p_neg.
query(r).
