[
{
 "@name":"p1", 
 "@confidence": 90, 
 "@role":"axiom",
 "@logic":["p","a"]
},
{
 "@name":"p2", 
 "@confidence": 80, 
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["p", ["f","?:X"]]]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["p",["f",["f",["f","a"]]]]
}
]