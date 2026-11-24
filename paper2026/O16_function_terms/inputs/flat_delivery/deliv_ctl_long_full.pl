0.9::cold(p1, s0).
parcel(p1).
plan_step(p1, short_leg, s0).
plan_step(p1, sheltered_leg1, s0).
plan_step(p1, sheltered_leg2, do(sheltered_leg1, s0)).
0.3::warmed(p1, short_leg, s0).
0.1::warmed(p1, sheltered_leg1, s0).
0.1::warmed(p1, sheltered_leg2, do(sheltered_leg1, s0)).
0.95::handover_ok(p1, do(short_leg, s0)).
0.95::handover_ok(p1, do(sheltered_leg2, do(sheltered_leg1, s0))).
cold(P, do(A, S)) :- cold(P, S), plan_step(P, A, S), \+warmed(P, A, S).
delivered_cold(P, S) :- cold(P, S), handover_ok(P, S).
query(delivered_cold(p1, do(sheltered_leg2, do(sheltered_leg1, s0)))).
