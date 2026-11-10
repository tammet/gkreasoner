// negation handling differs in confer and problog

/*

problog:

% Probabilistic facts:
0.5::bird(a).
0.5::not bird(a).

% Queries:
query(bird(a)).

result: 0.25
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
 "@confidence": 0.5,
 "@role":"axiom",
 "@logic":["-bird","a"]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["bird","a"]
}
]

/*

gives same confidence with negative and query strats:
{"result": "proof found",

"answers": [
{
{"answer": true,
"confidence": 0,
"positive_proof":
[
[1,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[2,      2, ["in", "q", "goal", 1, 0, []], [["-bird","a"]]],
[3,      4, ["mp", 1, 2, "fromgoal", 0.5, 0, [0]], false]
],
"negative_proof":
[
[1,      1, ["in", "a2", "axiom", 0.5, 0, []], [["-bird","a"]]],
[2,      3, ["in", "$auto_negated_question", "goal", 1, 0, []], [["bird","a"]]],
[3,      6, ["simp", 1, 2, "fromgoal", 0.5, 0, [1]], false]
]}
]}



*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study5-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs(c)
Bird(c)

// 0.685349  Obs(x) => Bird(x)
0.685349  Bird(a1) v !Obs(a1)

// 3.93714  Obs2(x) => !Bird(x)
3.93714  !Bird(a1) v !Obs2(a1)

// -0.68921  Bird(a1)
-0.68921  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

::::::::::::::
studymln/mln/study5.db
::::::::::::::
Obs(A)
Obs2(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.0150485
liftedinfer -ptpe:	Bird(A) 0
liftedinfer -lvg:	Bird(A) 0.0819181

*/

