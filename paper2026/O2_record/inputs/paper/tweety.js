[
{"@name": "s1", "@logic": ["bird", "tweety"], "@confidence": 0.9},
{"@name": "s2", "@logic": [["bird", "?:X"], "=>", [["flies", "?:X"], "|", ["$block", 1, ["$not", ["flies", "?:X"]]]]], "@confidence": 0.8},
{"@name": "s3", "@logic": [["penguin", "?:X"], "=>", ["-flies", "?:X"]], "@confidence": 0.7},
{"@name": "s4", "@logic": ["penguin", "tweety"], "@confidence": 0.5},
{"@name": "s5", "@logic": ["heavy", "tweety"], "@confidence": 0.6},
{"@name": "s6", "@logic": [["-heavy", "?:X"], ["-flies", "?:X"]]},
{"@name": "s7", "@logic": [["-penguin", "?:X"], ["bird", "?:X"]]},
{"@question": ["flies", "tweety"]}
]
