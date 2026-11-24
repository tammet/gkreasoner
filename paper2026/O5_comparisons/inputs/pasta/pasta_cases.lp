% Additional table analogues for PASTA 1.0.1.

0.5::c1_a.
0.6::c1_b.
c1_q :- c1_a.
c1_q :- c1_b.

0.5::c2_a.
0.6::c2_b.
c2_q :- c2_a, c2_b.

0.9::d1_neg.
d1_pos :- not d1_neg.

0.7::d2_b.
0.3::d2_neg_b.
0.9::d2_gate.
d2_h :- d2_gate, not d2_b.

0.5::d3_b.
0.5::d3_neg_b.
0.9::d3_gate.
d3_h :- d3_gate, d3_b, not d3_neg_b.

d4_q.
d4_r.
d4_pos :- d4_q, not d4_neg.
d4_neg :- d4_r, not d4_pos.

0.9::d5_low.
0.3::d5_high.
d5_pos :- d5_low, not d5_high.
d5_neg :- d5_high.

d6_undercut :- not d6_injured.
d6_rebut :- not d6_neg.

0.6::d7_p.
0.9::d7_pos_gate.
0.8::d7_neg_gate.
d7_pos :- d7_pos_gate, not d7_p.
d7_neg :- d7_p, d7_neg_gate.
d7_pos :- d7_p, not d7_neg_gate.
