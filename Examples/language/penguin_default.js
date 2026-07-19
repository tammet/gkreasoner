// Penguins are birds. Penguins do not fly. Birds fly. John is a penguin. John flies?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/penguin_default.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "penguin", "?:X"], ["isa", "bird", "?:X"]], "@nl": "Penguins are birds."},
{"@name": "sent_S2", "@logic": [["-isa", "penguin", "?:X"], ["-isa", "activity", "?:E"], ["-has type", "?:E", "fly", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["-has actor", "?:E", "?:X", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["-capability", "?:E"]], "@nl": "Penguins cannot fly."},
{"@name": "sent_S3", "@logic": [["-isa", "bird", "?:X"], ["isa", "activity", ["sk0", "?:X"]]], "@nl": "Birds can fly."},
{"@name": "sent_S3", "@logic": [["-isa", "bird", "?:X"], ["has type", ["sk0", "?:X"], "fly", ["$ctxt", "?:Fv12", "?:Fv11", "?:Fv9", "?:Fv10"]]], "@nl": "Birds can fly."},
{"@name": "sent_S3", "@logic": [["-isa", "bird", "?:X"], ["has actor", ["sk0", "?:X"], "?:X", ["$ctxt", "?:Fv12", "?:Fv11", "?:Fv9", "?:Fv10"]]], "@nl": "Birds can fly."},
{"@name": "sent_S3", "@logic": [["-isa", "bird", "?:X"], ["capability", ["sk0", "?:X"]], ["$block", ["$", "bird", 1], ["$not", ["capability", ["sk0", "?:X"]]]]], "@confidence": 0.9, "@nl": "Birds can fly."},
{"@name": "sent_S4", "@logic": ["isa", "penguin", "#:John 1"], "@nl": "John 1 is a penguin."},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "activity", "sk1_activity"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0"], ["has type", "sk1_activity", "fly", ["$ctxt", "?:Fv22", "?:Fv21", "?:Fv15", "?:Fv16"]]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0"], ["has actor", "sk1_activity", "#:John 1", ["$ctxt", "?:Fv24", "?:Fv23", "?:Fv15", "?:Fv16"]]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0"], ["capability", "sk1_activity"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-isa", "activity", "?:E"], ["-has type", "?:E", "fly", ["$ctxt", "?:Fv28", "?:Fv27", "?:Fv15", "?:Fv16"]], ["-has actor", "?:E", "#:John 1", ["$ctxt", "?:Fv30", "?:Fv29", "?:Fv15", "?:Fv16"]], ["-capability", "?:E"], ["$defq0"]]},
{"@name": "sent_S5", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "penguin", "$some_not_penguin"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "bird", "$some_bird"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "bird", "$some_not_bird"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["isa", "activity", "$some_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["-isa", "activity", "$some_not_activity"], "@nl": "[population: from input]"},
{"@name": "frm_syn", "@logic": [["-has type", "?:E", "fly", "?:Fv31"], ["has type", "?:E", "go", "?:Fv31"]], "@confidence": 0.52, "@nl": "[generated: frm_syn]"}
]
