// Tallinn is hardly in Latvia. Tallinn is in Latvia?
// Expected answer: Likely false
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/probability.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "entity_S1", "@logic": ["isa", "place", "#:Tallinn 1"], "@nl": "Tallinn 1 is in Latvia 2."},
{"@name": "entity_S1", "@logic": ["isa", "place", "#:Latvia 2"], "@nl": "Tallinn 1 is in Latvia 2."},
{"@name": "sent_S1", "@logic": ["-is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@confidence": 0.6, "@nl": "Tallinn 1 is in Latvia 2."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "present", "?:Fv5", "?:Fv3", "?:Fv4"]], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S2", "@sourcetype": "question_bridge", "@confidence": 0.95, "@logic": [["-is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["is rel2", "in", "Tallinn", "Latvia", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is Tallinn 1 in Latvia 2?"}
]
