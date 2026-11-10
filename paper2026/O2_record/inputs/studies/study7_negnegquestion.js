// negation handling differs in confer and problog

/*

% Probabilistic facts:
0.5::bird(a).
0.6::bird(a).
0.5::not bird(a).

% Queries:
query(not bird(X)).

result: 
ProbLog exceeded time or memory limit

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
 "@logic": ["-bird","?:X"]
}
]

/*

gives same confidence with negative and query strats:

{"result": "proof found",

"answers": [
{
"answer": [["$ans","a"]],
"confidence": -0.3,
"positive_proof":
[
[1,      2, ["in", "na1", "axiom", 0.5, 0, []], [["-bird","a"]]],
[2,      3, ["in", "q", "goal", 1, 0, []], [["$ans","?:X"], ["bird","?:X"]]],
[3,      4, ["mp", 1, [2,1], "fromgoal", 0.5, 0, [2]], [["$ans","a"]]]
],
"negative_proof":
[
[1,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","a"]]],
[2,      7, ["in", "q", "goal", 1, 0, []], [["-bird","a"]]],
[3,      9, ["mp", 1, 2, "fromgoal", 0.6, 0, [1]], false],
[4,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[5,      8, ["mp", 4, 2, "fromgoal", 0.5, 0, [0]], false],
[6,     12, ["cumul", 3, 5, "fromgoal", 0.8, 0, [1,0]], false]
]}
]}


*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study7-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs3(c)
Notbird(c)
Obs(c)
Bird(c)

// -35.9996  Obs(x) => Bird(x)
-35.9996  Bird(a1) v !Obs(a1)

// -15.9998  Obs2(x) => Bird(x)
-15.9998  Bird(a1) v !Obs2(a1)

// 103.999  Obs3(x) => !Bird(x)
103.999  !Bird(a1) v !Obs3(a1)

// !Bird(x) => Notbird(x).
Bird(a1) v Notbird(a1).

// -155.998  Bird(a1)
-155.998  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// 0       Obs3(a1)
0       Obs3(a1)

// -603.992  Notbird(a1)
-603.992  Notbird(a1)

::::::::::::::
studymln/mln/study7.db
::::::::::::::
Obs(A)
Obs2(A)
Obs3(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.99995
infer:	Notbird(A) 4.9995e-05
liftedinfer -ptpe:	Notbird(A) 0
liftedinfer -ptpe:	Bird(A) 0
liftedinfer -lvg:	Notbird(A) 1
liftedinfer -lvg:	Bird(A) 0

*/

