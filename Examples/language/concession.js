// Although John was tired, he finished the work. John finished the work?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/concession.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 was tired."},
{"@name": "sent_S1", "@logic": ["has degree property", "tired", "#:John 1", "none", "person", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 was tired."},
{"@name": "sent_S2", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["isa", "work", "#:work 2"], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["isa", "activity", "sk0_activity"], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["has type", "sk0_activity", "finish", ["$ctxt", "past", "W0", "?:Fv3", "?:Fv4"]], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["has actor", "sk0_activity", "#:John 1", ["$ctxt", "past", "W0", "?:Fv3", "?:Fv4"]], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["has target", "sk0_activity", "#:work 2", ["$ctxt", "past", "W0", "?:Fv3", "?:Fv4"]], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["has time", "sk0_activity", "past", "in", ["$ctxt", "past", "W0", "?:Fv3", "?:Fv4"]], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["actuality", "sk0_activity"], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S2", "@logic": ["next", "W0", "W1"], "@nl": "John 1 finished the work 2."},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "activity", "sk1_activity"]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has type", "sk1_activity", "finish", ["$ctxt", "past", "?:Fv10", "?:Fv5", "?:Fv6"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has actor", "sk1_activity", "#:John 1", ["$ctxt", "past", "?:Fv12", "?:Fv5", "?:Fv6"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has target", "sk1_activity", "#:work 2", ["$ctxt", "past", "?:Fv14", "?:Fv5", "?:Fv6"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has time", "sk1_activity", "past", "in", ["$ctxt", "past", "?:Fv16", "?:Fv5", "?:Fv6"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["actuality", "sk1_activity"]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-isa", "activity", "?:E"], ["-has type", "?:E", "finish", ["$ctxt", "past", "?:Fv20", "?:Fv5", "?:Fv6"]], ["-has actor", "?:E", "#:John 1", ["$ctxt", "past", "?:Fv22", "?:Fv5", "?:Fv6"]], ["-has target", "?:E", "#:work 2", ["$ctxt", "past", "?:Fv24", "?:Fv5", "?:Fv6"]], ["-actuality", "?:E"], ["$defq0"]]},
{"@name": "sent_S3", "@question": ["$defq0"]},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["isa", "activity", "$some_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S2", "@sourcetype": "populate", "@logic": ["-isa", "activity", "$some_not_activity"], "@nl": "[population: from input]"},
{"@name": "frm_world_geom", "@sourcetype": "world_geometry", "@logic": ["next", "W0", "W1"], "@nl": "[generated: frm_world_geom]"}
]
