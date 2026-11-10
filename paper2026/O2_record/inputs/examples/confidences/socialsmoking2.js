// like smoking social network example 1, but stress(bob) added:
// slightly different cumulative effect

/*

0.8::stress(ann).
0.4::stress(bob).
0.6::influences(ann,bob).
0.2::influences(bob,carl).

smokes(X) :- stress(X).
smokes(X) :- influences(Y,X), smokes(Y).

query(smokes(carl)).

result:  0.1376

*/

[
{"@confidence": 0.8, "@logic": ["stress","ann"]},
{"@confidence": 0.4, "@logic": ["stress","bob"]},
{"@confidence": 0.6, "@logic": ["influences","ann","bob"]},
{"@confidence": 0.2, "@logic": ["influences","bob","carl"]},
{"@confidence": 1.0, "@logic": [["stress","?:X"],"=>",["smokes","?:X"]]},
{"@confidence": 1.0, "@logic": [[["smokes","?:Y"],"&",["influences","?:Y","?:X"]],"=>",["smokes","?:X"]]},

{"@question": ["smokes","carl"]}
]

/*
{"result": "proof found",

"answers": [
{
"answer": false,
"confidence": 0.120107,
"positive_proof":
[
[1,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","carl"]]],
[2,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[3,      8, ["mp", 1, [2,2], "fromgoal", 1, 0, [5]], [["-influences","?:X","carl"], ["-smokes","?:X"]]],
[4,      3, ["in", "frm_4", "axiom", 0.2, 0, []], [["influences","bob","carl"]]],
[5,     10, ["mp", 3, 4, "fromgoal", 0.2, 0, [5,3]], [["-smokes","bob"]]],
[6,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[7,     11, ["mp", 5, [6,2], "fromgoal", 0.2, 0, [5,3]], [["-influences","?:X","bob"], ["-smokes","?:X"]]],
[8,      2, ["in", "frm_3", "axiom", 0.6, 0, []], [["influences","ann","bob"]]],
[9,     15, ["mp", 7, 8, "fromgoal", 0.12, 0, [5,3,2]], [["-smokes","ann"]]],
[10,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[11,     17, ["mp", 9, [10,1], "fromgoal", 0.12, 0, [5,3,2,4]], [["-stress","ann"]]],
[12,      0, ["in", "frm_1", "axiom", 0.8, 0, []], [["stress","ann"]]],
[13,     18, ["simp", 11, 12, "fromgoal", 0.096, 0, [5,3,2,4,0]], false],
[14,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","carl"]]],
[15,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[16,      8, ["mp", 14, [15,2], "fromgoal", 1, 0, [5]], [["-influences","?:X","carl"], ["-smokes","?:X"]]],
[17,      3, ["in", "frm_4", "axiom", 0.2, 0, []], [["influences","bob","carl"]]],
[18,     10, ["mp", 16, 17, "fromgoal", 0.2, 0, [5,3]], [["-smokes","bob"]]],
[19,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[20,     12, ["mp", 18, [19,1], "fromgoal", 0.2, 0, [5,3,4]], [["-stress","bob"]]],
[21,      1, ["in", "frm_2", "axiom", 0.4, 0, []], [["stress","bob"]]],
[22,     13, ["simp", 20, 21, "fromgoal", 0.08, 0, [5,3,4,1]], false],
[23,     20, ["cumul", 13, 22, "fromgoal", 0.120107, 0, [5,3,2,4,0,1]], false]
]}
]}


*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study9-lrn.mln
::::::::::::::
//predicate declarations
Stress(c)
Obs2(c,c)
Obs3(c,c)
Obs4(c)
Obs(c)
Smokes(c)
Influences(c,c)

// 0.936944  Obs(x) => Stress(x)
0.936944  Stress(a1) v !Obs(a1)

// -0.413825  Obs4(x) => Stress(x)
-0.413825  Stress(a1) v !Obs4(a1)

// 0.259245  Obs2(x,y) => Influences(x,y)
0.259245  Influences(a1,a2) v !Obs2(a1,a2)

// -0.910743  Obs3(x,y) => Influences(x,y)
-0.910743  Influences(a1,a2) v !Obs3(a1,a2)

// 0.265083  Stress(x) => Smokes(x)
0.265083  !Stress(a1) v Smokes(a1)

// 1.33609  Smokes(x) ^ Influences(x,y) => Smokes(y)
1.33609  !Influences(a1,a2) v Smokes(a2) v !Smokes(a1)

// -1.20113  Stress(a1)
-1.20113  Stress(a1)

// -1.3289  Influences(a1,a2)
-1.3289  Influences(a1,a2)

// -1.90172  Smokes(a1)
-1.90172  Smokes(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1,a2)
0       Obs2(a1,a2)

// 0       Obs3(a1,a2)
0       Obs3(a1,a2)

// 0       Obs4(a1)
0       Obs4(a1)

::::::::::::::
studymln/mln/study9.db
::::::::::::::
Obs(Ann)
Obs2(Ann,Bob)
Obs3(Bob,Carl)
Obs4(Bob)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Stress(Ann) 0.389011
infer:	Stress(Bob) 0.189031
infer:	Stress(Carl) 0.194031
infer:	Influences(Ann,Ann) 0.218028
infer:	Influences(Ann,Bob) 0.217028
infer:	Influences(Ann,Carl) 0.225027
infer:	Influences(Bob,Ann) 0.174033
infer:	Influences(Bob,Bob) 0.209029
infer:	Influences(Bob,Carl) 0.0770423
infer:	Influences(Carl,Ann) 0.162034
infer:	Influences(Carl,Bob) 0.189031
infer:	Influences(Carl,Carl) 0.207029
infer:	Smokes(Ann) 0.114039
infer:	Smokes(Bob) 0.145035
infer:	Smokes(Carl) 0.138036
liftedinfer -ptpe:	Influences(Ann,Ann) 0
liftedinfer -ptpe:	Influences(Ann,Bob) 0
liftedinfer -ptpe:	Influences(Ann,Carl) 0
liftedinfer -ptpe:	Influences(Bob,Ann) 0
liftedinfer -ptpe:	Influences(Bob,Bob) 0
liftedinfer -ptpe:	Influences(Bob,Carl) 0
liftedinfer -ptpe:	Influences(Carl,Ann) 0
liftedinfer -ptpe:	Influences(Carl,Bob) 0
liftedinfer -ptpe:	Influences(Carl,Carl) 0
liftedinfer -ptpe:	Stress(Ann) 0
liftedinfer -ptpe:	Stress(Bob) 0
liftedinfer -ptpe:	Stress(Carl) 0
liftedinfer -ptpe:	Smokes(Ann) 0
liftedinfer -ptpe:	Smokes(Bob) 0
liftedinfer -ptpe:	Smokes(Carl) 0
liftedinfer -lvg:	Influences(Ann,Ann) 0.74026
liftedinfer -lvg:	Influences(Ann,Bob) 0.498501
liftedinfer -lvg:	Influences(Ann,Carl) 0.9001
liftedinfer -lvg:	Influences(Bob,Ann) 0.89011
liftedinfer -lvg:	Influences(Bob,Bob) 0.775225
liftedinfer -lvg:	Influences(Bob,Carl) 0.875125
liftedinfer -lvg:	Influences(Carl,Ann) 0.893107
liftedinfer -lvg:	Influences(Carl,Bob) 0.433566
liftedinfer -lvg:	Influences(Carl,Carl) 0.879121
liftedinfer -lvg:	Stress(Ann) 0.877123
liftedinfer -lvg:	Stress(Bob) 0.934066
liftedinfer -lvg:	Stress(Carl) 0.941059
liftedinfer -lvg:	Smokes(Ann) 0.927073
liftedinfer -lvg:	Smokes(Bob) 0.932068
liftedinfer -lvg:	Smokes(Carl) 0.766234

*/

