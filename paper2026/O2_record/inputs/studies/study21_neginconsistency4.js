// negation handling inconsistency part 4:
// add rules for deriving not flies
// this almost restores consistency
//
// this time we check whether additional rules
// modify the bird(a) confidence
//
// notice the full ruleset cannot be written in problog:
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
//{"@question": ["flies","?:X"]}
{"@question": ["bird","?:X"]}
]

/*

{"result": "proof found",

"answers": [
{
"answer": [["$ans","?:X3"]],
"confidence": -0.51538,
"positive_proof":
[
[1, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[2, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[3, ["mp", 1, 2, "fromaxiom", 0.09], [["bird","?:X"]]],
[4, ["in", "frm_7", "goal", 1], [["-bird","?:X"], ["$ans","?:X"]]],
[5, ["mp", 3, 4, "fromgoal", 0.09], [["$ans","?:X3"]]]
],
"negative_proof":
[
[1, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[2, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[3, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[4, ["mp", 2, 3, "fromaxiom", 0.45], [["flies","a"]]],
[5, ["mp", 1, 4, "fromaxiom", 0.045], [["-bird","a"]]],
[6, ["in", "frm_7", "goal", 1], [["bird","?:X"]]],
[7, ["mp", 5, 6, "fromgoal", 0.045], false],
[8, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[9, ["mp", 8, 6, "fromgoal", 0.5], false],
[10, ["cumul", 7, 9, "fromgoal", 0.5225], false],
[11, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[12, ["mp", 2, 6, "fromgoal", 0.9], [["flies","?:X"]]],
[13, ["mp", 11, 12, "fromgoal", 0.81], [["bird","?:X"]]],
[14, ["mp", 13, 8, "fromgoal", 0.405], false],
[15, ["cumul", 10, 14, "fromgoal", 0.60538], false]
]},
{
"answer": [["$ans","a"]],
"confidence": -0.00864017,
"positive_proof":
[
[1, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[2, ["in", "frm_7", "goal", 1], [["-bird","?:X"], ["$ans","?:X"]]],
[3, ["mp", 1, 2, "fromgoal", 0.5], [["$ans","a"]]],
[4, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[5, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[6, ["mp", 4, 5, "fromaxiom", 0.09], [["bird","?:X"]]],
[7, ["in", "frm_7", "goal", 1], [["-bird","?:X"], ["$ans","?:X"]]],
[8, ["mp", 6, 7, "fromgoal", 0.09], [["$ans","?:X3"]]],
[9, ["cumul", 3, 8, "fromgoal", 0.545], [["$ans","a"]]]
],
"negative_proof":
[
[1, ["in", "frm_4", "axiom", 0.1], [["-flies","?:X"], ["-bird","?:X"]]],
[2, ["in", "frm_3", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[3, ["in", "frm_7", "goal", 1], [["bird","a"]]],
[4, ["mp", 2, 3, "fromgoal", 0.9], [["flies","a"]]],
[5, ["in", "frm_7", "goal", 1], [["bird","a"]]],
[6, ["mp", 1, 4, 5, "fromgoal", 0.09], false],
[7, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[8, ["simp", 7, 5, "fromgoal", 0.5], false],
[9, ["cumul", 6, 8, "fromgoal", 0.545], false],
[10, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[11, ["mp", 2, 10, "fromaxiom", 0.45], [["flies","a"]]],
[12, ["mp", 1, 11, 5, "fromgoal", 0.045], false],
[13, ["cumul", 9, 12, "fromgoal", 0.551825], false],
[14, ["in", "frm_5", "axiom", 0.1], [["flies","?:X"], ["bird","?:X"]]],
[15, ["in", "frm_6", "axiom", 0.9], [["-flies","?:X"], ["bird","?:X"]]],
[16, ["mp", 14, 15, "fromaxiom", 0.09], [["bird","?:X"]]],
[17, ["mp", 16, 2, "fromaxiom", 0.081], [["flies","?:X"]]],
[18, ["mp", 1, 17, "fromaxiom", 0.0081], [["-bird","?:X"]]],
[19, ["mp", 18, 3, "fromgoal", 0.0081], false],
[20, ["cumul", 13, 19, "fromgoal", 0.55364], false]
]}
]}


*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study21-lrn.mln
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
studymln/mln/study21.db
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
liftedinfer -lvg:	Flies(A) 0.561439
liftedinfer -lvg:	Bird(A) 0.043956

*/

