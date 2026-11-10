/*

problog:

% Probabilistic facts:
0.5::bird(a).
0.5::bird(a).

% Queries:
query(bird(a)).

result: 0.75
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
 "@logic":["bird","a"]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["bird","a"]
}
]

/*

gives same confidence with negative and query strats:

"answers": [
{
"answer": false,
"confidence": 0.75,
"positive_proof":
[
[1,      2, ["in", "q", "goal", 1, 0, []], [["-bird","a"]]],
[2,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[3,      5, ["mp", 1, 2, "fromgoal", 0.5, 0, [0]], false],
[4,      2, ["in", "q", "goal", 1, 0, []], [["-bird","a"]]],
[5,      1, ["in", "a2", "axiom", 0.5, 0, []], [["bird","a"]]],
[6,      4, ["mp", 4, 5, "fromgoal", 0.5, 0, [1]], false],
[7,      6, ["cumul", 3, 6, "fromgoal", 0.75, 0, [0,1]], false]
]}
]}

*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study1-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs(c)
Bird(c)

// 0.00788244  Obs(x) => Bird(x)
0.00788244  Bird(a1) v !Obs(a1)

// 0.00434364  Obs2(x) => Bird(x)
0.00434364  Bird(a1) v !Obs2(a1)

// 0.00703424  Bird(a1)
0.00703424  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

::::::::::::::
studymln/mln/study1.db
::::::::::::::
Obs(A)
Obs2(A)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.501
liftedinfer -ptpe:	Bird(A) 0.504815
liftedinfer -lvg:	Bird(A) 0.495504

*/

