// second smoking example from 
// Negation Without Negation in Probabilistic Logic Programming
// David Buchman and David Poole
//
// with concrete facts and query given by tanel

/*

0.3 :: smokes(X).
0.1 :: friends(X,Y).
0.9 :: friends(X,Y) :- friends(Y, X).
0.6 :: nonconformist(X).
0.2 :: smokes(X) :- nonconformist(X), friends(X,Y), not smokes(Y).

friends(chris, sam).
smokes(chris).

query(smokes(sam)).

result: 
NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 2:8. 


*/

[
{"@confidence": 0.3, "@logic": ["smokes","?:X"]},
{"@confidence": 0.1, "@logic": ["friends","?:X","?:Y"]},
{"@confidence": 0.9, "@logic": [["friends","?:X","?:Y"],"=>",["friends","?:Y","?:X"]]},
{"@confidence": 0.6, "@logic": ["nonconformist","?:X"]},
{"@confidence": 0.2, "@logic": 
   [[["-smokes","?:Y"],"&",["friends","?:X","?:Y"],"&",["nonconformist","?:X"]],"=>",["smokes","?:X"]]},

{"@confidence": 1.0, "@logic": ["friends","chris","sam"]},
{"@confidence": 1.0, "@logic": ["smokes","chris"]},
   
{"@question": ["smokes","sam"]}
]

/*

{"result": "proof found",

"answers": [
{
"answer": false,
"confidence": 0.3084,
"positive_proof":
[
[1,      4, ["in", "frm_5", "axiom", 0.2, 0, []], [["-friends","?:X","?:Y"], ["-nonconformist","?:X"], ["smokes","?:Y"], ["smokes","?:X"]]],
[2,      1, ["in", "frm_2", "axiom", 0.1, 0, []], [["friends","?:X","?:Y"]]],
[3,     14, ["mp", 1, 2, "fromaxiom", 0.02, 0, [4,1]], [["-nonconformist","?:X"], ["smokes","?:Y"], ["smokes","?:X"]]],
[4,      3, ["in", "frm_4", "axiom", 0.6, 0, []], [["nonconformist","?:X"]]],
[5,     20, ["mp", 3, 4, "fromaxiom", 0.012, 0, [4,1,3]], [["smokes","?:X"], ["smokes","?:Y"]]],
[6,     21, ["merge", [5,0,1], "fromaxiom", 0.012, 0, [4,1,3]], [["smokes","?:X"]]],
[7,      7, ["in", "frm_8", "goal", 1, 0, []], [["-smokes","sam"]]],
[8,     23, ["mp", 6, 7, "fromgoal", 0.012, 0, [4,1,3]], false],
[9,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["smokes","?:X"]]],
[10,      7, ["in", "frm_8", "goal", 1, 0, []], [["-smokes","sam"]]],
[11,      9, ["mp", 9, 10, "fromgoal", 0.3, 0, [0]], false],
[12,     26, ["cumul", 8, 11, "fromgoal", 0.3084, 0, [4,1,3,0]], false]


*/

/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study12-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c,c)
Obs3(c)
Nonconformist(c)
Obs(c)
Friends(c,c)
Smokes(c)

// -1.02687  Obs(x) => Smokes(x)
-1.02687  Smokes(a1) v !Obs(a1)

// -1.73629  Obs2(x,y) => Friends(x,y)
-1.73629  Friends(a1,a2) v !Obs2(a1,a2)

// 0.342918  Obs3(x) => Nonconformist(x)
0.342918  Nonconformist(a1) v !Obs3(a1)

// 2.57692  Friends(x,y) => Friends(y,x)
2.57692  Friends(a1,a2) v !Friends(a2,a1)

// 0.00310434  !Smokes(x) ^ Friends(x,y) ^ Nonconformist(y) => Smokes(y)
0.00310434  Smokes(a1) v Smokes(a2) v !Friends(a2,a1) v !Nonconformist(a1)

// -1.83038  Smokes(a1)
-1.83038  Smokes(a1)

// -2.21347  Friends(a1,a2)
-2.21347  Friends(a1,a2)

// -1.35008  Nonconformist(a1)
-1.35008  Nonconformist(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1,a2)
0       Obs2(a1,a2)

// 0       Obs3(a1)
0       Obs3(a1)

::::::::::::::
studymln/mln/study12.db
::::::::::::::
Smokes(Chris)
Friends(Chris,Sam)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Smokes(Sam) 0.0690431
infer:	Friends(Chris,Chris) 0.0240476
infer:	Friends(Sam,Chris) 0.344016
infer:	Friends(Sam,Sam) 0.0330467
infer:	Nonconformist(Chris) 0.19803
infer:	Nonconformist(Sam) 0.249025
liftedinfer -ptpe:	Friends(Chris,Chris) 0
liftedinfer -ptpe:	Friends(Sam,Chris) 0
liftedinfer -ptpe:	Friends(Sam,Sam) 0
liftedinfer -ptpe:	Nonconformist(Chris) 0
liftedinfer -ptpe:	Nonconformist(Sam) 0
liftedinfer -ptpe:	Smokes(Sam) 0
liftedinfer -lvg:	Friends(Chris,Chris) 0.719281
liftedinfer -lvg:	Friends(Sam,Chris) 0.993007
liftedinfer -lvg:	Friends(Sam,Sam) 0.752248
liftedinfer -lvg:	Nonconformist(Chris) 0.777223
liftedinfer -lvg:	Nonconformist(Sam) 0.732268
liftedinfer -lvg:	Smokes(Sam) 0.737263

*/

