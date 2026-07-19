// John has a car which is nice and red. The red car is nice?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/relative_clause.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 has a nice red car 2."},
{"@name": "sent_S1", "@logic": ["isa", "car", "#:car 2"], "@nl": "John 1 has a nice red car 2."},
{"@name": "sent_S1", "@logic": ["have", "#:John 1", "#:car 2", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 has a nice red car 2."},
{"@name": "sent_S1", "@logic": ["has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 has a nice red car 2."},
{"@name": "sent_S1", "@logic": ["has property", "red", "#:car 2", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 has a nice red car 2."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "car", "#:car 2"]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has property", "red", "#:car 2", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-isa", "car", "#:car 2"], ["-has property", "red", "#:car 2", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]], ["-has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S2", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has property", "red", "#:car 2", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has property", "red", "#:car 2", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has property", "red", "#:car 2", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is the red car 2 nice?"},
{"@name": "sent_S2", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree property", "good", "#:car 2", "none", "car", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is the red car 2 nice?"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "red", "?:X", ["$ctxt", "past", "?:Fv11", "?:Fv12", "?:Fv13"]], ["has property", "red", "?:X", ["$ctxt", "present", "?:Fv11", "?:Fv12", "?:Fv13"]], ["$block", 0, ["$not", ["has property", "red", "?:X", ["$ctxt", "present", "?:Fv11", "?:Fv12", "?:Fv13"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"},
{"@name": "frm_stable_persist", "@logic": [["-has property", "red", "?:X", ["$ctxt", "past", "?:Fv14", "?:Fv15", "?:Fv16"]], ["has property", "red", "?:X", ["$ctxt", "present", "?:Fv14", "?:Fv15", "?:Fv16"]], ["$block", 0, ["$not", ["has property", "red", "?:X", ["$ctxt", "present", "?:Fv14", "?:Fv15", "?:Fv16"]]]]], "@confidence": 0.95, "@nl": "[generated: frm_stable_persist]"}
]
