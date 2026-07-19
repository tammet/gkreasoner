// If X1 is a father of Y1, Y1 is a child of X1. If X1 is a father of Y1 and Y1 is a father of Z1, X1 is a grandfather of Z1. John is a father of Mike and Mickey. Luke is a father of John. If X1 is a grandfather of Y1, Y1 is a grandchild of X1. If X1 is male and X1 is a grandchild of Y1, X1 is a grandson of Y1. Mike or Mickey is not female. Any person is male or female. Who is a grandson of Luke?
// Expected answer: Mike or Mickey
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/family_relations.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "entity_S3", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 is a father of Mike 2."},
{"@name": "entity_S3", "@logic": ["isa", "person", "#:Mike 2"], "@nl": "John 1 is a father of Mike 2."},
{"@name": "entity_S4", "@logic": ["isa", "person", "#:Mickey 3"], "@nl": "John 1 is a father of Mickey 3."},
{"@name": "entity_S5", "@logic": ["isa", "person", "#:Luke 4"], "@nl": "Luke 4 is a father of John 1."},
{"@name": "sent_S1", "@logic": [["-is rel2", "father of", "?:X1", "?:Y1", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]], ["is rel2", "child of", "?:Y1", "?:X1", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]], "@nl": "If X1 is a father of Y1, Y1 is a child of X1."},
{"@name": "sent_S2", "@logic": [["-is rel2", "father of", "?:X1", "?:Y1", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["-is rel2", "father of", "?:Y1", "?:Z1", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]], ["is rel2", "grandfather of", "?:X1", "?:Z1", ["$ctxt", "?:Fv8", "?:Fv7", "?:Fv5", "?:Fv6"]]], "@nl": "If X1 is a father of Y1 and Y1 is a father of Z1, X1 is a grandfather of Z1."},
{"@name": "sent_S3", "@logic": ["is rel2", "father of", "#:John 1", "#:Mike 2", ["$ctxt", "present", "W0", "?:Fv9", "?:Fv10"]], "@nl": "John 1 is a father of Mike 2."},
{"@name": "sent_S4", "@logic": ["is rel2", "father of", "#:John 1", "#:Mickey 3", ["$ctxt", "present", "W0", "?:Fv11", "?:Fv12"]], "@nl": "John 1 is a father of Mickey 3."},
{"@name": "sent_S5", "@logic": ["is rel2", "father of", "#:Luke 4", "#:John 1", ["$ctxt", "present", "W0", "?:Fv13", "?:Fv14"]], "@nl": "Luke 4 is a father of John 1."},
{"@name": "sent_S6", "@logic": [["-is rel2", "grandfather of", "?:X1", "?:Y1", ["$ctxt", "?:Fv18", "?:Fv17", "?:Fv15", "?:Fv16"]], ["is rel2", "grandchild of", "?:Y1", "?:X1", ["$ctxt", "?:Fv18", "?:Fv17", "?:Fv15", "?:Fv16"]]], "@nl": "If X1 is a grandfather of Y1, Y1 is a grandchild of X1."},
{"@name": "sent_S7", "@logic": [["-has property", "male", "?:X1", ["$ctxt", "?:Fv22", "?:Fv21", "?:Fv19", "?:Fv20"]], ["-is rel2", "grandchild of", "?:X1", "?:Y1", ["$ctxt", "?:Fv22", "?:Fv21", "?:Fv19", "?:Fv20"]], ["is rel2", "grandson of", "?:X1", "?:Y1", ["$ctxt", "?:Fv22", "?:Fv21", "?:Fv19", "?:Fv20"]]], "@nl": "If X1 is male and X1 is a grandchild of Y1, X1 is a grandson of Y1."},
{"@name": "sent_S8", "@logic": [["-has property", "female", "#:Mike 2", ["$ctxt", "present", "W0", "?:Fv23", "?:Fv24"]], ["-has property", "female", "#:Mickey 3", ["$ctxt", "present", "W0", "?:Fv23", "?:Fv24"]]], "@nl": "Mike 2 or Mickey 3 is not female."},
{"@name": "sent_S9", "@logic": [["-isa", "person", "?:X"], ["has property", "male", "?:X", ["$ctxt", "?:Fv28", "?:Fv27", "?:Fv25", "?:Fv26"]], ["has property", "female", "?:X", ["$ctxt", "?:Fv28", "?:Fv27", "?:Fv25", "?:Fv26"]]], "@nl": "Any person is male or female."},
{"@name": "sent_S10", "@question": ["is rel2", "grandson of", "?:X", "#:Luke 4", ["$ctxt", "present", "?:Fv31", "?:Fv29", "?:Fv30"]]},
{"@name": "sent_S10", "@sourcetype": "question_bridge", "@confidence": 0.95, "@logic": [["-is rel2", "grandson of", "?:Br1", "#:Luke 4", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["is rel2", "grandson of", "?:Br1", "#:Luke 4", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["is rel2", "grandson of", "?:Br1", "#:Luke 4", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Which entity is a grandson of Luke 4?"},
{"@name": "sent_S9", "@sourcetype": "populate", "@logic": ["isa", "person", "$some_person"], "@nl": "[population: from input]"},
{"@name": "sent_S9", "@sourcetype": "populate", "@logic": ["-isa", "person", "$some_not_person"], "@nl": "[population: from input]"},
{"@name": "sent_S7", "@sourcetype": "populate", "@logic": ["has property", "male", "$some_male_person", ["$ctxt", "?:Fv45", "?:Fv42", "?:Fv43", "?:Fv44"]], "@nl": "[population: from input]"},
{"@name": "sent_S7", "@sourcetype": "populate", "@logic": ["isa", "person", "$some_male_person"], "@nl": "[population: from input]"},
{"@name": "sent_S7", "@sourcetype": "populate", "@logic": ["-has property", "male", "$some_not_male_person", ["$ctxt", "?:Fv53", "?:Fv50", "?:Fv51", "?:Fv52"]], "@nl": "[population: from input]"},
{"@name": "sent_S8", "@sourcetype": "populate", "@logic": ["has property", "female", "$some_female_person", ["$ctxt", "?:Fv57", "?:Fv54", "?:Fv55", "?:Fv56"]], "@nl": "[population: from input]"},
{"@name": "sent_S8", "@sourcetype": "populate", "@logic": ["isa", "person", "$some_female_person"], "@nl": "[population: from input]"},
{"@name": "frm_excl", "@logic": [["-has property", "female", "?:X", "?:Fv33"], ["-has property", "male", "?:X", "?:Fv33"]], "@confidence": 0.95, "@nl": "[generated: frm_excl]"}
]
