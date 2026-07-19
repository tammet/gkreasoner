// Squirrels can fly. Foxes cannot fly. Squirrels and foxes are animals. Which animal cannot fly?
// Expected answer: A fox
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/which_cannot_fly.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "squirrel", "?:X"], ["isa", "activity", ["sk0", "?:X"]]], "@nl": "Squirrels can fly."},
{"@name": "sent_S1", "@logic": [["-isa", "squirrel", "?:X"], ["has type", ["sk0", "?:X"], "fly", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]], "@nl": "Squirrels can fly."},
{"@name": "sent_S1", "@logic": [["-isa", "squirrel", "?:X"], ["has actor", ["sk0", "?:X"], "?:X", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]], "@nl": "Squirrels can fly."},
{"@name": "sent_S1", "@logic": [["-isa", "squirrel", "?:X"], ["capability", ["sk0", "?:X"]], ["$block", ["$", "squirrel", 1], ["$not", ["capability", ["sk0", "?:X"]]]]], "@nl": "Squirrels can fly."},
{"@name": "sent_S2", "@logic": [["-isa", "fox", "?:X"], ["-isa", "activity", "?:E"], ["-has type", "?:E", "fly", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["-has actor", "?:E", "?:X", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["-capability", "?:E"]], "@nl": "Foxes cannot fly."},
{"@name": "sent_S3", "@logic": [["-isa", "squirrel", "?:X"], ["isa", "animal", "?:X"]], "@nl": "Squirrels are animals."},
{"@name": "sent_S4", "@logic": [["-isa", "fox", "?:X"], ["isa", "animal", "?:X"]], "@nl": "Foxes are animals."},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0", "?:X"], ["isa", "animal", "?:X"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0", "?:X"], ["-isa", "activity", "?:E"], ["-has type", "?:E", "fly", ["$ctxt", "?:Fv26", "?:Fv25", "?:Fv17", "?:Fv18"]], ["-has actor", "?:E", "?:X", ["$ctxt", "?:Fv28", "?:Fv27", "?:Fv17", "?:Fv18"]], ["-capability", "?:E"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-isa", "animal", "?:X"], ["isa", "activity", ["sk1", "?:X"]], ["$defq0", "?:X"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-isa", "animal", "?:X"], ["has type", ["sk1", "?:X"], "fly", ["$ctxt", "?:Fv36", "?:Fv35", "?:Fv17", "?:Fv18"]], ["$defq0", "?:X"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-isa", "animal", "?:X"], ["has actor", ["sk1", "?:X"], "?:X", ["$ctxt", "?:Fv40", "?:Fv39", "?:Fv17", "?:Fv18"]], ["$defq0", "?:X"]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-isa", "animal", "?:X"], ["capability", ["sk1", "?:X"]], ["$defq0", "?:X"]]},
{"@name": "sent_S5", "@question": ["$defq0", "?:X"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "squirrel", "$some_squirrel"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "squirrel", "$some_not_squirrel"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "activity", "$some_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "activity", "$some_not_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["isa", "fox", "$some_fox"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["-isa", "fox", "$some_not_fox"], "@nl": "[population: from input]"},
{"@name": "sent_S3", "@sourcetype": "populate", "@logic": ["isa", "animal", "$some_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S3", "@sourcetype": "populate", "@logic": ["-isa", "animal", "$some_not_animal"], "@nl": "[population: from input]"},
{"@name": "frm_syn", "@logic": [["-has type", "?:E", "fly", "?:Fv43"], ["has type", "?:E", "go", "?:Fv43"]], "@confidence": 0.52, "@nl": "[generated: frm_syn]"}
]
