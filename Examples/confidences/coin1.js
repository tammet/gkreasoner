/*
% Probabilistic facts:
0.5::heads1.
0.6::heads2.

% Rules:
twoHeads :- heads1, heads2.

% Queries:
query(heads1).
query(heads2).
query(twoHeads).
*/

[
{
 "@name":"a1", 
 "@confidence": 50,
 "@role":"axiom",
 "@logic":["p","heads1"]
},
{
 "@name":"a2", 
 "@confidence": 60,
 "@role":"axiom",
 "@logic":["p","heads2"]
},
{
 "@name":"pr1", 
 "@confidence": 100, 
 "@role":"axiom",
 "@logic":[["-p","heads1"], ["-p","heads2"], ["r","c"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["r","?:X"]
}
]