// Elephants are big animals. John is an elephant. Who is nice?
// Expected answer: Unknown
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/no_information.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "animal", "?:X"]], "@nl": "Elephants are animals."},
{"@name": "sent_S2", "@logic": [["-isa", "elephant", "?:X"], ["has degree property", "big", "?:X", "none", "elephant", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["$block", ["$", "elephant", 1], ["$not", ["has degree property", "big", "?:X", "none", "elephant", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]]]]], "@confidence": 0.98, "@nl": "Elephants are big."},
{"@name": "sent_S3", "@logic": ["isa", "elephant", "#:John 1"], "@nl": "John 1 is an elephant."},
{"@name": "sent_S4", "@question": ["has degree property", "good", "?:X", "none", "?:Fv45", ["$ctxt", "present", "?:Fv13", "?:Fv11", "?:Fv12"]]},
{"@name": "sent_S4", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has degree property", "good", "?:Br1", "none", "?:Fv46", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree property", "good", "?:Br1", "none", "?:Fv47", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree property", "good", "?:Br1", "none", "?:Fv48", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Which entity is nice?"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "animal", "$some_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "animal", "$some_not_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["has degree property", "big", "$some_big_elephant", "none", "elephant", ["$ctxt", "?:Fv36", "?:Fv33", "?:Fv34", "?:Fv35"]], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["isa", "elephant", "$some_big_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["-has degree property", "big", "$some_not_big_elephant", "none", "elephant", ["$ctxt", "?:Fv44", "?:Fv41", "?:Fv42", "?:Fv43"]], "@nl": "[population: from input]"},
{"@name": "frm_stable_persist", "@logic": [["-has degree property", "big", "?:X", "none", "?:Fv49", ["$ctxt", "past", "?:Fv15", "?:Fv16", "?:Fv17"]], ["has degree property", "big", "?:X", "none", "?:Fv50", ["$ctxt", "present", "?:Fv15", "?:Fv16", "?:Fv17"]], ["$block", 0, ["$not", ["has degree property", "big", "?:X", "none", "?:Fv51", ["$ctxt", "present", "?:Fv15", "?:Fv16", "?:Fv17"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "past", "?:Fv18", "?:Fv19", "?:Fv20"]], ["has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "present", "?:Fv18", "?:Fv19", "?:Fv20"]], ["$block", 0, ["$not", ["has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "present", "?:Fv18", "?:Fv19", "?:Fv20"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"}
]
