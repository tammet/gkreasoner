[
{"@logic": ["bird","b"]},
{"@logic": ["penguin","p"], "@confidence": 0.8},

{"@logic": [["-penguin","?:X"],["bird","?:X"]]},
{"@logic": [["-penguin","?:X"],["-flies","?:X"]], "@confidence": 0.9},
{"@logic": [["-bird","?:X"],["flies","?:X"], ["$block", 2, ["$not", ["flies", "?:X"]]]]},

{"@question": ["-flies","?:X"]}

]

