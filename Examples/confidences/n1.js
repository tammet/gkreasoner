[
{
 "@name":"a", 
 "@confidence": 60,
 "@role":"axiom",
 "@logic":["p","a"]
},
{
 "@name":"b", 
 "@confidence": 70,
 "@role":"axiom",
 "@logic":["p","b"]
},
{
 "@name":"r", 
 "@confidence": 80,
 "@role":"axiom",
 "@logic":["r","a"]
},
{
 "@name":"pr", 
 "@confidence": 90,
 "@role":"axiom",
 "@logic":[["-p","?:X"], ["r","?:X"]]
},
{
 "@name":"q", 
 //"@role":"negated_conjecture",
 //"@logic":[["r","?:X"],"=>",["$ans","?:X"]]
 "@role": "question",    
 "@logic": ["r","?:X"]
}
]

/*

= Simple non-var question

positive:

 ["r","a"]

negative question:

 ["-r","a"]


= Simple var-question & ground answer

 ["r","?:X"]

positive:

"answer": [["$ans","b"]],
"answer": [["$ans","a"]],

negative questions:

 ["-r","a"]
 ["-r","b"]
 
= Simple var-question & var-containing answer

  ["r","?:X"]
 
positive:

"answer": [["$ans","?:U"]],
"answer": [["$ans",["f","?:V"]]],

negative questions:

 ["-r","?:U"]
 ["-r",["f","?:V"]] 


= Disjunction answer

  ["r","?:X"]

positive

"answer": [["$ans","b"], "|", ["$ans","c"]],
"answer": [["$ans","a"], "|", ["$ans","c"]],

negative questions:

 ["-r","b"]
 ["-r","c"]
 
 ["-r","a"]
 ["-r","c"]


= Disjunction var question

positive:

 ["r","?:X"], "|",  ["p","?:X"],
 
positive:

"answer": [["$ans","b"]],
"answer": [["$ans","a"]],

negative question:

 ["-r","b"], "&",  ["-","b"]
 
or alternatively
 ["-", [ ["r","b"], "|",  ["p","b"]]]

= Conjunction var question

positive:

 ["r","?:X"], "&",  ["p","?:X"],
 
positive:

"answer": [["$ans","b"]],
"answer": [["$ans","a"]],

negative question:

 ["-r","b"], "|",  ["-","b"]
 
or alternatively
 ["-", [["r","b"], "&",  ["p","b"]]]


*/