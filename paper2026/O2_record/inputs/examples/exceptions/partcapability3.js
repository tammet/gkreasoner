[

// from conceptnet:

{"@role": "axiom", "@confidence": 1.0, "@logic": [["be", "wing", "?:X1"], "=>", ["usedfor", "fly", "?:X1"] ]},

// split version (separate for class and instance) of a rule from quasimodo

{"@role": "axiom", "@confidence": 0.998553831433605, "@logic": [[["individual","?:X1"],"&",["be", "bird", "?:X1"]], "=>", [["hasa", "wing", "?:X1"], "|", ["$block", 10, ["$not", ["hasa", "wing", "?:X1"]]]]]},

{"@role": "axiom", "@confidence": 0.998553831433605, "@logic": [[["class","?:X1"],"&",["be", "bird", "?:X1"]], "=>", ["hasa", "wing", "?:X1"]]},

// from quasimodo:

{"@role": "axiom", "@confidence": 0.9, "@logic": [["be", "bird", "?:X1"], "=>", [["capability", "fly", "?:X1"], "|", ["$block", 10, ["$not", ["capability", "fly", "?:X1"]]]]]},

// our commonsense rule:

{"@role": "assumption", "@confidence": 1.0, "@logic": [["-hasa", "?:O", "?:C"], ["-usedfor", "?:U", "?:O"], ["-be","?:C","?:I"], ["hasa", "?:O", "?:I"], ["-capability","?:U","?:I"]] },

// reflexivity of be:

{"@role": "assumption","@confidence": 1.0, "@logic": ["be", "?:P", "?:P"]},

// question assumptions:

{"@role": "assumption", "@confidence": 1.0, "@logic":  ["be","bird","any_bird_constant"]},

["-hasa", "wing", "any_bird_constant"], 

["individual","any_bird_constant"],

["class","bird"],

// question:

{"@question": ["-capability","fly","any_bird_constant"]}

]

