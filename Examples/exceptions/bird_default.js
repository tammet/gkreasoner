[
{"@logic": ["bird","a"]},
{"@logic": ["bird","b"]},

{"@logic": [["-bird","?:X"],["flies","?:X"], ["$block", 2, ["$not", ["flies", "?:X"]]]]},

{"@question": ["flies","?:X"]}
]
