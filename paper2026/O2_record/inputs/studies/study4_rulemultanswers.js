// like study3, but asking for answer substitutions
/*

problog:

% Probabilistic facts:
0.5::bird(a).
0.6::bird(b).

twobirds(X,Y) :- bird(X), bird(Y).

% Queries:
query(twobirds(X,Y)).

results: 

twobirds(a,a)	0.5
twobirds(a,b)	0.3
twobirds(b,a)	0.3
twobirds(b,b)	0.6 

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
 "@logic":["bird","b"]
},
{
 "@name":"rule1", 
 "@confidence": 1.0,
 "@role":"axiom",
 "@logic":[["-bird","?:X"], ["-bird","?:Y"], ["twobirds","?:X","?:Y"]]
},
{
 "@name":"q", 
 "@question": ["twobirds","?:X","?:Y"]
}
]

/*

gives same confidence with negative and query strats:

"answers": [
{
"answer": [["$ans","a","a"]],
"confidence": 0.5,
"positive_proof":
[
[1,      2, ["in", "rule1", "axiom", 1, 0, []], [["twobirds","?:X","?:Y"], ["-bird","?:Y"], ["-bird","?:X"]]],
[2,      4, ["merge", [1,1,2], "fromaxiom", 1, 0, [2]], [["twobirds","?:X","?:X"], ["-bird","?:X"]]],
[3,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[4,      7, ["mp", [2,1], 3, "fromaxiom", 0.5, 0, [2,0]], [["twobirds","a","a"]]],
[5,      3, ["in", "q", "goal", 1, 0, []], [["-twobirds","?:X","?:Y"], ["$ans","?:X","?:Y"]]],
[6,      9, ["mp", 4, 5, "fromgoal", 0.5, 0, [2,0]], [["$ans","a","a"]]]
]},
{
"answer": [["$ans","b","b"]],
"confidence": 0.6,
"positive_proof":
[
[1,      2, ["in", "rule1", "axiom", 1, 0, []], [["twobirds","?:X","?:Y"], ["-bird","?:Y"], ["-bird","?:X"]]],
[2,      4, ["merge", [1,1,2], "fromaxiom", 1, 0, [2]], [["twobirds","?:X","?:X"], ["-bird","?:X"]]],
[3,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","b"]]],
[4,      8, ["mp", [2,1], 3, "fromaxiom", 0.6, 0, [2,1]], [["twobirds","b","b"]]],
[5,      3, ["in", "q", "goal", 1, 0, []], [["-twobirds","?:X","?:Y"], ["$ans","?:X","?:Y"]]],
[6,     10, ["mp", 4, 5, "fromgoal", 0.6, 0, [2,1]], [["$ans","b","b"]]]
]},
{
"answer": [["$ans","b","a"]],
"confidence": 0.3,
"positive_proof":
[
[1,      2, ["in", "rule1", "axiom", 1, 0, []], [["twobirds","?:X","?:Y"], ["-bird","?:Y"], ["-bird","?:X"]]],
[2,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[3,      5, ["mp", [1,1], 2, "fromaxiom", 0.5, 0, [2,0]], [["twobirds","?:X","a"], ["-bird","?:X"]]],
[4,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","b"]]],
[5,     12, ["mp", [3,1], 4, "fromaxiom", 0.3, 0, [2,0,1]], [["twobirds","b","a"]]],
[6,      3, ["in", "q", "goal", 1, 0, []], [["-twobirds","?:X","?:Y"], ["$ans","?:X","?:Y"]]],
[7,     13, ["mp", 5, 6, "fromgoal", 0.3, 0, [2,0,1]], [["$ans","b","a"]]]
]},
{
"answer": [["$ans","a","b"]],
"confidence": 0.3,
"positive_proof":
[
[1,      2, ["in", "rule1", "axiom", 1, 0, []], [["twobirds","?:X","?:Y"], ["-bird","?:Y"], ["-bird","?:X"]]],
[2,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","b"]]],
[3,      6, ["mp", [1,1], 2, "fromaxiom", 0.6, 0, [2,1]], [["twobirds","?:X","b"], ["-bird","?:X"]]],
[4,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[5,     14, ["mp", [3,1], 4, "fromaxiom", 0.3, 0, [2,1,0]], [["twobirds","a","b"]]],
[6,      3, ["in", "q", "goal", 1, 0, []], [["-twobirds","?:X","?:Y"], ["$ans","?:X","?:Y"]]],
[7,     16, ["mp", 5, 6, "fromgoal", 0.3, 0, [2,1,0]], [["$ans","a","b"]]]
]}
]}


*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study4-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Twobirds(c,c)
Obs(c)
Bird(c)

// 0.285154  Obs(x) => Bird(x)
0.285154  Bird(a1) v !Obs(a1)

// 0.416121  Obs2(x) => Bird(x)
0.416121  Bird(a1) v !Obs2(a1)

// Bird(x) ^ Bird(y) => Twobirds(x,y).
!Bird(a1) v !Bird(a2) v Twobirds(a1,a2).

// 0.806418  Bird(a1)
0.806418  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// -0.0146565  Twobirds(a1,a2)
-0.0146565  Twobirds(a1,a2)

::::::::::::::
studymln/mln/study4.db
::::::::::::::
Obs(A)
Obs2(B)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.452005
infer:	Bird(B) 0.479002
infer:	Twobirds(A,A) 0.740976
infer:	Twobirds(A,B) 0.586991
infer:	Twobirds(B,A) 0.559994
infer:	Twobirds(B,B) 0.739976
liftedinfer -ptpe:	Twobirds(A,A) 0
liftedinfer -ptpe:	Twobirds(A,B) 0
liftedinfer -ptpe:	Twobirds(B,A) 0
liftedinfer -ptpe:	Twobirds(B,B) 0
liftedinfer -ptpe:	Bird(A) 0.818719
liftedinfer -ptpe:	Bird(B) 0.818719
liftedinfer -lvg:	Twobirds(A,A) 0.732268
liftedinfer -lvg:	Twobirds(A,B) 0.719281
liftedinfer -lvg:	Twobirds(B,A) 0.719281
liftedinfer -lvg:	Twobirds(B,B) 0.776224
liftedinfer -lvg:	Bird(A) 0
liftedinfer -lvg:	Bird(B) 0.814186

*/

