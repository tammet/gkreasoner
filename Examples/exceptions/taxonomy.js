[
{"@logic": ["bird","b"]},
{"@logic": ["penguin","p"]},
{"@logic": ["ostrich","os"]},
{"@logic": ["object","o"]},

{"@logic": [["-penguin","?:X"],["bird","?:X"]]},
{"@logic": [["-bird","?:X"],["object","?:X"]]},

{"@logic": [["-penguin","?:X"],["-flies","?:X"]]},
//{"@logic": [["-ostrich","?:X"],["-flies","?:X"]]},

{"@logic": [["-bird","?:X"],["flies","?:X"], ["$block", ["$","bird"], ["$not", ["flies", "?:X"]]]]},
{"@logic": [["-object","?:X"],["-flies","?:X"], ["$block", ["$","object"], ["flies", "?:X"]]]},

{"@question": ["bird","os"]}
]


