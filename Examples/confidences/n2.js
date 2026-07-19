[
{
 "@name":"a", 
 "@confidence": 60,
 "@role":"axiom",
 "@logic":["p","a"]
},
/*
{
 "@name":"b", 
 "@confidence": 70,
 "@role":"axiom",
 "@logic":["p","b"]
},
{
 "@name":"nb", 
 "@confidence": 5,
 "@role":"axiom",
 "@logic":["-r","b"]
},
*/
{
 "@name":"r", 
 "@confidence": 80,
 "@role":"axiom",
 "@logic":["r","a"]
},
{
 "@name":"nr", 
 "@confidence": 70,
 "@role":"axiom",
 "@logic":["-r","a"]
},
{
 "@name":"pr", 
 "@confidence": 90,
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["r","?:X"]]
},
{
 "@name":"pr", 
 "@confidence": 20,
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["-r","?:X"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["r","?:X"]
}
]