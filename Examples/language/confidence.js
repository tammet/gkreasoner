// Yellow and green elephants are nice. John is an elephant. John is yellow and green. John is nice?
// Expected answer: Probably true
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/confidence.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["-has property", "yellow", "?:X", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["-has property", "green", "?:X", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["has degree property", "good", "?:X", "none", "?:Fv53", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["$block", ["$", "elephant", 3], ["$not", ["has degree property", "good", "?:X", "none", "?:Fv54", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]]]], "@confidence": 0.9, "@nl": "Elephants that are yellow and green are nice."},
{"@name": "sent_S2", "@logic": ["isa", "elephant", "#:John 1"], "@nl": "John 1 is an elephant."},
{"@name": "sent_S3", "@logic": ["has property", "yellow", "#:John 1", ["$ctxt", "present", "W0", "?:Fv7", "?:Fv8"]], "@nl": "John 1 is yellow."},
{"@name": "sent_S4", "@logic": ["has property", "green", "#:John 1", ["$ctxt", "present", "W0", "?:Fv9", "?:Fv10"]], "@nl": "John 1 is green."},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-$defq0"], ["has degree property", "good", "#:John 1", "none", "?:Fv55", ["$ctxt", "present", "?:Fv13", "?:Fv11", "?:Fv12"]]]},
{"@name": "sent_S5", "@sourcetype": "question", "@logic": [["-has degree property", "good", "#:John 1", "none", "?:Fv56", ["$ctxt", "present", "?:Fv13", "?:Fv11", "?:Fv12"]], ["$defq0"]]},
{"@name": "sent_S5", "@question": ["$defq0"]},
{"@name": "sent_S5", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has degree property", "good", "#:John 1", "none", "?:Fv57", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree property", "good", "#:John 1", "none", "?:Fv58", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree property", "good", "#:John 1", "none", "?:Fv59", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is John 1 nice?"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-has property", "yellow", "$some_not_yellow_elephant", ["$ctxt", "?:Fv36", "?:Fv33", "?:Fv34", "?:Fv35"]], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-has property", "green", "$some_not_green_elephant", ["$ctxt", "?:Fv40", "?:Fv37", "?:Fv38", "?:Fv39"]], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["has degree property", "good", "$some_nice_entity", "none", "?:Fv60", ["$ctxt", "?:Fv44", "?:Fv41", "?:Fv42", "?:Fv43"]], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-has degree property", "good", "$some_not_nice_entity", "none", "?:Fv61", ["$ctxt", "?:Fv52", "?:Fv49", "?:Fv50", "?:Fv51"]], "@nl": "[population: from input]"},
{"@name": "frm_excl", "@logic": [["-has property", "green", "?:X", "?:Fv15"], ["-has property", "yellow", "?:X", "?:Fv15"], ["$block", 0, ["has property", "yellow", "?:X", "?:Fv15"]]], "@confidence": 0.95, "@nl": "[generated: frm_excl]"},
{"@name": "frm_excl", "@logic": [["-has property", "green", "?:X", "?:Fv16"], ["-has property", "yellow", "?:X", "?:Fv16"], ["$block", 0, ["has property", "green", "?:X", "?:Fv16"]]], "@confidence": 0.95, "@nl": "[generated: frm_excl]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "green", "?:X", ["$ctxt", "past", "?:Fv17", "?:Fv18", "?:Fv19"]], ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv17", "?:Fv18", "?:Fv19"]], ["$block", 0, ["$not", ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv17", "?:Fv18", "?:Fv19"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "green", "?:X", ["$ctxt", "past", "?:Fv20", "?:Fv21", "?:Fv22"]], ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv20", "?:Fv21", "?:Fv22"]], ["$block", 0, ["$not", ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv20", "?:Fv21", "?:Fv22"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "yellow", "?:X", ["$ctxt", "past", "?:Fv23", "?:Fv24", "?:Fv25"]], ["has property", "yellow", "?:X", ["$ctxt", "present", "?:Fv23", "?:Fv24", "?:Fv25"]], ["$block", 0, ["$not", ["has property", "yellow", "?:X", ["$ctxt", "present", "?:Fv23", "?:Fv24", "?:Fv25"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "yellow", "?:X", ["$ctxt", "past", "?:Fv26", "?:Fv27", "?:Fv28"]], ["has property", "yellow", "?:X", ["$ctxt", "present", "?:Fv26", "?:Fv27", "?:Fv28"]], ["$block", 0, ["$not", ["has property", "yellow", "?:X", ["$ctxt", "present", "?:Fv26", "?:Fv27", "?:Fv28"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"}
]
