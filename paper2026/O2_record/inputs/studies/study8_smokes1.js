// smoking social network example 1

/*

0.8::stress(ann).
% 0.4::stress(bob).
0.6::influences(ann,bob).
0.2::influences(bob,carl).

smokes(X) :- stress(X).
smokes(X) :- influences(Y,X), smokes(Y).

query(smokes(carl)).

result:  0.096 

*/

[
{"@confidence": 0.8,  "@logic": ["stress","ann"]},
//{"@confidence": 0.4, "@logic": ["stress","bob"]},
{"@confidence": 0.6, "@logic": ["influences","ann","bob"]},
{"@confidence": 0.2, "@logic": ["influences","bob","carl"]},
{"@confidence": 1.0, "@logic": [["stress","?:X"],"=>",["smokes","?:X"]]},
{"@confidence": 1.0, "@logic": [[["smokes","?:Y"],"&",["influences","?:Y","?:X"]],"=>",["smokes","?:X"]]},

{"@question": ["smokes","carl"]}
]

/*

gives same confidence with negative and query strats:

{"result": "proof found",

"answers": [
{
{"answer": true,
"confidence": 0.096,
"positive_proof":
[
[1,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-influences","?:X","?:Y"], ["-smokes","?:X"], ["smokes","?:Y"]]],
[2,      2, ["in", "frm_3", "axiom", 0.2, 0, []], [["influences","bob","carl"]]],
[3,      5, ["in", "frm_6", "goal", 1, 0, []], [["-smokes","carl"]]],
[4,     10, ["mp", 1, 2, 3, "fromgoal", 0.2, 0, [4,2]], [["-smokes","bob"]]],
[5,      1, ["in", "frm_2", "axiom", 0.6, 0, []], [["influences","ann","bob"]]],
[6,      8, ["mp", 1, 5, "fromaxiom", 0.6, 0, [4,1]], [["-smokes","ann"], ["smokes","bob"]]],
[7,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[8,      0, ["in", "frm_1", "axiom", 0.8, 0, []], [["stress","ann"]]],
[9,      7, ["mp", 7, 8, "fromaxiom", 0.8, 0, [3,0]], [["smokes","ann"]]],
[10,      9, ["simp", 6, 9, "fromaxiom", 0.48, 0, [4,1,3,0]], [["smokes","bob"]]],
[11,     11, ["simp", 4, 10, "fromgoal", 0.096, 0, [4,2,1,3,0]], false]
]}
]}

*/

/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study8-lrn.mln
::::::::::::::
//predicate declarations
Stress(c)
Obs2(c,c)
Obs3(c,c)
Obs(c)
Smokes(c)
Influences(c,c)

// 0.816986  Obs(x) => Stress(x)
0.816986  Stress(a1) v !Obs(a1)

// 0.305887  Obs2(x,y) => Influences(x,y)
0.305887  Influences(a1,a2) v !Obs2(a1,a2)

// -0.904943  Obs3(x,y) => Influences(x,y)
-0.904943  Influences(a1,a2) v !Obs3(a1,a2)

// 0.417122  Stress(x) => Smokes(x)
0.417122  !Stress(a1) v Smokes(a1)

// 1.05417  Smokes(x) ^ Influences(x,y) => Smokes(y)
1.05417  !Influences(a1,a2) v Smokes(a2) v !Smokes(a1)

// -0.941437  Stress(a1)
-0.941437  Stress(a1)

// -1.13347  Influences(a1,a2)
-1.13347  Influences(a1,a2)

// -1.56816  Smokes(a1)
-1.56816  Smokes(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1,a2)
0       Obs2(a1,a2)

// 0       Obs3(a1,a2)
0       Obs3(a1,a2)

::::::::::::::
studymln/mln/study8.db
::::::::::::::
Obs(Ann)
Obs2(Ann,Bob)
Obs3(Bob,Carl)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Stress(Ann) 0.39801
infer:	Stress(Bob) 0.19903
infer:	Stress(Carl) 0.233027
infer:	Influences(Ann,Ann) 0.246025
infer:	Influences(Ann,Bob) 0.281022
infer:	Influences(Ann,Carl) 0.251025
infer:	Influences(Bob,Ann) 0.217028
infer:	Influences(Bob,Bob) 0.230027
infer:	Influences(Bob,Carl) 0.0920408
infer:	Influences(Carl,Ann) 0.267023
infer:	Influences(Carl,Bob) 0.228027
infer:	Influences(Carl,Carl) 0.251025
infer:	Smokes(Ann) 0.174033
infer:	Smokes(Bob) 0.185031
infer:	Smokes(Carl) 0.135036
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
liftedinfer -lvg:	Influences(Ann,Ann) 0.896104
liftedinfer -lvg:	Influences(Ann,Bob) 0.796204
liftedinfer -lvg:	Influences(Ann,Carl) 0.491508
liftedinfer -lvg:	Influences(Bob,Ann) 0.888112
liftedinfer -lvg:	Influences(Bob,Bob) 0.922078
liftedinfer -lvg:	Influences(Bob,Carl) 0.742258
liftedinfer -lvg:	Influences(Carl,Ann) 0.87013
liftedinfer -lvg:	Influences(Carl,Bob) 0.919081
liftedinfer -lvg:	Influences(Carl,Carl) 0.896104
liftedinfer -lvg:	Stress(Ann) 0.873127
liftedinfer -lvg:	Stress(Bob) 0.711289
liftedinfer -lvg:	Stress(Carl) 0.615385
liftedinfer -lvg:	Smokes(Ann) 0.899101
liftedinfer -lvg:	Smokes(Bob) 0.932068
liftedinfer -lvg:	Smokes(Carl) 0.741259

*/

