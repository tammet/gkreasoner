// The roof of John's house is green. John has a house?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/possession.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "entity_S1", "@logic": ["isa", "roof", "#:roof 1"], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S1", "@logic": ["isa", "roof", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]]], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 2"], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S1", "@logic": ["isa", "house", "#:house 3"], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S1", "@logic": ["has part", "#:house 3", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S1", "@logic": ["has property", "green", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "The roof 1 of John 2's house 3 is green."},
{"@name": "sent_S2", "@logic": ["isa", "roof", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]]], "@nl": "The roof 1 is the roof of John 2's house 3."},
{"@name": "sent_S2", "@logic": ["isa", "person", "#:John 2"], "@nl": "The roof 1 is the roof of John 2's house 3."},
{"@name": "sent_S2", "@logic": ["isa", "house", "#:house 3"], "@nl": "The roof 1 is the roof of John 2's house 3."},
{"@name": "sent_S2", "@logic": ["has part", "#:house 3", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], ["$ctxt", "present", "W0", "?:Fv3", "?:Fv4"]], "@nl": "The roof 1 is the roof of John 2's house 3."},
{"@name": "sent_S3", "@logic": ["isa", "person", "#:John 2"], "@nl": "John 2 owns the house 3."},
{"@name": "sent_S3", "@logic": ["isa", "house", "#:house 3"], "@nl": "John 2 owns the house 3."},
{"@name": "sent_S3", "@logic": ["have", "#:John 2", "#:house 3", ["$ctxt", "present", "W0", "?:Fv5", "?:Fv6"]], "@nl": "John 2 owns the house 3."},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "house", "sk0_house"]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["have", "#:John 2", "sk0_house", ["$ctxt", "present", "?:Fv13", "?:Fv7", "?:Fv8"]]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-isa", "house", "?:X"], ["-have", "#:John 2", "?:X", ["$ctxt", "present", "?:Fv16", "?:Fv7", "?:Fv8"]], ["$defq0"]]},
{"@name": "sent_S4", "@question": ["$defq0"]},
{"@name": "sent_S4", "@sourcetype": "question_bridge", "@confidence": 0.97, "@logic": [["-have", "#:John 2", "?:Br1", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["have", "#:John 2", "?:Br1", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["have", "#:John 2", "?:Br1", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Does John 2 have a house?"},
{"@name": "frm_theof", "@logic": ["have", "#:house 3", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "[generated: frm_theof]"},
{"@name": "frm_theof", "@logic": ["have", "#:house 3", ["$theof1", "roof", "#:house 3", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "[generated: frm_theof]"},
{"@name": "frm_theof", "@logic": ["is rel2", "roof of", ["$theof1", "roof", "?:S", "?:C"], "?:S", "?:C"], "@nl": "[generated: frm_theof]"},
{"@name": "frm_theof", "@logic": ["isa", "roof", ["$theof1", "roof", "?:S", "?:C"]], "@nl": "[generated: frm_theof]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "green", "?:X", ["$ctxt", "past", "?:Fv17", "?:Fv18", "?:Fv19"]], ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv17", "?:Fv18", "?:Fv19"]], ["$block", 0, ["$not", ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv17", "?:Fv18", "?:Fv19"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "green", "?:X", ["$ctxt", "past", "?:Fv20", "?:Fv21", "?:Fv22"]], ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv20", "?:Fv21", "?:Fv22"]], ["$block", 0, ["$not", ["has property", "green", "?:X", ["$ctxt", "present", "?:Fv20", "?:Fv21", "?:Fv22"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"}
]
