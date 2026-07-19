// John stopped smoking. Does John smoke now?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/event_change.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["isa", "activity", "sk0_activity"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has type", "sk0_activity", "stop", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has actor", "sk0_activity", "#:John 1", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has time", "sk0_activity", "past", "in", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has content", "sk0_activity", "sk1_activity"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["isa", "activity", "sk1_activity"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has type", "sk1_activity", "smoke", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has actor", "sk1_activity", "#:John 1", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["has time", "sk1_activity", "past", "in", ["$ctxt", "past", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["actuality", "sk0_activity"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S1", "@logic": ["next", "W0", "W1"], "@nl": "John 1 stopped smoking."},
{"@name": "sent_S2", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 smoked."},
{"@name": "sent_S2", "@logic": ["isa", "activity", "sk2_activity"], "@nl": "John 1 smoked."},
{"@name": "sent_S2", "@logic": ["has type", "sk2_activity", "smoke", ["$ctxt", "past", "?:Fv5", "?:Fv3", "?:Fv4"]], "@nl": "John 1 smoked."},
{"@name": "sent_S2", "@logic": ["has actor", "sk2_activity", "#:John 1", ["$ctxt", "past", "?:Fv5", "?:Fv3", "?:Fv4"]], "@nl": "John 1 smoked."},
{"@name": "sent_S2", "@logic": ["has time", "sk2_activity", "past", "in", ["$ctxt", "past", "?:Fv5", "?:Fv3", "?:Fv4"]], "@nl": "John 1 smoked."},
{"@name": "sent_S2", "@logic": [["typical", "sk2_activity", ["$ctxt", "past", "?:Fv5", "?:Fv3", "?:Fv4"]], ["$block", ["$", "$generic", 1], ["$not", ["typical", "sk2_activity", ["$ctxt", "past", "?:Fv5", "?:Fv3", "?:Fv4"]]]]], "@nl": "John 1 smoked."},
{"@name": "sent_S3", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 does not smoke."},
{"@name": "sent_S3", "@logic": [["-isa", "activity", "?:E"], ["-has type", "?:E", "smoke", ["$ctxt", "present", "W1", "?:Fv7", "?:Fv8"]], ["-has actor", "?:E", "#:John 1", ["$ctxt", "present", "W1", "?:Fv7", "?:Fv8"]], ["-typical", "?:E", ["$ctxt", "present", "W1", "?:Fv7", "?:Fv8"]]], "@nl": "John 1 does not smoke."},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "activity", "sk3_activity"]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["has type", "sk3_activity", "smoke", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["has actor", "sk3_activity", "#:John 1", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-$defq0"], ["typical", "sk3_activity", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]]]},
{"@name": "sent_S4", "@sourcetype": "question", "@logic": [["-isa", "activity", "?:E"], ["-has type", "?:E", "smoke", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]], ["-has actor", "?:E", "#:John 1", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]], ["-typical", "?:E", ["$ctxt", "present", "?:Fv11", "?:Fv9", "?:Fv10"]], ["$defq0"]]},
{"@name": "sent_S4", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "activity", "$some_activity"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "activity", "$some_not_activity"], "@nl": "[population: from input]"},
{"@name": "frm_world_geom", "@sourcetype": "world_geometry", "@logic": ["next", "W0", "W1"], "@nl": "[generated: frm_world_geom]"}
]
