// The mountain is higher than the hill. Is the hill higher than the mountain?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/comparison.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "mountain", "#:mountain 1"], "@nl": "The mountain 1 is higher than the hill 2."},
{"@name": "sent_S1", "@logic": ["isa", "hill", "#:hill 2"], "@nl": "The mountain 1 is higher than the hill 2."},
{"@name": "sent_S1", "@logic": ["has degree rel2", "high", "#:mountain 1", "#:hill 2", "high", "place", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "The mountain 1 is higher than the hill 2."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has degree rel2", "high", "#:hill 2", "#:mountain 1", "high", "?:Fv7", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-has degree rel2", "high", "#:hill 2", "#:mountain 1", "high", "?:Fv8", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S2", "@sourcetype": "question_bridge", "@confidence": 0.95, "@logic": [["-has degree rel2", "high", "#:hill 2", "#:mountain 1", "high", "place", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree rel2", "high", "#:hill 2", "#:mountain 1", "high", "place", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree rel2", "high", "#:hill 2", "#:mountain 1", "high", "place", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is the hill 2 higher than the mountain 1?"}
]
