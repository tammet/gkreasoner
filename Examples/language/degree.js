// John is somewhat big. John is big?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/degree.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 is somewhat big."},
{"@name": "sent_S1", "@logic": ["has degree property", "big", "#:John 1", "low", "person", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 is somewhat big."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has degree property", "big", "#:John 1", "none", "person", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-has degree property", "big", "#:John 1", "none", "person", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S2", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has degree property", "big", "#:John 1", "none", "person", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree property", "big", "#:John 1", "none", "person", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree property", "big", "#:John 1", "none", "person", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is John 1 big?"},
{"@name": "frm_stable_persist", "@logic": [["-has degree property", "big", "?:X", "none", "?:Fv13", ["$ctxt", "past", "?:Fv7", "?:Fv8", "?:Fv9"]], ["has degree property", "big", "?:X", "none", "?:Fv14", ["$ctxt", "present", "?:Fv7", "?:Fv8", "?:Fv9"]], ["$block", 0, ["$not", ["has degree property", "big", "?:X", "none", "?:Fv15", ["$ctxt", "present", "?:Fv7", "?:Fv8", "?:Fv9"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "past", "?:Fv10", "?:Fv11", "?:Fv12"]], ["has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "present", "?:Fv10", "?:Fv11", "?:Fv12"]], ["$block", 0, ["$not", ["has degree property", "big", "?:X", "?:D", "?:RC", ["$ctxt", "present", "?:Fv10", "?:Fv11", "?:Fv12"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"}
]
