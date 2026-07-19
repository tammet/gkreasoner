// Elephants have trunks or tails. John is an elephant. John has no trunk. John has a tail?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/disjunction.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "trunk", ["sk0", "?:X"]], ["isa", "tail", ["sk1", "?:X"]]], "@nl": "Elephants have trunks or tails."},
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "trunk", ["sk0", "?:X"]], ["has part", "?:X", ["sk1", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["$block", ["$", "elephant", 1], ["$not", ["has part", "?:X", ["sk1", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]]]], "@confidence": 0.9933, "@nl": "Elephants have trunks or tails."},
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "tail", ["sk1", "?:X"]], ["has part", "?:X", ["sk0", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["$block", ["$", "elephant", 1], ["$not", ["has part", "?:X", ["sk0", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]]]], "@confidence": 0.9933, "@nl": "Elephants have trunks or tails."},
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["has part", "?:X", ["sk0", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["has part", "?:X", ["sk1", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["$block", ["$", "elephant", 1], ["$not", ["has part", "?:X", ["sk1", "?:X"], ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]]]], "@confidence": 0.9933, "@nl": "Elephants have trunks or tails."},
{"@name": "sent_S2", "@logic": ["isa", "elephant", "#:John 1"], "@nl": "John 1 is an elephant."},
{"@name": "sent_S3", "@logic": [["-isa", "trunk", "?:Y"], ["-has part", "#:John 1", "?:Y", ["$ctxt", "present", "W0", "?:Fv7", "?:Fv8"]]], "@nl": "John 1 has no trunk."},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "tail", "sk2_tail"]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["has part", "#:John 1", "sk2_tail", ["$ctxt", "present", "?:Fv15", "?:Fv9", "?:Fv10"]]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-isa", "tail", "?:Z"], ["-has part", "#:John 1", "?:Z", ["$ctxt", "present", "?:Fv18", "?:Fv9", "?:Fv10"]], ["$defq0"]]},
{"@name": "sent_haspart_bridge", "@logic": [["-isa", "tail", "?:Y"], ["-have", "?:X", "?:Y", "?:Ctxt"], ["has part", "?:X", "?:Y", "?:Ctxt"]], "@confidence": 0.9, "@nl": "[generated: sent_haspart_bridge]"},
{"@name": "sent_haspart_bridge", "@logic": [["-isa", "trunk", "?:Y"], ["-have", "?:X", "?:Y", "?:Ctxt"], ["has part", "?:X", "?:Y", "?:Ctxt"]], "@confidence": 0.9, "@nl": "[generated: sent_haspart_bridge]"},
{"@name": "sent_S4", "@question": ["$defq0"]},
{"@name": "sent_S4", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has part", "#:John 1", "?:Br1", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has part", "#:John 1", "?:Br1", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has part", "#:John 1", "?:Br1", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Does John 1 have a tail?"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "trunk", "$some_trunk"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "trunk", "$some_not_trunk"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "tail", "$some_tail"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "tail", "$some_not_tail"], "@nl": "[population: from input]"}
]
