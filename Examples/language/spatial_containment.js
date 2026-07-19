// Tallinn is in Estonia. Estonia is not outside Europe. Earth contains Europe. Estonia contains Tartu. Riga is not in Estonia. Riga is in Estonia?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/spatial_containment.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "entity_S1", "@logic": ["isa", "place", "#:Tallinn 1"], "@nl": "Tallinn 1 is in Estonia 2."},
{"@name": "entity_S1", "@logic": ["isa", "place", "#:Estonia 2"], "@nl": "Tallinn 1 is in Estonia 2."},
{"@name": "entity_S2", "@logic": ["isa", "place", "#:Europe 3"], "@nl": "Estonia 2 is not outside Europe 3."},
{"@name": "entity_S3", "@logic": ["isa", "place", "#:Earth 4"], "@nl": "Earth 4 contains Europe 3."},
{"@name": "entity_S4", "@logic": ["isa", "place", "#:Tartu 5"], "@nl": "Estonia 2 contains Tartu 5."},
{"@name": "entity_S5", "@logic": ["isa", "place", "#:Riga 6"], "@nl": "Riga 6 is not in Estonia 2."},
{"@name": "sent_S1", "@logic": ["is rel2", "in", "Tallinn", "Estonia", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "Tallinn 1 is in Estonia 2."},
{"@name": "sent_S2", "@logic": ["-is rel2", "outside", "Estonia", "Europe", ["$ctxt", "present", "W0", "?:Fv3", "?:Fv4"]], "@nl": "Estonia 2 is not outside Europe 3."},
{"@name": "sent_S3", "@logic": ["is rel2", "in", "Europe", "Earth", ["$ctxt", "present", "W0", "?:Fv5", "?:Fv6"]], "@nl": "Earth 4 contains Europe 3."},
{"@name": "sent_S4", "@logic": ["is rel2", "in", "Tartu", "Estonia", ["$ctxt", "present", "W0", "?:Fv7", "?:Fv8"]], "@nl": "Estonia 2 contains Tartu 5."},
{"@name": "sent_S5", "@logic": ["-is rel2", "in", "Riga", "Estonia", ["$ctxt", "present", "W0", "?:Fv9", "?:Fv10"]], "@nl": "Riga 6 is not in Estonia 2."},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-$defq0"], ["is rel2", "in", "Riga", "Estonia", ["$ctxt", "present", "?:Fv13", "?:Fv11", "?:Fv12"]]]},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-is rel2", "in", "Riga", "Estonia", ["$ctxt", "present", "?:Fv13", "?:Fv11", "?:Fv12"]], ["$defq0"]]},
{"@name": "sent_S6", "@question": ["$defq0"]},
{"@name": "sent_S6", "@sourcetype": "question_bridge", "@confidence": 0.95, "@logic": [["-is rel2", "in", "Riga", "Estonia", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["is rel2", "in", "Riga", "Estonia", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["is rel2", "in", "Riga", "Estonia", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Is Riga 6 in Estonia 2?"},
{"@name": "frm_excl", "@logic": [["-has property", "in", "?:X", "?:Fv15"], ["-has property", "outside", "?:X", "?:Fv15"], ["$block", 0, ["has property", "outside", "?:X", "?:Fv15"]]], "@confidence": 0.95, "@nl": "[generated: frm_excl]"},
{"@name": "frm_excl", "@logic": [["-has property", "in", "?:X", "?:Fv16"], ["-has property", "outside", "?:X", "?:Fv16"], ["$block", 0, ["has property", "in", "?:X", "?:Fv16"]]], "@confidence": 0.95, "@nl": "[generated: frm_excl]"}
]
