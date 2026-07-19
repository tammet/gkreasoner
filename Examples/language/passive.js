// The letter was written by Eve. Eve wrote the letter?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/passive.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:Eve 1"], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["isa", "letter", "#:letter 2"], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["isa", "activity", "sk0_activity"], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["has type", "sk0_activity", "write", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["has actor", "sk0_activity", "#:Eve 1", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["has target", "sk0_activity", "#:letter 2", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["has time", "sk0_activity", "past", "in", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S1", "@logic": ["actuality", "sk0_activity"], "@nl": "Eve 1 wrote the letter 2."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "activity", "sk1_activity"]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has type", "sk1_activity", "write", ["$ctxt", "past", "?:Fv9", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has actor", "sk1_activity", "#:Eve 1", ["$ctxt", "past", "?:Fv11", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has target", "sk1_activity", "#:letter 2", ["$ctxt", "past", "?:Fv13", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["has time", "sk1_activity", "past", "in", ["$ctxt", "past", "?:Fv15", "?:Fv3", "?:Fv4"]]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["actuality", "sk1_activity"]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-isa", "activity", "?:E"], ["-has type", "?:E", "write", ["$ctxt", "past", "?:Fv19", "?:Fv3", "?:Fv4"]], ["-has actor", "?:E", "#:Eve 1", ["$ctxt", "past", "?:Fv21", "?:Fv3", "?:Fv4"]], ["-has target", "?:E", "#:letter 2", ["$ctxt", "past", "?:Fv23", "?:Fv3", "?:Fv4"]], ["-actuality", "?:E"], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "activity", "$some_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "activity", "$some_not_activity"], "@nl": "[population: from input]"}
]
