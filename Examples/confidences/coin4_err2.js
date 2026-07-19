[
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
 "@name":"pr1", 
 "@confidence": 60, 
 "@role":"axiom",
 "@logic":[["-coin","?:X"], ["heads","?:X"]]
},
{
 "@name":"pr2", 
 "@confidence": 100, 
 "@role":"axiom",
 "@logic":[["-heads","?:X"], ["someheads","c"]]
},
{
 "@name":"e1", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":["-", ["c3","=","c4"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["someheads","c"]
}
]