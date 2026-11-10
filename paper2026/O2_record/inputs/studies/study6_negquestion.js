// negation handling differs in confer and problog

/*

% Probabilistic facts:
0.5::bird(a).
0.6::bird(a).
0.5::not bird(a).

% Queries:
query(bird(X)).

result: 
bird(a) 0.4

*/

[
{
 "@name":"a1", 
 "@confidence": 0.5,
 "@role":"axiom",
 "@logic":["bird","a"]
},
{
 "@name":"a2", 
 "@confidence": 0.6,
 "@role":"axiom",
 "@logic":["bird","a"]
},
{
 "@name":"na1", 
 "@confidence": 0.5,
 "@role":"axiom",   
 "@logic": ["-bird","a"]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["bird","?:X"]
}
]

/*

gives same confidence with negative and query strats:
{"result": "proof found",

"answers": [
{
"answer": [["$ans","a"]],
"confidence": 0.3,
"positive_proof":
[
[1,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","a"]]],
[2,      3, ["in", "q", "goal", 1, 0, []], [["-bird","?:X"], ["$ans","?:X"]]],
[3,      5, ["mp", 1, 2, "fromgoal", 0.6, 0, [1]], [["$ans","a"]]],
[4,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[5,      3, ["in", "q", "goal", 1, 0, []], [["-bird","?:X"], ["$ans","?:X"]]],
[6,      4, ["mp", 4, 5, "fromgoal", 0.5, 0, [0]], [["$ans","a"]]],
[7,      8, ["cumul", 3, 6, "fromgoal", 0.8, 0, [1,0]], [["$ans","a"]]]
],
"negative_proof":
[
[1,      2, ["in", "na1", "axiom", 0.5, 0, []], [["-bird","a"]]],
[2,      9, ["in", "q", "goal", 1, 0, []], [["bird","a"]]],
[3,     10, ["simp", 1, 2, "fromgoal", 0.5, 0, [2]], false]
]}
]}



*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study6-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs3(c)
Obs(c)
Bird(c)

// 0.314844  Obs(x) => Bird(x)
0.314844  Bird(a1) v !Obs(a1)

// 0.729438  Obs2(x) => Bird(x)
0.729438  Bird(a1) v !Obs2(a1)

// 4.15491  Obs3(x) => !Bird(x)
4.15491  !Bird(a1) v !Obs3(a1)

// -0.334538  Bird(a1)
-0.334538  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// 0       Obs3(a1)
0       Obs3(a1)

::::::::::::::
studymln/mln/study6.db
::::::::::::::
Obs(A)
Obs2(A)
Obs3(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.0370463
liftedinfer -ptpe:	Bird(A) 0
liftedinfer -lvg:	Bird(A) 0.118881

*/

