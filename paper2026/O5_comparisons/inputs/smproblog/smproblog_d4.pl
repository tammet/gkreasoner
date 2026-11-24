% Deterministic Nixon diamond, isolated because the smProbLog compiler handles
% this negative cycle separately from the stratified probabilistic cases.
1.0::d4_q.
1.0::d4_r.
d4_pos :- d4_q, \+ d4_neg.
d4_neg :- d4_r, \+ d4_pos.

query(d4_pos).
query(d4_neg).
