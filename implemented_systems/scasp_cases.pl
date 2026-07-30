% Crisp counterparts for s(CASP); select each query with --query.

d1_neg.
d1_pos :- not d1_neg.

d2_b.
d2_neg_b.
d2_gate.
d2_h :- d2_gate, not d2_b.

d3_b.
d3_neg_b.
d3_gate.
d3_h :- d3_gate, d3_b, not d3_neg_b.

d4_q.
d4_r.
d4_pos :- d4_q, not d4_neg.
d4_neg :- d4_r, not d4_pos.

d5_low.
d5_high.
d5_pos :- d5_low, not d5_high.
d5_neg :- d5_high.

d6_undercut :- not d6_injured.
d6_rebut :- not d6_neg.
