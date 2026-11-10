parcel(p1).
0.9::cold(p1, s0).
plan_step(p1, leg1, s0).
0.1::warmed(p1, leg1, s0).
plan_step(p1, leg2, do(leg1, s0)).
0.1::warmed(p1, leg2, do(leg1, s0)).
plan_step(p1, leg3, do(leg2, do(leg1, s0))).
0.1::warmed(p1, leg3, do(leg2, do(leg1, s0))).
plan_step(p1, leg4, do(leg3, do(leg2, do(leg1, s0)))).
0.1::warmed(p1, leg4, do(leg3, do(leg2, do(leg1, s0)))).
plan_step(p1, leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))).
0.1::warmed(p1, leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))).
plan_step(p1, leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))).
0.1::warmed(p1, leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))).
plan_step(p1, leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))).
0.1::warmed(p1, leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))).
plan_step(p1, leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))).
0.1::warmed(p1, leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))).
plan_step(p1, leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))).
0.1::warmed(p1, leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))).
plan_step(p1, leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))).
0.1::warmed(p1, leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))).
plan_step(p1, leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))).
0.1::warmed(p1, leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))).
plan_step(p1, leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))).
0.1::warmed(p1, leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))).
plan_step(p1, leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))).
0.1::warmed(p1, leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))).
plan_step(p1, leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))).
0.1::warmed(p1, leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))).
plan_step(p1, leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))).
0.1::warmed(p1, leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))).
plan_step(p1, leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))).
0.1::warmed(p1, leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))).
plan_step(p1, leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))).
0.1::warmed(p1, leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))).
plan_step(p1, leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))).
0.1::warmed(p1, leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))).
plan_step(p1, leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))).
0.1::warmed(p1, leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))).
plan_step(p1, leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))).
0.1::warmed(p1, leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))).
plan_step(p1, leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))).
0.1::warmed(p1, leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))).
plan_step(p1, leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))).
0.1::warmed(p1, leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))).
plan_step(p1, leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))).
0.1::warmed(p1, leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))).
plan_step(p1, leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))).
0.1::warmed(p1, leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))).
plan_step(p1, leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))).
0.1::warmed(p1, leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))).
plan_step(p1, leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))).
0.1::warmed(p1, leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))).
plan_step(p1, leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))).
0.1::warmed(p1, leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))).
plan_step(p1, leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))).
0.1::warmed(p1, leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))).
plan_step(p1, leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))))).
0.1::warmed(p1, leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))))).
plan_step(p1, leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))))).
0.1::warmed(p1, leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))))).
plan_step(p1, leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))))))).
0.1::warmed(p1, leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))))))).
plan_step(p1, leg32, do(leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))))))).
0.1::warmed(p1, leg32, do(leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))))))).
0.95::handover_ok(p1, do(leg32, do(leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0))))))))))))))))))))))))))))))))).
cold(P, do(A, S)) :- cold(P, S), plan_step(P, A, S), \+warmed(P, A, S).
delivered_cold(P, S) :- cold(P, S), handover_ok(P, S).
query(delivered_cold(p1, do(leg32, do(leg31, do(leg30, do(leg29, do(leg28, do(leg27, do(leg26, do(leg25, do(leg24, do(leg23, do(leg22, do(leg21, do(leg20, do(leg19, do(leg18, do(leg17, do(leg16, do(leg15, do(leg14, do(leg13, do(leg12, do(leg11, do(leg10, do(leg9, do(leg8, do(leg7, do(leg6, do(leg5, do(leg4, do(leg3, do(leg2, do(leg1, s0)))))))))))))))))))))))))))))))))).
