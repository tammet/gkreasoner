[
{
 "@name":"p1", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":[["p","?:X"], ["r","?:X"]]
},
{
 "@name":"p2", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["p","?:X"], ["-r","?:X"]]
},
{
 "@name":"p3", 
 "@confidence": 70, 
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["r","?:X"]]
},
{
 "@name":"p4", 
 "@confidence": 60, 
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