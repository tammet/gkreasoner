// John is glad. If John is glad, then Mike is not glad. Is Mike glad?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/conditional.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "entity_S2", "@logic": ["isa", "person", "#:Mike 2"], "@nl": "If John 1 is glad, then Mike 2 is not glad."},
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 is glad."},
{"@name": "sent_S1", "@logic": ["has property", "glad", "#:John 1", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 is glad."},
{"@name": "sent_S2", "@logic": [["-has property", "glad", "#:John 1", ["$ctxt", "present", "W0", "?:Fv3", "?:Fv4"]], ["-has property", "glad", "#:Mike 2", ["$ctxt", "present", "W0", "?:Fv3", "?:Fv4"]]], "@nl": "If John 1 is glad, then Mike 2 is not glad."},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has property", "glad", "#:Mike 2", ["$ctxt", "present", "?:Fv7", "?:Fv5", "?:Fv6"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-has property", "glad", "#:Mike 2", ["$ctxt", "present", "?:Fv7", "?:Fv5", "?:Fv6"]], ["$defq0"]]},
{"@name": "sent_S3", "@question": ["$defq0"]},
{"@name": "sent_S3", "@sourcetype": "question_bridge", "@confidence": 0.99, "@logic": [["-has property", "glad", "#:Mike 2", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has property", "glad", "#:Mike 2", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has property", "glad", "#:Mike 2", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is Mike 2 glad?"}
]
