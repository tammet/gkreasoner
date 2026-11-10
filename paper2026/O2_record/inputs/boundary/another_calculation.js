[
{"@name": "b", "@logic": ["b"], "@confidence": 0.2},
{"@name": "q_unless_b", "@logic": [["q"], "|", ["$block", 1, ["b"]]], "@confidence": 0.2},
{"@name": "q_from_b", "@logic": [["b"], "=>", ["q"]], "@confidence": 0.5},
{"@question": ["q"]}
]
