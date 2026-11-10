// simplest rule for multiplication of confidences
/*

problog:

% Probabilistic facts:
0.5::bird(a).
0.6::bird(b).

% Rules:
twobirds(dummy) :- bird(a), bird(b).

% Queries:
query(twobirds(dummy)).

result: 0.3

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
 "@confidence": 100,
 "@role":"axiom",
 "@logic":[["-bird","a"], ["-bird","b"], ["twobirds","dummy"]]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["twobirds","dummy"]
}
]

/*

gives same confidence with negative and query strats:

"answers": [
{
{"answer": true,
"confidence": 0.3,
"positive_proof":
[
[1,      2, ["in", "rule1", "axiom", 1, 0, []], [["-bird","b"], ["-bird","a"], ["twobirds","dummy"]]],
[2,      1, ["in", "a2", "axiom", 0.6, 0, []], [["bird","b"]]],
[3,      3, ["in", "q", "goal", 1, 0, []], [["-twobirds","dummy"]]],
[4,      5, ["mp", 1, 2, 3, "fromgoal", 0.6, 0, [2,1]], [["-bird","a"]]],
[5,      0, ["in", "a1", "axiom", 0.5, 0, []], [["bird","a"]]],
[6,      6, ["simp", 4, 5, "fromgoal", 0.3, 0, [2,1,0]], false]
]}
]}

*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study3-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Twobirds(AlchemyPropositionalType)
Obs(c)
Bird(c)

// -0.071478  Obs(x) => Bird(x)
-0.071478  Bird(a1) v !Obs(a1)

// 0.321607  Obs2(x) => Bird(x)
0.321607  Bird(a1) v !Obs2(a1)

// Bird(A) ^ Bird(B) => Twobirds.
!Bird(A) v !Bird(B) v Twobirds.

// 0.0665082  Bird(a1)
0.0665082  Bird(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

// -1.12649  Twobirds
-1.12649  Twobirds

::::::::::::::
studymln/mln/study3.db
::::::::::::::
Obs(A)
Obs2(B)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(A) 0.331017
infer:	Bird(B) 0.505
infer:	Twobirds 0.318018
liftedinfer -ptpe:	Twobirds(AlchemyPropositionalConstant) 0
liftedinfer -ptpe:	Bird(A) 0.800291
liftedinfer -ptpe:	Bird(B) 0.800291
liftedinfer -lvg:	Twobirds(AlchemyPropositionalConstant) 0.735265
liftedinfer -lvg:	Bird(A) 0.788212
liftedinfer -lvg:	Bird(B) 0.601399

*/

