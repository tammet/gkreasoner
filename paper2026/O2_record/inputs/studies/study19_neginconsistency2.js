// negation handling inconsistency part 2:
// we get a zero confidence that "a" is a bird
// while the inconsistency part 1 gives
// a 0.45 confidence that "a" flies,


/*

% notice that problog is consistent in its
% interpretation: 0.25*0.9=0.225 we get in part 1

% Probabilistic facts:
0.5::bird(a).
0.5::not bird(a).
0.9:: flies(X) :- bird(X).

% Queries:
query(bird(_)).

result: 
a  0.25


*/

[
{"@confidence": 0.5, "@logic": ["bird","a"]},
{"@confidence": 0.5, "@logic": ["-bird","a"]},
{"@confidence": 0.9, "@logic": [["bird","?:X"],"=>",["flies","?:X"]]},
//{"@question": ["flies","?:X"]}
{"@question": ["bird","?:X"]}
]

/*

{"result": "proof found",

"answers": [
{
"answer": [["$ans","a"]],
"confidence": 0,
"positive_proof":
[
[1, ["in", "frm_1", "axiom", 0.5], [["bird","a"]]],
[2, ["in", "frm_4", "goal", 1], [["-bird","?:X"], ["$ans","?:X"]]],
[3, ["mp", 1, 2, "fromgoal", 0.5], [["$ans","a"]]]
],
"negative_proof":
[
[1, ["in", "frm_2", "axiom", 0.5], [["-bird","a"]]],
[2, ["in", "frm_4", "goal", 1], [["bird","a"]]],
[3, ["simp", 1, 2, "fromgoal", 0.5], false]
]}
]}

*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study19-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs(c)
Flies(c)
Bird(c)

// -2.77202  Obs(x) => Bird(x)
-2.77202  Bird(a1) v !Obs(a1)

// 6.8762  Obs2(x) => !Bird(x)
6.8762  !Bird(a1) v !Obs2(a1)

// 3.18368  Bird(x) => Flies(x)
3.18368  !Bird(a1) v Flies(a1)

// 5.17133  Bird(a1)
5.17133  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// -2.86368  Flies(a1)
-2.86368  Flies(a1)

::::::::::::::
studymln/mln/study19.db
::::::::::::::
Obs(A)
Obs2(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.0030497
infer:	Flies(A) 0.0470453
liftedinfer -ptpe:	Flies(A) 0
liftedinfer -ptpe:	Bird(A) 0.330733
liftedinfer -lvg:	Flies(A) 0.976024
liftedinfer -lvg:	Bird(A) 0.015984

*/

