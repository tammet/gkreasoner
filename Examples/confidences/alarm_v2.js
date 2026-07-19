/*
0.7::burglary.
0.2::earthquake.

0.9::alarm :- burglary, earthquake.
0.8::alarm :- burglary, \+earthquake.
0.1::alarm :- \+burglary, earthquake.

evidence(alarm,true).
query(burglary).
query(earthquake).
*/

[
{
 "@name":"c1", 
 "@confidence": 70,
 "@role":"axiom",
 "@logic":["burglary","c"]
},
{
 "@name":"c1n", 
 "@confidence": 30,
 "@role":"axiom",
 "@logic":["-burglary","c"]
},
{
 "@name":"c2", 
 "@confidence": 20,
 "@role":"axiom",
 "@logic":["earthquake","c"]
},
{
 "@name":"c2n", 
 "@confidence": 80,
 "@role":"axiom",
 "@logic":["-earthquake","c"]
},
{
 "@name":"pr1", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":[["-burglary","c"], ["-earthquake","c"],  ["alarm","c"]]
},
{
 "@name":"pr2", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["-burglary","c"], ["earthquake","c"],  ["alarm","c"]]
},
{
 "@name":"pr3", 
 "@confidence": 10, 
 "@role":"axiom",
 "@logic":[["burglary","c"], ["-earthquake","c"],  ["alarm","c"]]
},

{
 "@name":"pr1n1", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":[["burglary","c"], ["-alarm","c"]]
},
{
 "@name":"pr1n2", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":[["earthquake","c"], ["-alarm","c"]]
},
{
 "@name":"pr2n1", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["burglary","c"], ["-alarm","c"]]
},
{
 "@name":"pr2n2", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["-earthquake","c"],  ["-alarm","c"]]
},
{
 "@name":"pr3n1", 
 "@confidence": 10, 
 "@role":"axiom",
 "@logic":[["-burglary","c"],  ["-alarm","c"]]
},
{
 "@name":"pr3n2", 
 "@confidence": 10, 
 "@role":"axiom",
 "@logic":[ ["earthquake","c"],  ["-alarm","c"]]
},
{
 "@name":"a1", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["alarm","c"]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["burglary","c"]
}
/*
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["earthquake","c"]
}
*/
]