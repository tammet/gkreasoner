% Additional table analogues for smProbLog 2.1.0.42.

0.5::c1_a.
0.6::c1_b.
c1_q :- c1_a.
c1_q :- c1_b.

0.5::c2_a.
0.6::c2_b.
c2_q :- c2_a, c2_b.

0.9::d1_neg.
d1_pos :- \+ d1_neg.

0.7::d2_b.
0.3::d2_neg_b.
0.9::d2_gate.
d2_h :- d2_gate, \+ d2_b.

0.5::d3_b.
0.5::d3_neg_b.
0.9::d3_gate.
d3_h :- d3_gate, d3_b, \+ d3_neg_b.

0.9::d5_low.
0.3::d5_high.
d5_pos :- d5_low, \+ d5_high.
d5_neg :- d5_high.

0.0::d6_injured.
0.0::d6_neg.
d6_undercut :- \+ d6_injured.
d6_rebut :- \+ d6_neg.

0.6::d7_p.
0.9::d7_pos_gate.
0.8::d7_neg_gate.
d7_pos :- d7_pos_gate, \+ d7_p.
d7_neg :- d7_p, d7_neg_gate.
d7_pos :- d7_p, \+ d7_neg_gate.

query(c1_q).
query(c2_q).
query(d1_pos).
query(d1_neg).
query(d2_h).
query(d3_h).
query(d5_pos).
query(d5_neg).
query(d6_undercut).
query(d6_rebut).
query(d7_pos).
query(d7_neg).
