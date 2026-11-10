

[
{
 "@name":"a1", 
 "@confidence": 0.5,
 "@role":"axiom",
 "@logic":["bird","a"]
},
{
 "@name":"a2", 
 "@confidence": 0.6,
 "@role":"axiom",
 "@logic":["black","a"]
},
{
 "@name":"rule1", 
 "@confidence": 100,
 "@role":"axiom",
 "@logic":[["-bird","?:X"], ["-black","?:X"], ["blackbird","?:X"]]
},
{
 "@name":"q", 
 "@role": "question",    
 "@logic": ["blackbird","?:X"]
}
]

