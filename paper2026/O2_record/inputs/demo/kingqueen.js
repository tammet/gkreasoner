[

{"@logic": ["isa","queen","q1"]},
{"@logic": ["isa","queen","q2"]},
{"@logic": ["prop","male","q2"]},

{"@logic": ["isa","king","k1"]},

{"@logic": [["isa", "queen","?:X"],  "=>", ["prop","female","?:X"]]},

{"@logic": [["prop","female","?:X"], "=>", ["-prop","male","?:X"]]},

{"@logic": [["isa","king","?:X"], "=>", ["prop","rich","?:X"]]},
{"@logic": [["isa","king","?:X"], "=>", ["prop","male","?:X"]]},
{"@logic": [["isa","king","?:X"], "=>", ["-prop","poor","?:X"]]},


//{"@logic": [["-queen","?:X"],["king","?:X"]], "@confidence":0.9},
//{"@logic": [["-king","?:X"],["male","?:X"]]},

{"@question": ["prop","?:X","q1"]}


]
