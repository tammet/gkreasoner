// first smoking example from 
// Negation Without Negation in Probabilistic Logic Programming
// David Buchman and David Poole
//
// with concrete facts and query given by tanel

/*

0.3 :: smokes(X).
0.1 :: friends(X,Y).
0.9 :: friends(X,Y) :- friends(Y, X).
0.6 :: susceptible(X).
0.2 :: smokes(X) :- susceptible(X), friends(X,Y), smokes(Y).

friends(chris, sam).
smokes(chris).

query(smokes(sam)).

result:  
NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 3:8.
(0.1 :: friends(X,Y). rule)

when we comment out 0.1 :: friends(X,Y) we get
result: 0.3756 


*/

[
{"@confidence": 0.3, "@logic": ["smokes","?:X"]},
{"@confidence": 0.1, "@logic": ["friends","?:X","?:Y"]},
{"@confidence": 0.9, "@logic": [["friends","?:X","?:Y"],"=>",["friends","?:Y","?:X"]]},
{"@confidence": 0.6, "@logic": ["susceptible","?:X"]},
{"@confidence": 0.2, "@logic": 
   [[["smokes","?:Y"],"&",["friends","?:X","?:Y"],"&",["susceptible","?:X"]],"=>",["smokes","?:X"]]},

{"@confidence": 1.0, "@logic": ["friends","chris","sam"]},
{"@confidence": 1.0, "@logic": ["smokes","chris"]},
   
{"@question": ["smokes","sam"]}
]

/*

NB! When we comment out the //{"@confidence": 0.1, "@logic": ["friends","?:X","?:Y"]},
we get the same confidence 0.3756 as problog. 
Down here is a proof for non-outcommented version.

{"result": "proof found",

"answers": [
{
"answer": false,
"confidence": 0.378597,
"positive_proof":
[
[1,      4, ["in", "frm_5", "axiom", 0.2, 0, []], [["-friends","?:X","?:Y"], ["-susceptible","?:X"], ["-smokes","?:Y"], ["smokes","?:X"]]],
[2,      2, ["in", "frm_3", "axiom", 0.9, 0, []], [["-friends","?:X","?:Y"], ["friends","?:Y","?:X"]]],
[3,      5, ["in", "frm_6", "axiom", 1, 0, []], [["friends","chris","sam"]]],
[4,     11, ["mp", 2, 3, "fromaxiom", 0.9, 0, [2,5]], [["friends","sam","chris"]]],
[5,      7, ["in", "frm_8", "goal", 1, 0, []], [["-smokes","sam"]]],
[6,     14, ["mp", 1, 4, 5, "fromgoal", 0.18, 0, [4,2,5]], [["-susceptible","sam"], ["-smokes","chris"]]],
[7,      6, ["in", "frm_7", "axiom", 1, 0, []], [["smokes","chris"]]],
[8,     15, ["simp", 6, 7, "fromgoal", 0.18, 0, [4,2,5,6]], [["-susceptible","sam"]]],
[9,      3, ["in", "frm_4", "axiom", 0.6, 0, []], [["susceptible","?:X"]]],
[10,     16, ["mp", 8, 9, "fromgoal", 0.108, 0, [4,2,5,6,3]], false],
[11,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["smokes","?:X"]]],
[12,      7, ["in", "frm_8", "goal", 1, 0, []], [["-smokes","sam"]]],
[13,      9, ["mp", 11, 12, "fromgoal", 0.3, 0, [0]], false],
[14,     22, ["cumul", 10, 13, "fromgoal", 0.3756, 0, [4,2,5,6,3,0]], false],
[15,      4, ["in", "frm_5", "axiom", 0.2, 0, []], [["-friends","?:X","?:Y"], ["-susceptible","?:X"], ["-smokes","?:Y"], ["smokes","?:X"]]],
[16,      1, ["in", "frm_2", "axiom", 0.1, 0, []], [["friends","?:X","?:Y"]]],
[17,     13, ["mp", 15, 16, "fromaxiom", 0.02, 0, [4,1]], [["-susceptible","?:X"], ["-smokes","?:Y"], ["smokes","?:X"]]],
[18,      3, ["in", "frm_4", "axiom", 0.6, 0, []], [["susceptible","?:X"]]],
[19,     17, ["mp", 17, 18, "fromaxiom", 0.012, 0, [4,1,3]], [["-smokes","?:X"], ["smokes","?:Y"]]],
[20,      6, ["in", "frm_7", "axiom", 1, 0, []], [["smokes","chris"]]],
[21,     19, ["mp", 19, 20, "fromaxiom", 0.012, 0, [4,1,3,6]], [["smokes","?:X"]]],
[22,      7, ["in", "frm_8", "goal", 1, 0, []], [["-smokes","sam"]]],
[23,     21, ["mp", 21, 22, "fromgoal", 0.012, 0, [4,1,3,6]], false],
[24,     26, ["cumul", 14, 23, "fromgoal", 0.378597, 0, [4,2,5,6,3,0,1]], false]



*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study11-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c,c)
Obs3(c)
Obs(c)
Susceptible(c)
Friends(c,c)
Smokes(c)

// -1.02895  Obs(x) => Smokes(x)
-1.02895  Smokes(a1) v !Obs(a1)

// -1.7398  Obs2(x,y) => Friends(x,y)
-1.7398  Friends(a1,a2) v !Obs2(a1,a2)

// 0.343612  Obs3(x) => Susceptible(x)
0.343612  Susceptible(a1) v !Obs3(a1)

// 2.58214  Friends(x,y) => Friends(y,x)
2.58214  Friends(a1,a2) v !Friends(a2,a1)

// 0.0121402  Smokes(x) ^ Friends(x,y) ^ Susceptible(y) => Smokes(y)
0.0121402  Smokes(a1) v !Smokes(a2) v !Friends(a2,a1) v !Susceptible(a1)

// -1.30741  Smokes(a1)
-1.30741  Smokes(a1)

// -2.21796  Friends(a1,a2)
-2.21796  Friends(a1,a2)

// -1.35281  Susceptible(a1)
-1.35281  Susceptible(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1,a2)
0       Obs2(a1,a2)

// 0       Obs3(a1)
0       Obs3(a1)

::::::::::::::
studymln/mln/study11.db
::::::::::::::
Smokes(Chris)
Friends(Chris,Sam)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Smokes(Sam) 0.120038
infer:	Friends(Chris,Chris) 0.0350465
infer:	Friends(Sam,Chris) 0.331017
infer:	Friends(Sam,Sam) 0.0380462
infer:	Susceptible(Chris) 0.19903
infer:	Susceptible(Sam) 0.207029
liftedinfer -ptpe:	Friends(Chris,Chris) 0
liftedinfer -ptpe:	Friends(Sam,Chris) 0
liftedinfer -ptpe:	Friends(Sam,Sam) 0
liftedinfer -ptpe:	Susceptible(Chris) 0
liftedinfer -ptpe:	Susceptible(Sam) 0
liftedinfer -ptpe:	Smokes(Sam) 0
liftedinfer -lvg:	Friends(Chris,Chris) 0.743257
liftedinfer -lvg:	Friends(Sam,Chris) 0.971029
liftedinfer -lvg:	Friends(Sam,Sam) 0.748252
liftedinfer -lvg:	Susceptible(Chris) 0.736264
liftedinfer -lvg:	Susceptible(Sam) 0.722278
liftedinfer -lvg:	Smokes(Sam) 0.856144

*/

