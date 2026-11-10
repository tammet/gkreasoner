// negation handling inconsistency part 3:
// add rules for deriving not flies
// this almost restores consistency
//
// notice the full ruleset cannot be written in problog
// NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 10:7.

/*

% notice that problog does not accept
%% 0.1:: flies(X) :- not bird(X).

% Probabilistic facts:
0.5::bird(a).
0.5::not bird(a).
0.9:: flies(X) :- bird(X).
0.1:: not flies(X) :- bird(X).
%% 0.1:: flies(X) :- not bird(X).
0.9:: not flies(X) :- not bird(X).

% Queries:
query(flies(_)).

result:  
a  0.2025

*/

[
{"@confidence": 0.5, "@logic": ["bird","a"]},
{"@confidence": 0.5, "@logic": ["-bird","a"]},
{"@confidence": 0.9, "@logic": [["bird","?:X"],"=>",["flies","?:X"]]},
{"@confidence": 0.1, "@logic": [["bird","?:X"],"=>",["-flies","?:X"]]},
{"@confidence": 0.1, "@logic": [["-bird","?:X"],"=>",["flies","?:X"]]},
{"@confidence": 0.9, "@logic": [["-bird","?:X"],"=>",["-flies","?:X"]]},
{"@question": ["flies","?:X"]}
//{"@question": ["bird","?:X"]}
]

/*

"answers": [
{
"answer": [["$ans","?:X3"]],
"confidence": -0.393867,
"positive_proof":
[
[1, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[2, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[3, ["mp", 1, 2, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[4, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[5, ["mp", [3,1], 4, "fromgoal", 0.09], [["$ans","?:X"], ["flies","?:X"]]],
[6, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[7, ["mp", [5,1], 6, "fromgoal", 0.09], [["$ans","?:X3"]]]
],
"negative_proof":
[
[1, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[2, ["in", "frm_7", "goal", 1], [["flies","?:X"]]],
[3, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[4, ["mp", 3, 2, "fromgoal", 0.9], [["bird","?:X3"]]],
[5, ["mp", 1, 2, 4, "fromgoal", 0.09], false],
[6, ["mp", 3, 2, "fromgoal", 0.9], [["bird","?:X"]]],
[7, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[8, ["mp", 6, 7, "fromgoal", 0.45], false],
[9, ["cumul", 5, 8, "fromgoal", 0.47475], false],
[10, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[11, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[12, ["mp", 10, 11, "fromaxiom", 0.45], [["flies","a"]]],
[13, ["mp", 1, 12, "fromaxiom", 0.045], [["-bird","a"]]],
[14, ["mp", 13, 6, "fromgoal", 0.0405], false],
[15, ["cumul", 9, 14, "fromgoal", 0.483867], false]
]},
{
"answer": [["$ans","a"]],
"confidence": 0.0144505,
"positive_proof":
[
[1, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[2, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[3, ["mp", 1, 2, "fromaxiom", 0.45], [["flies","a"]]],
[4, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[5, ["mp", 3, 4, "fromgoal", 0.45], [["$ans","a"]]],
[6, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[7, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[8, ["mp", 6, 7, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[9, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[10, ["mp", [8,1], 9, "fromgoal", 0.09], [["$ans","?:X"], ["flies","?:X"]]],
[11, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[12, ["mp", [10,1], 11, "fromgoal", 0.09], [["$ans","?:X3"]]],
[13, ["cumul", 5, 12, "fromgoal", 0.47475], [["$ans","a"]]],
[14, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[15, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[16, ["mp", 14, 15, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[17, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[18, ["mp", [16,1], 17, "fromgoal", 0.05], [["$ans","a"]]],
[19, ["cumul", 13, 18, "fromgoal", 0.490508], [["$ans","a"]]],
[20, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[21, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[22, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[23, ["mp", 21, 22, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[24, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[25, ["mp", [23,1], 24, "fromgoal", 0.09], [["$ans","?:X"], ["flies","?:X"]]],
[26, ["mp", 20, [25,1], "fromgoal", 0.009], [["-bird","?:X"], ["$ans","?:X"]]],
[27, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[28, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[29, ["mp", 27, 28, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[30, ["mp", 26, [29,1], "fromgoal", 0.0009], [["$ans","?:X3"]]],
[31, ["cumul", 19, 30, "fromgoal", 0.490704], [["$ans","a"]]],
[32, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[33, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[34, ["in", "frm_7", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[35, ["mp", 33, 34, "fromgoal", 0.1], [["$ans","?:X"], ["bird","?:X"]]],
[36, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[37, ["mp", [35,1], 36, "fromgoal", 0.09], [["$ans","?:X"], ["flies","?:X"]]],
[38, ["mp", 32, [37,1], "fromgoal", 0.009], [["-bird","?:X"], ["$ans","?:X"]]],
[39, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[40, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[41, ["mp", 39, 40, "fromaxiom", 0.09], [["bird","?:X"]]],
[42, ["mp", 38, 41, "fromgoal", 0.00081], [["$ans","?:X3"]]],
[43, ["cumul", 31, 42, "fromgoal", 0.490842], [["$ans","a"]]]
],
"negative_proof":
[
[1, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[2, ["in", "frm_7", "goal", 1], [["flies","a"]]],
[3, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[4, ["mp", 3, 2, "fromgoal", 0.9], [["bird","a"]]],
[5, ["mp", 1, 2, 4, "fromgoal", 0.09], false],
[6, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[7, ["simp", 4, 6, "fromgoal", 0.45], false],
[8, ["cumul", 5, 7, "fromgoal", 0.47475], false],
[9, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[10, ["mp", 9, 3, "fromaxiom", 0.09], [["bird","?:X"]]],
[11, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[12, ["mp", 10, 11, "fromaxiom", 0.081], [["flies","?:X"]]],
[13, ["mp", 1, 12, "fromaxiom", 0.0081], [["-bird","?:X"]]],
[14, ["mp", 3, 2, "fromgoal", 0.9], [["bird","a"]]],
[15, ["mp", 13, 14, "fromgoal", 0.00729], false],
[16, ["cumul", 8, 15, "fromgoal", 0.476391], false]
]}
]}


*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study20-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs(c)
Flies(c)
Bird(c)

// 0.0305443  Obs(x) => Bird(x)
0.0305443  Bird(a1) v !Obs(a1)

// 4.41746  Obs2(x) => !Bird(x)
4.41746  !Bird(a1) v !Obs2(a1)

// 0.213006  Bird(x) => Flies(x)
0.213006  !Bird(a1) v Flies(a1)

// -0.452706  Bird(x) => !Flies(x)
-0.452706  !Bird(a1) v !Flies(a1)

// -0.660624  !Bird(x) => Flies(x)
-0.660624  Bird(a1) v Flies(a1)

// 1.93394  !Bird(x) => !Flies(x)
1.93394  Bird(a1) v !Flies(a1)

// 0.154701  Bird(a1)
0.154701  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// -0.482121  Flies(a1)
-0.482121  Flies(a1)

::::::::::::::
studymln/mln/study20.db
::::::::::::::
Obs(A)
Obs2(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.020048
infer:	Flies(A) 0.0560444
liftedinfer -ptpe:	Flies(A) 0
liftedinfer -ptpe:	Bird(A) 0.0356304
liftedinfer -lvg:	Flies(A) 0.509491
liftedinfer -lvg:	Bird(A) 0.043956

*/

