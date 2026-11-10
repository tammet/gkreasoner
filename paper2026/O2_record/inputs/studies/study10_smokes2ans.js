// like smoking social network example 2, but asking for all answers:
// slightly different cumulative effect

/*

0.8::stress(ann).
0.4::stress(bob).
0.6::influences(ann,bob).
0.2::influences(bob,carl).

smokes(X) :- stress(X).
smokes(X) :- influences(Y,X), smokes(Y).

query(smokes(X)).

result:  
smokes(ann)	0.8
smokes(bob)	0.688
smokes(carl) 0.1376 

*/

[
{"@confidence": 0.8, "@logic": ["stress","ann"]},
{"@confidence": 0.4, "@logic": ["stress","bob"]},
{"@confidence": 0.6, "@logic": ["influences","ann","bob"]},
{"@confidence": 0.2, "@logic": ["influences","bob","carl"]},
{"@confidence": 1.0, "@logic": [["stress","?:X"],"=>",["smokes","?:X"]]},
{"@confidence": 1.0, "@logic": [[["smokes","?:Y"],"&",["influences","?:Y","?:X"]],"=>",["smokes","?:X"]]},

{"@question": ["smokes","?:X"]}
]

/*{"result": "proof found",

"answers": [
{
"answer": [["$ans","ann"]],
"confidence": 0.8,
"positive_proof":
[
[1,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[2,      0, ["in", "frm_1", "axiom", 0.8, 0, []], [["stress","ann"]]],
[3,      7, ["mp", 1, 2, "fromaxiom", 0.8, 0, [4,0]], [["smokes","ann"]]],
[4,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","?:X"], ["$ans","?:X"]]],
[5,      9, ["mp", 3, 4, "fromgoal", 0.8, 0, [4,0]], [["$ans","ann"]]]
]},
{
"answer": [["$ans","bob"]],
"confidence": 0.618667,
"positive_proof":
[
[1,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[2,      2, ["in", "frm_3", "axiom", 0.6, 0, []], [["influences","ann","bob"]]],
[3,     13, ["mp", 1, 2, "fromaxiom", 0.6, 0, [5,2]], [["-smokes","ann"], ["smokes","bob"]]],
[4,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[5,      0, ["in", "frm_1", "axiom", 0.8, 0, []], [["stress","ann"]]],
[6,      7, ["mp", 4, 5, "fromaxiom", 0.8, 0, [4,0]], [["smokes","ann"]]],
[7,     14, ["simp", 3, 6, "fromaxiom", 0.48, 0, [5,2,4,0]], [["smokes","bob"]]],
[8,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","?:X"], ["$ans","?:X"]]],
[9,     16, ["mp", 7, 8, "fromgoal", 0.48, 0, [5,2,4,0]], [["$ans","bob"]]],
[10,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[11,      1, ["in", "frm_2", "axiom", 0.4, 0, []], [["stress","bob"]]],
[12,      8, ["mp", 10, 11, "fromaxiom", 0.4, 0, [4,1]], [["smokes","bob"]]],
[13,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","?:X"], ["$ans","?:X"]]],
[14,     10, ["mp", 12, 13, "fromgoal", 0.4, 0, [4,1]], [["$ans","bob"]]],
[15,     21, ["cumul", 9, 14, "fromgoal", 0.618667, 0, [5,2,4,0,1]], [["$ans","bob"]]]
]},
{
"answer": [["$ans","carl"]],
"confidence": 0.120107,
"positive_proof":
[
[1,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[2,      3, ["in", "frm_4", "axiom", 0.2, 0, []], [["influences","bob","carl"]]],
[3,     11, ["mp", 1, 2, "fromaxiom", 0.2, 0, [5,3]], [["-smokes","bob"], ["smokes","carl"]]],
[4,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[5,      2, ["in", "frm_3", "axiom", 0.6, 0, []], [["influences","ann","bob"]]],
[6,     13, ["mp", 4, 5, "fromaxiom", 0.6, 0, [5,2]], [["-smokes","ann"], ["smokes","bob"]]],
[7,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[8,      0, ["in", "frm_1", "axiom", 0.8, 0, []], [["stress","ann"]]],
[9,      7, ["mp", 7, 8, "fromaxiom", 0.8, 0, [4,0]], [["smokes","ann"]]],
[10,     14, ["simp", 6, 9, "fromaxiom", 0.48, 0, [5,2,4,0]], [["smokes","bob"]]],
[11,     17, ["mp", 3, 10, "fromaxiom", 0.096, 0, [5,3,2,4,0]], [["smokes","carl"]]],
[12,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","?:X"], ["$ans","?:X"]]],
[13,     19, ["mp", 11, 12, "fromgoal", 0.096, 0, [5,3,2,4,0]], [["$ans","carl"]]],
[14,      5, ["in", "frm_6", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[15,      3, ["in", "frm_4", "axiom", 0.2, 0, []], [["influences","bob","carl"]]],
[16,     11, ["mp", 14, 15, "fromaxiom", 0.2, 0, [5,3]], [["-smokes","bob"], ["smokes","carl"]]],
[17,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[18,      1, ["in", "frm_2", "axiom", 0.4, 0, []], [["stress","bob"]]],
[19,      8, ["mp", 17, 18, "fromaxiom", 0.4, 0, [4,1]], [["smokes","bob"]]],
[20,     12, ["simp", 16, 19, "fromaxiom", 0.08, 0, [5,3,4,1]], [["smokes","carl"]]],
[21,      6, ["in", "frm_7", "goal", 1, 0, []], [["-smokes","?:X"], ["$ans","?:X"]]],
[22,     15, ["mp", 20, 21, "fromgoal", 0.08, 0, [5,3,4,1]], [["$ans","carl"]]],
[23,     22, ["cumul", 13, 22, "fromgoal", 0.120107, 0, [5,3,2,4,0,1]], [["$ans","carl"]]]
]}
]}

*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study10-lrn.mln
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
studymln/mln/study10.db
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
liftedinfer -lvg:	Influences(Ann,Ann) 0.703297
liftedinfer -lvg:	Influences(Ann,Bob) 0.782218
liftedinfer -lvg:	Influences(Ann,Carl) 0.475524
liftedinfer -lvg:	Influences(Bob,Ann) 0.9001
liftedinfer -lvg:	Influences(Bob,Bob) 0.904096
liftedinfer -lvg:	Influences(Bob,Carl) 0.668332
liftedinfer -lvg:	Influences(Carl,Ann) 0.892108
liftedinfer -lvg:	Influences(Carl,Bob) 0.883117
liftedinfer -lvg:	Influences(Carl,Carl) 0.877123
liftedinfer -lvg:	Stress(Ann) 0.874126
liftedinfer -lvg:	Stress(Bob) 0.955045
liftedinfer -lvg:	Stress(Carl) 0.85015
liftedinfer -lvg:	Smokes(Ann) 0.894106
liftedinfer -lvg:	Smokes(Bob) 0.728272
liftedinfer -lvg:	Smokes(Carl) 0.796204

*/

