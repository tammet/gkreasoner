[
{"@logic": ["bird","a"]},
{"@logic": ["bird","b"]},

{"@logic": ["-flies","a"], "@confidence": 0.9},
{"@logic": [["-bird","?:X"],["flies","?:X"], ["$block", 2, ["$not", ["flies", "?:X"]]]]},

{"@question": ["flies","?:X"]}
]
