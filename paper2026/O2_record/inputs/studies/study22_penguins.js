// classic penguins do not fly example
// this time with probabilities instead of defaults

/*

1.0::bird(tweety).
1.0::penguin(pennie).

1.0:: bird(X) :- penguin(X).

0.001:: penguin(X) :- bird(X).
% 0.999:: not penguin(X) :- bird(X).

0.9:: flies(X) :- bird(X).
1.0:: not flies(X) :- penguin(X).

% Queries:
query(flies(_)).

result:
flies(pennie)	0
flies(tweety)	0.8991 

% adding the outcommented rule
% 0.999:: not penguin(X) :- bird(X). 
% gives error:
% NegativeCycle: Negative cycle detected

% the same rule could be commented out from the
% js rules below, with no bad consequences: 
% it is not used in the proof below


*/

[

{"@confidence": 1.0, "@logic": ["bird","tweety"]},
{"@confidence": 1.0, "@logic": ["penguin","pennie"]},

{"@confidence": 1.0, "@logic":   [["penguin","?:X"],"=>",["bird","?:X"]]},

{"@confidence": 0.001, "@logic": [["bird","?:X"],"=>",["penguin","?:X"]]},
//{"@confidence": 0.999, "@logic": [["bird","?:X"],"=>",["-penguin","?:X"]]},

{"@confidence": 0.9, "@logic": [["bird","?:X"],"=>",["flies","?:X"]]},

{"@confidence": 1.0, "@logic": [["penguin","?:X"],"=>",["-flies","?:X"]]},

{"@question": ["flies","?:X"]}

]


/*

{"result": "proof found",

"answers": [
{
"answer": [["$ans","pennie"]],
"confidence": -0.0999,
"positive_proof":
[
[1, ["in", "frm_6", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[2, ["in", "frm_3", "axiom", 1], [["-penguin","?:X"], ["bird","?:X"]]],
[3, ["in", "frm_2", "axiom", 1], [["penguin","pennie"]]],
[4, ["mp", 2, 3, "fromaxiom", 1], [["bird","pennie"]]],
[5, ["mp", 1, 4, "fromaxiom", 0.9], [["flies","pennie"]]],
[6, ["in", "frm_8", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[7, ["mp", 5, 6, "fromgoal", 0.9], [["$ans","pennie"]]]
],
"negative_proof":
[
[1, ["in", "frm_7", "axiom", 0.9999], [["-flies","?:X"], ["-penguin","?:X"]]],
[2, ["in", "frm_8", "goal", 1], [["flies","pennie"]]],
[3, ["mp", 1, 2, "fromgoal", 0.9999], [["-penguin","pennie"]]],
[4, ["in", "frm_2", "axiom", 1], [["penguin","pennie"]]],
[5, ["simp", 3, 4, "fromgoal", 0.9999], false]
]},
{
"answer": [["$ans","tweety"]],
"confidence": 0.899,
"positive_proof":
[
[1, ["in", "frm_6", "axiom", 0.9], [["-bird","?:X"], ["flies","?:X"]]],
[2, ["in", "frm_1", "axiom", 1], [["bird","tweety"]]],
[3, ["mp", 1, 2, "fromaxiom", 0.9], [["flies","tweety"]]],
[4, ["in", "frm_8", "goal", 1], [["-flies","?:X"], ["$ans","?:X"]]],
[5, ["mp", 3, 4, "fromgoal", 0.9], [["$ans","tweety"]]]
],
"negative_proof":
[
[1, ["in", "frm_7", "axiom", 0.9999], [["-flies","?:X"], ["-penguin","?:X"]]],
[2, ["in", "frm_8", "goal", 1], [["flies","tweety"]]],
[3, ["mp", 1, 2, "fromgoal", 0.9999], [["-penguin","tweety"]]],
[4, ["in", "frm_4", "axiom", 0.001], [["-bird","?:X"], ["penguin","?:X"]]],
[5, ["in", "frm_1", "axiom", 1], [["bird","tweety"]]],
[6, ["mp", 4, 5, "fromaxiom", 0.001], [["penguin","tweety"]]],
[7, ["simp", 3, 6, "fromgoal", 0.0009999], false]
]}
]}



*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study22-lrn.mln
::::::::::::::
//predicate declarations
Penguin(c)
Flies(c)
Bird(c)

// Penguin(x) => Bird(x).
Bird(a1) v !Penguin(a1).

// -2.14381  Bird(x) => Penguin(x)
-2.14381  !Bird(a1) v Penguin(a1)

// 2.14381  Bird(x) => !Penguin(x)
2.14381  !Bird(a1) v !Penguin(a1)

// -1.20469  Bird(x) => Flies(x)
-1.20469  !Bird(a1) v Flies(a1)

// Penguin(x) => !Flies(x).
!Penguin(a1) v !Flies(a1).

// 0       Bird(a1)
0       Bird(a1)

// -2.14381  Penguin(a1)
-2.14381  Penguin(a1)

// -1.20469  Flies(a1)
-1.20469  Flies(a1)

::::::::::::::
studymln/mln/study22.db
::::::::::::::
Bird(Tweety)
Penguin(Pennie)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Flies(Tweety) 0.0640436
infer:	Flies(Pennie) 4.9995e-05
infer:	Penguin(Tweety) 4.9995e-05
liftedinfer -ptpe:	Penguin(Tweety) 0
liftedinfer -ptpe:	Flies(Tweety) 0
liftedinfer -ptpe:	Flies(Pennie) 0
liftedinfer -lvg:	Penguin(Tweety) 0
liftedinfer -lvg:	Flies(Tweety) 0.873127
liftedinfer -lvg:	Flies(Pennie) 0

*/

