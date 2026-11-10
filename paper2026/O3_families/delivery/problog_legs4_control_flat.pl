parcel(p1).
0.9::cold(p1, s0).
plan_step(p1, leg1, s0).
succ(s0, leg1, s1).
0.1::warmed(p1, leg1, s0).
plan_step(p1, leg2, s1).
succ(s1, leg2, s2).
0.1::warmed(p1, leg2, s1).
plan_step(p1, leg3, s2).
succ(s2, leg3, s3).
0.1::warmed(p1, leg3, s2).
plan_step(p1, leg4, s3).
succ(s3, leg4, s4).
0.1::warmed(p1, leg4, s3).
0.95::handover_ok(p1, s4).
cold(P, S2) :- cold(P, S), plan_step(P, A, S), succ(S, A, S2), \+warmed(P, A, S).
delivered_cold(P, S) :- cold(P, S), handover_ok(P, S).
query(delivered_cold(p1, s4)).
