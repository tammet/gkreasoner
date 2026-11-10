0.9::sw_pos.
0.8::sw_neg.
p_neg :- sw_neg.
p_pos :- sw_pos, \+p_neg.
query(p_pos).
