/*
0.5::heads1.
0.6::heads2.

% Rules:
someHeads :- heads1.
someHeads :- heads2.

% Queries:
query(someHeads).
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
 "@logic":[["-p","heads1"], ["r","c"]]
},
{
 "@name":"pr2", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":[["-p","heads2"], ["r","c"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["r","?:X"]
}
]