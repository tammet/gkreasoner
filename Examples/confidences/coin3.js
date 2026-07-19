/*
% Probabilistic facts:
0.6::lands_heads(_).

% Background information:
coin(c1).
coin(c2).
coin(c3).
coin(c4).

% Rules:
heads(C) :- coin(C), lands_heads(C).
someHeads :- heads(_).

% Queries:
query(someHeads).
*/

[
{
 "@name":"a1", 
 "@confidence": 60,
 "@role":"axiom",
 "@logic":["lands_heads","?:X"]
},
{
 "@name":"c1", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["coin","c1"]
},
{
 "@name":"c2", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["coin","c2"]
},
{
 "@name":"c3", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["coin","c3"]
},
{
 "@name":"c4", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["coin","c4"]
},

{
 "@name":"pr1", 
 "@confidence": 100, 
 "@role":"axiom",
 "@logic":[["-lands_heads","?:X"], ["-coin","?:X"], ["heads","?:X"]]
},
{
 "@name":"pr2", 
 "@confidence": 100, 
 "@role":"axiom",
 "@logic":[["-heads","?:X"], ["someheads","c"]]
},
/*
{
 "@name":"e1", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["-", ["c1","=","c2"]]
},
*/
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["someheads","c"]
}
]