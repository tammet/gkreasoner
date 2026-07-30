% Additional table analogues for plingo 1.1.0, ProbLog front end.

c1_a :- &problog("0.5").
c1_b :- &problog("0.6").
c1_q :- c1_a.
c1_q :- c1_b.

c2_a :- &problog("0.5").
c2_b :- &problog("0.6").
c2_q :- c2_a, c2_b.

d1_neg :- &problog("0.9").
d1_pos :- not d1_neg.

d2_b :- &problog("0.7").
d2_neg_b :- &problog("0.3").
d2_gate :- &problog("0.9").
d2_h :- d2_gate, not d2_b.

d3_b :- &problog("0.5").
d3_neg_b :- &problog("0.5").
d3_gate :- &problog("0.9").
d3_h :- d3_gate, d3_b, not d3_neg_b.

d4_q.
d4_r.
d4_pos :- d4_q, not d4_neg.
d4_neg :- d4_r, not d4_pos.

d5_low :- &problog("0.9").
d5_high :- &problog("0.3").
d5_pos :- d5_low, not d5_high.
d5_neg :- d5_high.

d6_undercut :- not d6_injured.
d6_rebut :- not d6_neg.

d7_p :- &problog("0.6").
d7_pos_gate :- &problog("0.9").
d7_neg_gate :- &problog("0.8").
d7_pos :- d7_pos_gate, not d7_p.
d7_neg :- d7_p, d7_neg_gate.
d7_pos :- d7_p, not d7_neg_gate.

&query(c1_q).
&query(c2_q).
&query(d1_pos).
&query(d1_neg).
&query(d2_h).
&query(d3_h).
&query(d4_pos).
&query(d4_neg).
&query(d5_pos).
&query(d5_neg).
&query(d6_undercut).
&query(d6_rebut).
&query(d7_pos).
&query(d7_neg).
