[
{
 "@name":"p1", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":[["p","?:X"], ["p", "a"]]
},
{
 "@name":"p2", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["-p", "a"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["p","a"]
}
]