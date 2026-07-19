[
{
 "@name":"ma", 
 "@confidence": 90,
 "@role":"axiom",
 "@logic":["m","a"]
},
{
 "@name":"nma", 
 "@confidence": 10,
 "@role":"axiom",
 "@logic":["-m","a"]
},
{
 "@name":"ra", 
 "@confidence": 80,
 "@role":"axiom",
 "@logic":["r","a"]
},
{
 "@name":"nra", 
 "@confidence": 70,
 "@role":"axiom",
 "@logic":["-r","a"]
},
{
 "@name":"rb", 
 "@confidence": 60,
 "@role":"axiom",
 "@logic":["r","b"]
},
{
 "@name":"nrb", 
 "@confidence": 20,
 "@role":"axiom",
 "@logic":["-r","b"]
},
/*
{
 "@name":"nnrb", 
 "@confidence": 10,
 "@role":"axiom",
 "@logic":["-r","?:X"]
},
{
 "@name":"nnrb", 
 "@confidence": 10,
 "@role":"axiom",
 "@logic":["-m","?:X"]
},
*/
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 //"@role": "question",    
 //"@logic": ["exists",["X"], [["r","X"], "&", ["m","X"]]]
  
  //"@question": ["exists",["X"], [["r","X"], "&", ["m","X"]]]
  "@question": [["r","?:X"], "&", ["m","?:X"]]
}
]